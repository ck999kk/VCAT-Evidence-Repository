# 🚀 VCAT Evidence Repository - Replit Deployment Instructions

## 📦 Package Ready for Upload

**Package Location**: `replit_deployment/` folder  
**Total Size**: 232KB (well under 10GB limit)  
**Contains**: Complete VCAT evidence system + database backup

## 🎯 Step-by-Step Deployment

### Step 1: Create New Replit Project
1. Go to [Replit.com](https://replit.com)
2. Click **"Create Repl"**
3. Choose **"Python"** template
4. Name: `vcat-evidence-repository`

### Step 2: Upload Files
1. **Delete** the default `main.py` in Replit
2. **Upload all files** from `replit_deployment/` folder:
   - Drag and drop the entire folder contents
   - Or use Replit's upload feature

### Step 3: Install Dependencies
```bash
# Replit will auto-detect requirements.txt
# If not, run manually:
pip install -r requirements.txt
```

### Step 4: Setup Database (Run Once)
```bash
python3 setup_replit_db.py
```

**Expected Output:**
```
🏛️ VCAT Evidence Repository - Replit Setup
==================================================
🔧 Setting up PostgreSQL on Replit...
✅ PostgreSQL started
🏗️ Creating database and user...
✅ Database and user created
📊 Restoring database from backup...
✅ Database restored successfully
🔍 Verifying data...
✅ Verification complete:
   📄 Documents: 40
   📧 Emails: 114
   📊 Total evidence: 154

🎉 Replit database setup completed successfully!
🌐 Ready to start the API server with: python3 main.py
```

### Step 5: Start the System
```bash
python3 main.py
```

### Step 6: Test Access
- **Web Interface**: Click the Replit preview URL
- **Health Check**: Add `/health` to URL
- **API Docs**: Add `/docs` to URL
- **Search Test**: Add `/search?q=water+damage` to URL

## ✅ Success Indicators

When deployment is successful, you'll see:
- 🟢 Replit shows "Running" status
- 🌐 Web interface loads correctly
- 📊 Health check shows 154 evidence files
- 🔍 Search returns relevant results
- 📋 API documentation accessible

## 🎛️ Environment Configuration

Already pre-configured in `.replit` file:
- PostgreSQL 16 enabled
- Python 3.11 environment
- Port 8080 mapped to external port 80
- Database credentials set

## 🔧 Troubleshooting

### If Database Setup Fails:
```bash
# Reset and retry
rm -rf /tmp/postgresql
python3 setup_replit_db.py
```

### If Server Won't Start:
```bash
# Check dependencies
pip install -r requirements.txt
python3 main.py
```

### If Search Doesn't Work:
```bash
# Verify database
python3 -c "
import psycopg2
conn = psycopg2.connect(host='localhost', database='vcat', user='vcat', password='secret123')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM evidence.documents')
print(f'Documents: {cursor.fetchone()[0]}')
"
```

## 📱 Access URLs

Once deployed, your Replit will provide:
- **Main URL**: `https://[project-name].[username].repl.co`
- **Web Interface**: Same as main URL
- **API Docs**: `[main-url]/docs`
- **Health Check**: `[main-url]/health`
- **Search API**: `[main-url]/search?q=<query>`

## 🎉 Final Result

You'll have a **complete cloud-hosted VCAT evidence management system** with:
- ✅ 154 evidence files searchable
- ✅ Professional web interface
- ✅ REST API with documentation
- ✅ Export functionality for legal bundles
- ✅ No local dependencies needed
- ✅ Accessible from anywhere

---

**🏛️ Ready for Professional VCAT Tribunal Use**