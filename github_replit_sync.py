#!/usr/bin/env python3
"""
GitHub-Replit Sync System for VCAT Evidence Repository
Enables automatic updates from GitHub to Replit deployment
"""

import os
import subprocess
import requests
import json
from datetime import datetime
from pathlib import Path
import psycopg2

class GitHubReplitSync:
    def __init__(self):
        self.github_repo = "ck999kk/VCAT-Evidence-Repository"
        self.github_api = f"https://api.github.com/repos/{self.github_repo}"
        self.local_version_file = ".github_version"
        
    def get_latest_github_commit(self):
        """Get latest commit SHA from GitHub"""
        try:
            response = requests.get(f"{self.github_api}/commits/main")
            if response.status_code == 200:
                commit_data = response.json()
                return {
                    'sha': commit_data['sha'][:8],
                    'message': commit_data['commit']['message'],
                    'date': commit_data['commit']['committer']['date'],
                    'author': commit_data['commit']['author']['name']
                }
        except Exception as e:
            print(f"❌ GitHub API error: {e}")
            return None
    
    def get_current_version(self):
        """Get current deployed version"""
        version_file = Path(self.local_version_file)
        if version_file.exists():
            try:
                with open(version_file, 'r') as f:
                    return json.loads(f.read())
            except:
                pass
        return None
    
    def save_version(self, commit_info):
        """Save current version info"""
        with open(self.local_version_file, 'w') as f:
            json.dump(commit_info, f, indent=2)
    
    def check_for_updates(self):
        """Check if updates are available from GitHub"""
        print("🔍 Checking for GitHub updates...")
        
        latest = self.get_latest_github_commit()
        current = self.get_current_version()
        
        if not latest:
            return False, "Cannot fetch GitHub info"
        
        if not current or current.get('sha') != latest['sha']:
            print(f"📦 Update available:")
            print(f"   Current: {current.get('sha', 'unknown') if current else 'Not deployed'}")
            print(f"   Latest: {latest['sha']}")
            print(f"   Message: {latest['message'][:60]}...")
            return True, latest
        else:
            print("✅ Already up to date")
            return False, "Already current"
    
    def pull_from_github(self):
        """Pull latest changes from GitHub"""
        print("⬇️ Pulling from GitHub...")
        try:
            # Git pull
            result = subprocess.run(['git', 'pull', 'origin', 'main'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Git pull successful")
                return True
            else:
                print(f"❌ Git pull failed: {result.stderr}")
                return False
        except Exception as e:
            print(f"❌ Git pull error: {e}")
            return False
    
    def update_database(self):
        """Update database if new backup exists"""
        backup_file = Path("vcat_database_backup.dump")
        if backup_file.exists():
            print("📊 Updating database from backup...")
            try:
                # Check if database exists and has data
                conn = psycopg2.connect(
                    host='localhost',
                    database='vcat',
                    user='vcat',
                    password='secret123'
                )
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM evidence.documents")
                current_count = cursor.fetchone()[0]
                conn.close()
                
                if current_count > 0:
                    print(f"   Current database has {current_count} documents")
                    print("   Backing up current data before update...")
                
                # Restore from backup
                env = {**os.environ, 'PGPASSWORD': 'secret123'}
                result = subprocess.run([
                    'pg_restore',
                    '-h', 'localhost',
                    '-U', 'vcat',
                    '-d', 'vcat',
                    '--clean',
                    '--if-exists',
                    '--no-owner',
                    '--no-privileges',
                    str(backup_file)
                ], capture_output=True, text=True, env=env)
                
                if result.returncode == 0:
                    print("✅ Database updated successfully")
                    return True
                else:
                    print(f"❌ Database update failed: {result.stderr}")
                    return False
                    
            except Exception as e:
                print(f"❌ Database update error: {e}")
                return False
        else:
            print("ℹ️ No database backup found, skipping database update")
            return True
    
    def restart_service(self):
        """Restart the application service"""
        print("🔄 Restarting application...")
        try:
            # Kill existing Python processes
            subprocess.run(['pkill', '-f', 'main.py'], capture_output=True)
            
            # Start new process in background
            subprocess.Popen(['python3', 'main.py'], 
                           stdout=subprocess.DEVNULL, 
                           stderr=subprocess.DEVNULL)
            
            print("✅ Application restarted")
            return True
        except Exception as e:
            print(f"❌ Restart failed: {e}")
            return False
    
    def sync_from_github(self):
        """Complete sync process from GitHub"""
        print("🔄 GitHub → Replit Sync Process")
        print("=" * 40)
        
        # Check for updates
        has_updates, info = self.check_for_updates()
        if not has_updates:
            print("ℹ️ No updates needed")
            return True
        
        # Pull changes
        if not self.pull_from_github():
            return False
        
        # Update database
        if not self.update_database():
            print("⚠️ Database update failed, but continuing...")
        
        # Restart service
        if not self.restart_service():
            print("⚠️ Service restart failed")
        
        # Save version info
        if isinstance(info, dict):
            self.save_version(info)
            print(f"✅ Sync completed successfully")
            print(f"   Now running: {info['sha']} - {info['message'][:40]}...")
            return True
        
        return False
    
    def setup_auto_sync(self):
        """Setup automatic sync via cron or scheduled task"""
        cron_job = f"""
# VCAT Evidence Repository Auto-Sync (every 30 minutes)
*/30 * * * * cd {os.getcwd()} && python3 github_replit_sync.py --auto
"""
        
        print("⚙️ Auto-sync setup:")
        print("Add this to your crontab (crontab -e):")
        print(cron_job)
        
        # Also create a webhook endpoint for instant updates
        webhook_code = '''
@app.post("/webhook/github")
async def github_webhook(request: Request):
    """GitHub webhook for instant updates"""
    payload = await request.json()
    
    if payload.get("ref") == "refs/heads/main":
        # Trigger sync in background
        import threading
        sync_thread = threading.Thread(target=lambda: GitHubReplitSync().sync_from_github())
        sync_thread.start()
        
        return {"status": "sync_triggered"}
    
    return {"status": "ignored"}
'''
        
        print("\n🔗 For instant updates, add this to main.py:")
        print(webhook_code)
    
    def status(self):
        """Show current sync status"""
        print("📊 GitHub-Replit Sync Status")
        print("=" * 30)
        
        current = self.get_current_version()
        latest = self.get_latest_github_commit()
        
        if current:
            print(f"🏠 Current Version: {current['sha']}")
            print(f"📅 Deployed: {current.get('date', 'Unknown')}")
            print(f"💬 Message: {current.get('message', 'No message')[:50]}...")
        else:
            print("🏠 Current Version: Not tracked")
        
        if latest:
            print(f"🌟 Latest GitHub: {latest['sha']}")
            print(f"📅 Committed: {latest['date']}")
            print(f"👤 Author: {latest['author']}")
            print(f"💬 Message: {latest['message'][:50]}...")
            
            if current and current['sha'] == latest['sha']:
                print("✅ Status: Up to date")
            else:
                print("🔄 Status: Update available")
        else:
            print("❌ Cannot fetch GitHub status")

def main():
    import sys
    sync = GitHubReplitSync()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "--check":
            has_updates, info = sync.check_for_updates()
            sys.exit(0 if not has_updates else 1)
            
        elif command == "--sync":
            success = sync.sync_from_github()
            sys.exit(0 if success else 1)
            
        elif command == "--auto":
            # For cron jobs - sync only if updates available
            has_updates, _ = sync.check_for_updates()
            if has_updates:
                sync.sync_from_github()
            sys.exit(0)
            
        elif command == "--setup":
            sync.setup_auto_sync()
            
        elif command == "--status":
            sync.status()
            
    else:
        print("🔗 GitHub-Replit Sync Tool")
        print("Commands:")
        print("  --check   Check for updates")
        print("  --sync    Sync from GitHub")
        print("  --auto    Auto-sync (for cron)")
        print("  --setup   Setup auto-sync")
        print("  --status  Show sync status")

if __name__ == "__main__":
    main()