# VCAT Evidence Repository - Replit Deployment

🏛️ **Complete VCAT Evidence Management System on Replit**

## 🚀 Quick Start

1. **Setup Database** (Run once):
   ```bash
   python3 setup_replit_db.py
   ```

2. **Start Server**:
   ```bash
   python3 main.py
   ```

3. **Access System**:
   - **Web Interface**: Click the URL in Replit output
   - **API Documentation**: Add `/docs` to the URL
   - **Health Check**: Add `/health` to the URL

## 📊 System Overview

- **154 Evidence Files** (40 documents + 114 emails)
- **Full-Text Search** with PostgreSQL
- **REST API** with FastAPI
- **Web Interface** for easy access
- **Export Functionality** for legal bundles

## 🔍 API Endpoints

- `GET /health` - System health check
- `GET /search?q=<query>` - Search evidence
- `GET /` - Web interface
- `GET /docs` - API documentation
- `GET /export/case-summary` - Export case summary
- `GET /export/legal-bundle` - Export legal evidence bundle

## 🎯 VCAT Cases Included

- **RT252398**: Residential Tenancy Dispute (Resolved)
- **R202518214**: Notice to Vacate Challenge (Resolved)  
- **R202518589**: Possession of Property (Active)

## 📈 Evidence Statistics

- **PDF Documents**: Legal orders, receipts, notices
- **Email Evidence**: 114 email communications
- **Photo Evidence**: Water damage documentation
- **Timeline**: February 2025 - August 2025
- **Property**: 1803/243 Franklin Street, Melbourne

## 🔧 Technical Details

- **Backend**: FastAPI (Python 3.11)
- **Database**: PostgreSQL 16 with full-text search
- **Storage**: 10GB Replit space
- **Deployment**: Replit Cloud Run
- **Port**: 8080 (mapped to 80 externally)

## 📝 Environment Variables

Already configured in `.replit` file:
- `DB_HOST=localhost`
- `DB_NAME=vcat`
- `DB_USER=vcat`
- `DB_PASSWORD=secret123`
- `DB_PORT=5432`

## 🛠️ Troubleshooting

### Database Issues
```bash
# Reset database
python3 setup_replit_db.py
```

### Server Issues
```bash
# Check logs
python3 main.py
```

### Search Not Working
```bash
# Verify data
python3 -c "
import psycopg2
conn = psycopg2.connect(host='localhost', database='vcat', user='vcat', password='secret123')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM evidence.documents')
print(f'Documents: {cursor.fetchone()[0]}')
cursor.execute('SELECT COUNT(*) FROM evidence.emails')
print(f'Emails: {cursor.fetchone()[0]}')
conn.close()
"
```

## 📋 File Structure

```
VCAT-Evidence-Repository/
├── main.py                 # FastAPI server
├── requirements.txt        # Python dependencies
├── setup_replit_db.py     # Database setup script
├── vcat_database_backup.dump # Database backup
├── .replit                # Replit configuration
├── replit.nix            # Nix dependencies
└── static/               # Web interface files
```

## 🎉 Success Indicators

When setup is complete, you should see:
- ✅ PostgreSQL running
- ✅ Database restored with 154 evidence files
- ✅ API server running on port 8080
- ✅ Web interface accessible
- ✅ Search functionality working

---

**🏛️ Professional Legal Evidence Management System**  
**Ready for VCAT Tribunal Proceedings**