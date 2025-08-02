#!/usr/bin/env python3
"""
VCAT Evidence Updater System
Handles automatic updates of evidence data from various sources
"""

import os
import hashlib
import psycopg2
from pathlib import Path
from datetime import datetime
import json
import subprocess

class EvidenceUpdater:
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'database': 'vcat',
            'user': 'vcat',
            'password': 'secret123',
            'port': 5432
        }
        self.evidence_manifest = "evidence_manifest.json"
    
    def get_db_connection(self):
        """Get database connection"""
        return psycopg2.connect(**self.db_config)
    
    def calculate_directory_hash(self, directory):
        """Calculate hash of all files in directory"""
        hasher = hashlib.sha256()
        
        if not Path(directory).exists():
            return None
        
        for root, dirs, files in os.walk(directory):
            # Sort to ensure consistent ordering
            dirs.sort()
            files.sort()
            
            for filename in files:
                if filename.startswith('.'):
                    continue
                    
                filepath = Path(root) / filename
                try:
                    with open(filepath, 'rb') as f:
                        while chunk := f.read(8192):
                            hasher.update(chunk)
                    # Include filename in hash
                    hasher.update(str(filepath).encode())
                except:
                    continue
        
        return hasher.hexdigest()
    
    def load_manifest(self):
        """Load evidence manifest"""
        manifest_file = Path(self.evidence_manifest)
        if manifest_file.exists():
            try:
                with open(manifest_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def save_manifest(self, manifest):
        """Save evidence manifest"""
        with open(self.evidence_manifest, 'w') as f:
            json.dump(manifest, f, indent=2)
    
    def check_evidence_changes(self):
        """Check if evidence files have changed"""
        print("🔍 Checking for evidence changes...")
        
        evidence_dirs = [
            "../VCAT_GMAIL_EVIDENCE ",
            "../VCAT_NON_GMAIL_EVIDENCE"
        ]
        
        manifest = self.load_manifest()
        current_state = {}
        changes_detected = False
        
        for evidence_dir in evidence_dirs:
            dir_path = Path(evidence_dir)
            if dir_path.exists():
                current_hash = self.calculate_directory_hash(dir_path)
                current_state[str(dir_path)] = {
                    'hash': current_hash,
                    'last_checked': datetime.now().isoformat(),
                    'file_count': sum(1 for _ in dir_path.rglob('*') if _.is_file())
                }
                
                # Check against manifest
                old_hash = manifest.get(str(dir_path), {}).get('hash')
                if old_hash != current_hash:
                    print(f"📦 Changes detected in: {dir_path}")
                    print(f"   Old hash: {old_hash[:8] if old_hash else 'None'}...")
                    print(f"   New hash: {current_hash[:8] if current_hash else 'None'}...")
                    changes_detected = True
                else:
                    print(f"✅ No changes in: {dir_path}")
        
        return changes_detected, current_state
    
    def create_evidence_backup(self):
        """Create new evidence database backup"""
        print("💾 Creating evidence database backup...")
        
        try:
            # Run the evidence loader to update database
            result = subprocess.run(['python3', 'load_evidence_data.py'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Evidence data updated in database")
                
                # Create new backup
                backup_file = "vcat_database_backup.dump"
                subprocess.run([
                    'docker', 'exec', 'mygpt-vcat-db',
                    'pg_dump', '-U', 'vcat', '-d', 'vcat',
                    '--format=custom', '--no-owner', '--no-privileges'
                ], stdout=open(backup_file, 'wb'), check=True)
                
                print(f"✅ New backup created: {backup_file}")
                return True
            else:
                print(f"❌ Evidence loading failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Backup creation failed: {e}")
            return False
    
    def commit_changes_to_git(self, manifest):
        """Commit evidence changes to Git"""
        print("📝 Committing changes to Git...")
        
        try:
            # Add evidence files and backup
            subprocess.run(['git', 'add', 'vcat_database_backup.dump'], check=True)
            subprocess.run(['git', 'add', 'evidence_manifest.json'], check=True)
            
            # Create commit message
            file_counts = {dir_path: info['file_count'] 
                          for dir_path, info in manifest.items()}
            total_files = sum(file_counts.values())
            
            commit_msg = f"""📊 Evidence data update - {datetime.now().strftime('%Y-%m-%d %H:%M')}

🔄 Updated evidence database:
- Total files processed: {total_files}
- Database backup refreshed
- Evidence manifest updated

📁 Sources updated:
{chr(10).join(f'  - {Path(dir_path).name}: {info["file_count"]} files' for dir_path, info in manifest.items())}

🤖 Generated with Claude Code(https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"""
            
            # Commit
            subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
            print("✅ Changes committed to Git")
            
            # Optionally push to remote
            try:
                subprocess.run(['git', 'push', 'origin', 'main'], check=True)
                print("✅ Changes pushed to GitHub")
            except:
                print("⚠️ Push to GitHub failed (check permissions)")
            
            return True
            
        except Exception as e:
            print(f"❌ Git commit failed: {e}")
            return False
    
    def update_evidence_system(self):
        """Complete evidence update process"""
        print("🔄 VCAT Evidence Update Process")
        print("=" * 40)
        
        # Check for changes
        has_changes, current_state = self.check_evidence_changes()
        
        if not has_changes:
            print("ℹ️ No evidence changes detected")
            return True
        
        # Create new backup with updated data
        if not self.create_evidence_backup():
            print("❌ Failed to create evidence backup")
            return False
        
        # Save new manifest
        self.save_manifest(current_state)
        
        # Commit to Git
        if not self.commit_changes_to_git(current_state):
            print("⚠️ Git commit failed, but evidence updated locally")
        
        print("✅ Evidence update completed successfully")
        return True
    
    def get_evidence_stats(self):
        """Get current evidence statistics"""
        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            
            # Get document count
            cursor.execute("SELECT COUNT(*) FROM evidence.documents")
            doc_count = cursor.fetchone()[0]
            
            # Get email count
            cursor.execute("SELECT COUNT(*) FROM evidence.emails")
            email_count = cursor.fetchone()[0]
            
            # Get file type breakdown
            cursor.execute("""
                SELECT file_type, COUNT(*) 
                FROM evidence.documents 
                WHERE file_type IS NOT NULL 
                GROUP BY file_type 
                ORDER BY COUNT(*) DESC
            """)
            file_types = cursor.fetchall()
            
            conn.close()
            
            return {
                'documents': doc_count,
                'emails': email_count,
                'total': doc_count + email_count,
                'file_types': dict(file_types)
            }
            
        except Exception as e:
            print(f"❌ Could not get stats: {e}")
            return None
    
    def status(self):
        """Show evidence system status"""
        print("📊 VCAT Evidence System Status")
        print("=" * 35)
        
        # Database stats
        stats = self.get_evidence_stats()
        if stats:
            print(f"📄 Documents: {stats['documents']}")
            print(f"📧 Emails: {stats['emails']}")
            print(f"📊 Total Evidence: {stats['total']}")
            print(f"📁 File Types: {', '.join(f'{ft}({cnt})' for ft, cnt in stats['file_types'].items())}")
        
        # Manifest status
        manifest = self.load_manifest()
        if manifest:
            print(f"\n📋 Evidence Sources:")
            for dir_path, info in manifest.items():
                print(f"   {Path(dir_path).name}: {info['file_count']} files")
                print(f"   Last checked: {info['last_checked'][:19]}")
        else:
            print("\n⚠️ No evidence manifest found")
        
        # Check for changes
        has_changes, _ = self.check_evidence_changes()
        if has_changes:
            print("\n🔄 Status: Updates available")
        else:
            print("\n✅ Status: Up to date")

def main():
    import sys
    updater = EvidenceUpdater()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "--check":
            has_changes, _ = updater.check_evidence_changes()
            sys.exit(1 if has_changes else 0)
            
        elif command == "--update":
            success = updater.update_evidence_system()
            sys.exit(0 if success else 1)
            
        elif command == "--status":
            updater.status()
            
        elif command == "--stats":
            stats = updater.get_evidence_stats()
            if stats:
                print(json.dumps(stats, indent=2))
            
    else:
        print("📊 VCAT Evidence Updater")
        print("Commands:")
        print("  --check   Check for evidence changes")
        print("  --update  Update evidence system")
        print("  --status  Show system status")
        print("  --stats   Show statistics (JSON)")

if __name__ == "__main__":
    main()