#!/usr/bin/env python3
"""
Webhook Endpoints for VCAT Evidence Repository
GitHub-Replit integration and auto-deployment
"""

from fastapi import Request, HTTPException
from datetime import datetime
import threading
import json
import logging

# Setup logging
logger = logging.getLogger(__name__)

def setup_webhook_endpoints(app):
    """Add webhook endpoints to FastAPI app"""
    
    @app.post("/webhook/github")
    async def github_webhook(request: Request):
        """GitHub webhook for instant updates"""
        try:
            payload = await request.json()
            
            # Verify it's a push to main branch
            if payload.get("ref") == "refs/heads/main":
                commit_info = {
                    'sha': payload.get('after', '')[:8],
                    'message': payload.get('head_commit', {}).get('message', 'No message'),
                    'author': payload.get('head_commit', {}).get('author', {}).get('name', 'Unknown'),
                    'timestamp': datetime.now().isoformat()
                }
                
                # Trigger sync in background
                def sync_task():
                    try:
                        from github_replit_sync import GitHubReplitSync
                        sync = GitHubReplitSync()
                        result = sync.sync_from_github()
                        logger.info(f"GitHub sync completed: {result}")
                    except Exception as e:
                        logger.error(f"GitHub sync failed: {e}")
                
                sync_thread = threading.Thread(target=sync_task, daemon=True)
                sync_thread.start()
                
                return {
                    "status": "sync_triggered",
                    "commit": commit_info,
                    "timestamp": datetime.now().isoformat()
                }
            
            return {"status": "ignored", "reason": "not_main_branch"}
            
        except Exception as e:
            logger.error(f"GitHub webhook error: {e}")
            return {"status": "error", "message": str(e)}

    @app.post("/webhook/auto-deploy")
    async def auto_deploy_webhook(request: Request):
        """Webhook for triggering auto-deployment"""
        try:
            # Trigger full deployment cycle in background
            def deploy_task():
                try:
                    from auto_deploy import AutoDeploy
                    deployer = AutoDeploy()
                    result = deployer.full_update_cycle()
                    logger.info(f"Auto-deploy completed: {result}")
                except Exception as e:
                    logger.error(f"Auto-deploy failed: {e}")
            
            deploy_thread = threading.Thread(target=deploy_task, daemon=True)
            deploy_thread.start()
            
            return {
                "status": "deployment_triggered",
                "timestamp": datetime.now().isoformat(),
                "message": "Full update cycle started in background"
            }
            
        except Exception as e:
            logger.error(f"Auto-deploy webhook error: {e}")
            return {"status": "error", "message": str(e)}

    @app.post("/webhook/evidence-update")
    async def evidence_update_webhook(request: Request):
        """Webhook for evidence data updates"""
        try:
            payload = await request.json()
            
            # Trigger evidence update in background
            def evidence_task():
                try:
                    from evidence_updater import EvidenceUpdater
                    updater = EvidenceUpdater()
                    result = updater.update_evidence_system()
                    logger.info(f"Evidence update completed: {result}")
                except Exception as e:
                    logger.error(f"Evidence update failed: {e}")
            
            evidence_thread = threading.Thread(target=evidence_task, daemon=True)
            evidence_thread.start()
            
            return {
                "status": "evidence_update_triggered",
                "timestamp": datetime.now().isoformat(),
                "message": "Evidence update started in background"
            }
            
        except Exception as e:
            logger.error(f"Evidence update webhook error: {e}")
            return {"status": "error", "message": str(e)}

    @app.get("/system/status")
    async def system_status():
        """Get comprehensive system status"""
        try:
            # Import here to avoid circular imports
            from auto_deploy import AutoDeploy
            import psycopg2
            
            deployer = AutoDeploy()
            
            # System health
            healthy, health_msg = deployer.check_system_health()
            
            # Database stats
            try:
                db_config = {
                    'host': 'localhost',
                    'database': 'vcat',
                    'user': 'vcat',
                    'password': 'secret123',
                    'port': 5432
                }
                conn = psycopg2.connect(**db_config)
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM evidence.documents")
                doc_count = cursor.fetchone()[0]
                cursor.execute("SELECT COUNT(*) FROM evidence.emails")
                email_count = cursor.fetchone()[0]
                cursor.close()
                conn.close()
                db_status = "connected"
            except Exception as e:
                doc_count = 0
                email_count = 0
                db_status = f"error: {e}"
            
            # GitHub version info
            try:
                from github_replit_sync import GitHubReplitSync
                sync = GitHubReplitSync()
                current_version = sync.get_current_version()
                latest_github = sync.get_latest_github_commit()
                up_to_date = (current_version and latest_github and 
                             current_version.get('sha') == latest_github.get('sha'))
            except Exception as e:
                current_version = None
                latest_github = None
                up_to_date = None
            
            return {
                "system_health": {
                    "status": "healthy" if healthy else "unhealthy",
                    "message": health_msg
                },
                "database": {
                    "status": db_status,
                    "documents": doc_count,
                    "emails": email_count,
                    "total_evidence": doc_count + email_count
                },
                "version": {
                    "current": current_version,
                    "latest_github": latest_github,
                    "up_to_date": up_to_date
                },
                "webhooks": {
                    "github": "/webhook/github",
                    "auto_deploy": "/webhook/auto-deploy",
                    "evidence_update": "/webhook/evidence-update"
                },
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Status check failed: {e}")
            raise HTTPException(status_code=500, detail=f"Status check failed: {str(e)}")

    @app.get("/system/logs")
    async def system_logs(limit: int = 20):
        """Get system deployment logs"""
        try:
            from pathlib import Path
            import json
            
            log_file = Path("deploy_log.json")
            if not log_file.exists():
                return {"logs": [], "message": "No logs found"}
            
            with open(log_file, 'r') as f:
                logs = json.load(f)
            
            # Return last N logs
            recent_logs = logs[-limit:] if len(logs) > limit else logs
            
            return {
                "logs": recent_logs,
                "total_logs": len(logs),
                "showing": len(recent_logs)
            }
            
        except Exception as e:
            logger.error(f"Could not fetch logs: {e}")
            raise HTTPException(status_code=500, detail=f"Could not fetch logs: {str(e)}")

    return app