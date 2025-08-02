#!/usr/bin/env python3
"""
Auto-Deploy System for VCAT Evidence Repository
Handles automatic deployment from GitHub to Replit with evidence updates
"""

import os
import json
import subprocess
import time
from datetime import datetime
from pathlib import Path
from github_replit_sync import GitHubReplitSync
from evidence_updater import EvidenceUpdater

class AutoDeploy:
    def __init__(self):
        self.sync = GitHubReplitSync()
        self.evidence = EvidenceUpdater()
        self.deploy_log = "deploy_log.json"
        
    def log_deployment(self, status, details):
        """Log deployment activity"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'status': status,
            'details': details
        }
        
        # Load existing log
        log_file = Path(self.deploy_log)
        if log_file.exists():
            try:
                with open(log_file, 'r') as f:
                    log_data = json.load(f)
            except:
                log_data = []
        else:
            log_data = []
        
        # Add new entry
        log_data.append(log_entry)
        
        # Keep only last 50 entries
        log_data = log_data[-50:]
        
        # Save log
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        print(f"📝 {status}: {details}")
    
    def check_system_health(self):
        """Check if the system is healthy"""
        try:
            # Check database connection
            conn = self.evidence.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM evidence.documents")
            doc_count = cursor.fetchone()[0]
            conn.close()
            
            if doc_count > 0:
                return True, f"System healthy - {doc_count} documents"
            else:
                return False, "Database empty"
                
        except Exception as e:
            return False, f"Health check failed: {e}"
    
    def deploy_to_replit(self):
        """Deploy current system to Replit environment"""
        print("🚀 Deploying to Replit environment...")
        
        try:
            # Ensure we're in deployment mode
            if not Path(".replit").exists():
                print("⚠️ Not in Replit environment, skipping deployment setup")
                return True
            
            # Check if database needs setup
            try:
                conn = self.evidence.get_db_connection()
                conn.close()
                print("✅ Database connection available")
            except:
                print("🔧 Setting up database...")
                result = subprocess.run(['python3', 'setup_replit_db.py'], 
                                      capture_output=True, text=True)
                if result.returncode != 0:
                    print(f"❌ Database setup failed: {result.stderr}")
                    return False
                print("✅ Database setup completed")
            
            # Check system health
            healthy, health_msg = self.check_system_health()
            if not healthy:
                print(f"❌ System unhealthy: {health_msg}")
                return False
            
            print(f"✅ Deployment successful: {health_msg}")
            return True
            
        except Exception as e:
            print(f"❌ Deployment failed: {e}")
            return False
    
    def full_update_cycle(self):
        """Complete update cycle: evidence → database → git → replit"""
        print("🔄 Full Update Cycle Starting")
        print("=" * 40)
        
        cycle_start = time.time()
        
        try:
            # Step 1: Check for evidence changes
            self.log_deployment("info", "Checking for evidence changes")
            has_evidence_changes, _ = self.evidence.check_evidence_changes()
            
            # Step 2: Update evidence if needed
            if has_evidence_changes:
                self.log_deployment("info", "Evidence changes detected, updating")
                if not self.evidence.update_evidence_system():
                    self.log_deployment("error", "Evidence update failed")
                    return False
                self.log_deployment("success", "Evidence updated and committed to Git")
            else:
                self.log_deployment("info", "No evidence changes detected")
            
            # Step 3: Check for GitHub updates
            self.log_deployment("info", "Checking for GitHub updates")
            has_git_updates, git_info = self.sync.check_for_updates()
            
            # Step 4: Sync from GitHub if needed
            if has_git_updates:
                self.log_deployment("info", f"GitHub updates available: {git_info}")
                if not self.sync.sync_from_github():
                    self.log_deployment("error", "GitHub sync failed")
                    return False
                self.log_deployment("success", "Synced from GitHub")
            else:
                self.log_deployment("info", "No GitHub updates needed")
            
            # Step 5: Deploy to Replit environment
            if has_evidence_changes or has_git_updates:
                self.log_deployment("info", "Deploying to Replit")
                if not self.deploy_to_replit():
                    self.log_deployment("error", "Replit deployment failed")
                    return False
                self.log_deployment("success", "Deployed to Replit")
            else:
                self.log_deployment("info", "No deployment needed - system up to date")
            
            # Step 6: Final health check
            healthy, health_msg = self.check_system_health()
            if healthy:
                cycle_time = time.time() - cycle_start
                self.log_deployment("success", f"Update cycle completed in {cycle_time:.1f}s - {health_msg}")
                return True
            else:
                self.log_deployment("error", f"Final health check failed: {health_msg}")
                return False
                
        except Exception as e:
            self.log_deployment("error", f"Update cycle failed: {e}")
            return False
    
    def setup_automation(self):
        """Setup automated deployment"""
        print("⚙️ Setting up automated deployment...")
        
        # Create automation script
        automation_script = f"""#!/bin/bash
# VCAT Evidence Repository - Auto Deployment
# Run every 15 minutes to check for updates

cd {os.getcwd()}
python3 auto_deploy.py --cycle >> deploy_automation.log 2>&1
"""
        
        script_path = Path("auto_deploy.sh")
        with open(script_path, 'w') as f:
            f.write(automation_script)
        script_path.chmod(0o755)
        
        # Cron job suggestion
        cron_job = f"""
# VCAT Auto-Deploy (every 15 minutes)
*/15 * * * * {script_path.absolute()}

# VCAT Evidence Check (every hour)
0 * * * * cd {os.getcwd()} && python3 evidence_updater.py --check && python3 evidence_updater.py --update
"""
        
        print(f"✅ Automation script created: {script_path}")
        print("\n📋 Add to crontab (crontab -e):")
        print(cron_job)
        
        # GitHub webhook
        webhook_code = '''
@app.post("/webhook/auto-deploy")
async def auto_deploy_webhook(request: Request):
    """Webhook for triggering auto-deployment"""
    import threading
    from auto_deploy import AutoDeploy
    
    # Trigger deployment in background
    def deploy():
        deployer = AutoDeploy()
        deployer.full_update_cycle()
    
    thread = threading.Thread(target=deploy)
    thread.start()
    
    return {"status": "deployment_triggered", "timestamp": datetime.now().isoformat()}
'''
        
        print("\n🔗 Add to main.py for webhook deployment:")
        print(webhook_code)
    
    def show_logs(self, limit=10):
        """Show recent deployment logs"""
        log_file = Path(self.deploy_log)
        if not log_file.exists():
            print("📝 No deployment logs found")
            return
        
        try:
            with open(log_file, 'r') as f:
                logs = json.load(f)
            
            print(f"📊 Last {min(limit, len(logs))} Deployment Logs:")
            print("=" * 50)
            
            for log in logs[-limit:]:
                timestamp = log['timestamp'][:19].replace('T', ' ')
                status = log['status'].upper()
                details = log['details']
                
                status_emoji = {
                    'SUCCESS': '✅',
                    'ERROR': '❌',
                    'INFO': 'ℹ️',
                    'WARNING': '⚠️'
                }.get(status, '📝')
                
                print(f"{status_emoji} {timestamp} [{status}] {details}")
                
        except Exception as e:
            print(f"❌ Could not read logs: {e}")
    
    def status(self):
        """Show auto-deploy system status"""
        print("🚀 Auto-Deploy System Status")
        print("=" * 30)
        
        # System health
        healthy, health_msg = self.check_system_health()
        print(f"🏥 System Health: {'✅' if healthy else '❌'} {health_msg}")
        
        # GitHub sync status
        self.sync.status()
        
        # Evidence status
        print("\n📊 Evidence Status:")
        self.evidence.status()
        
        # Recent logs
        print("\n📝 Recent Activity:")
        self.show_logs(5)

def main():
    import sys
    deployer = AutoDeploy()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "--cycle":
            success = deployer.full_update_cycle()
            sys.exit(0 if success else 1)
            
        elif command == "--deploy":
            success = deployer.deploy_to_replit()
            sys.exit(0 if success else 1)
            
        elif command == "--setup":
            deployer.setup_automation()
            
        elif command == "--logs":
            limit = int(sys.argv[2]) if len(sys.argv) > 2 else 20
            deployer.show_logs(limit)
            
        elif command == "--status":
            deployer.status()
            
        elif command == "--health":
            healthy, msg = deployer.check_system_health()
            print(f"{'✅' if healthy else '❌'} {msg}")
            sys.exit(0 if healthy else 1)
            
    else:
        print("🚀 VCAT Auto-Deploy System")
        print("Commands:")
        print("  --cycle   Run full update cycle")
        print("  --deploy  Deploy to Replit")
        print("  --setup   Setup automation")
        print("  --logs [N] Show deployment logs")
        print("  --status  Show system status")
        print("  --health  Check system health")

if __name__ == "__main__":
    main()