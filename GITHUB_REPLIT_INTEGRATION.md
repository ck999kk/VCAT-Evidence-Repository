# 🔗 GitHub-Replit Integration Guide

## 🎯 **COMPLETE INTEGRATION SYSTEM**

ระบบนี้รองรับการอัพเดตแบบอัตโนมัติจาก GitHub ไป Replit พร้อมฟังก์ชันการจัดการข้อมูล Evidence

---

## 📋 **FUNCTIONS ที่ต้องมีสำหรับ GitHub → Replit Integration**

### 🔄 **1. GitHub Sync Functions**
```python
github_replit_sync.py
├── GitHubReplitSync.get_latest_github_commit()     # ดึงข้อมูล commit ล่าสุด
├── GitHubReplitSync.check_for_updates()           # เช็คว่ามี updates หรือไม่
├── GitHubReplitSync.pull_from_github()            # Pull โค้ดจาก GitHub
├── GitHubReplitSync.sync_from_github()            # Sync แบบเต็มรูปแบบ
└── GitHubReplitSync.setup_auto_sync()             # ตั้งค่า auto-sync
```

### 📊 **2. Evidence Update Functions**
```python
evidence_updater.py
├── EvidenceUpdater.check_evidence_changes()       # เช็คการเปลี่ยนแปลงของ evidence
├── EvidenceUpdater.create_evidence_backup()       # สร้าง backup database
├── EvidenceUpdater.update_evidence_system()       # อัพเดตระบบ evidence
└── EvidenceUpdater.commit_changes_to_git()        # Commit ไป Git
```

### 🚀 **3. Auto-Deploy Functions**
```python
auto_deploy.py
├── AutoDeploy.full_update_cycle()                 # รันการอัพเดตแบบเต็มรูปแบบ
├── AutoDeploy.deploy_to_replit()                  # Deploy ไป Replit
├── AutoDeploy.check_system_health()               # เช็คสุขภาพระบบ
└── AutoDeploy.setup_automation()                  # ตั้งค่า automation
```

### 🌐 **4. Webhook Endpoints**
```python
webhook_endpoints.py
├── /webhook/github                                # GitHub webhook
├── /webhook/auto-deploy                           # Auto-deployment trigger
├── /webhook/evidence-update                       # Evidence update trigger
├── /system/status                                 # System status
└── /system/logs                                   # Deployment logs
```

---

## 🔧 **SETUP STEPS**

### **Step 1: Commit ทุกอย่างไป GitHub**
```bash
git add .
git commit -m "🔗 Complete GitHub-Replit integration system"
git push origin main
```

### **Step 2: Upload ไป Replit**
1. สร้าง Replit project ใหม่
2. Upload ทุกไฟล์จาก `replit_deployment/`
3. รัน setup script:
```bash
python3 setup_replit_db.py
```

### **Step 3: Setup GitHub Webhooks**
ใน GitHub repository settings:
1. ไปที่ **Settings → Webhooks**
2. เพิ่ม webhook URL: `https://your-replit-url.com/webhook/github`
3. เลือก events: **Push events**
4. Content type: **application/json**

### **Step 4: Test Integration**
```bash
# Test GitHub sync
python3 github_replit_sync.py --check

# Test evidence updates  
python3 evidence_updater.py --check

# Test auto-deployment
python3 auto_deploy.py --cycle
```

### **Step 5: Setup Automation**
```bash
# Setup cron jobs
python3 auto_deploy.py --setup

# Or use webhook for instant updates
curl -X POST https://your-replit-url.com/webhook/auto-deploy
```

---

## ⚡ **AUTOMATIC UPDATE WORKFLOW**

### 🔄 **Evidence Update → GitHub → Replit**

1. **Evidence Changes Detected**
   ```
   evidence_updater.py --check
   └── Scans VCAT_*_EVIDENCE folders for changes
   ```

2. **Update Database & Create Backup**
   ```
   evidence_updater.py --update
   ├── Loads new evidence into database
   ├── Creates new vcat_database_backup.dump
   └── Commits to GitHub
   ```

3. **GitHub Triggers Webhook**
   ```
   GitHub Push → /webhook/github
   └── Triggers Replit sync automatically
   ```

4. **Replit Updates Automatically**
   ```
   github_replit_sync.py --sync
   ├── Pulls latest code from GitHub
   ├── Updates database from backup
   └── Restarts API service
   ```

### 🕐 **Scheduled Updates**
```bash
# Auto-check every 15 minutes
*/15 * * * * python3 auto_deploy.py --cycle

# Evidence check every hour
0 * * * * python3 evidence_updater.py --check
```

---

## 📊 **MONITORING & STATUS**

### **Check System Status**
```bash
# Complete system status
curl https://your-replit-url.com/system/status

# Health check only
python3 auto_deploy.py --health

# View deployment logs
python3 auto_deploy.py --logs 10
```

### **GitHub Sync Status**
```bash
# Check for GitHub updates
python3 github_replit_sync.py --status

# Manual sync if needed
python3 github_replit_sync.py --sync
```

### **Evidence Status**
```bash
# Evidence system status
python3 evidence_updater.py --status

# Force evidence update
python3 evidence_updater.py --update
```

---

## 🔐 **SECURITY & PERMISSIONS**

### **Required Permissions**
- ✅ **GitHub**: Read repository, Write webhooks
- ✅ **Replit**: Database access, File system access
- ✅ **PostgreSQL**: Full database access for backups

### **Environment Variables** (Already configured)
```env
DB_HOST=localhost
DB_NAME=vcat
DB_USER=vcat
DB_PASSWORD=secret123
DB_PORT=5432
```

---

## 🎯 **USAGE SCENARIOS**

### **Scenario 1: เพิ่ม Evidence ใหม่**
1. เพิ่มไฟล์ใน `VCAT_*_EVIDENCE` folders
2. รัน: `python3 evidence_updater.py --update`
3. ระบบจะ auto-sync ไป Replit ภายใน 15 นาที

### **Scenario 2: แก้ไขโค้ด**
1. แก้ไขโค้ดใน local
2. `git commit && git push`
3. Replit จะอัพเดตทันทีผ่าน webhook

### **Scenario 3: Manual Deployment**
```bash
# Deploy everything manually
python3 auto_deploy.py --cycle
```

### **Scenario 4: Troubleshooting**
```bash
# Check system health
curl https://your-replit-url.com/system/status

# View recent logs
curl https://your-replit-url.com/system/logs
```

---

## 🎉 **FINAL RESULT**

✅ **Automatic Evidence Updates**  
✅ **GitHub → Replit Sync**  
✅ **Webhook Integration**  
✅ **Health Monitoring**  
✅ **Professional API System**  
✅ **154 Evidence Files Searchable**  

**🌐 Access**: `https://your-replit-url.com`  
**📚 API Docs**: `https://your-replit-url.com/docs`  
**📊 Status**: `https://your-replit-url.com/system/status`

---

**🏛️ Complete Professional VCAT Evidence Management System**  
**Ready for Tribunal Proceedings with Auto-Update Capability**