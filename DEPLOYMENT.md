# VCAT Evidence Repository - Deployment Guide

## 🚀 Quick Deploy to Render.com

### Prerequisites
1. GitHub repository: `https://github.com/ck999kk/VCAT-Evidence-Repository`
2. Render.com account
3. PostgreSQL database (production instance; in-memory or demo mode not supported)

### 1. Deploy to Render (Automatic)
```bash
# Method 1: Use render.yaml (Recommended)
1. Push all files to GitHub
2. Connect Render to your GitHub repo
3. Render will auto-detect render.yaml and deploy

# Method 2: Manual Web Service
1. Go to Render.com dashboard
2. Click "New" → "Web Service"
3. Connect GitHub repo: VCAT-Evidence-Repository
4. Use these settings:
   - Environment: Docker
   - Port: 8080
```

### 2. Environment Variables (Render Dashboard)
```env
## 2. Environment Variables (Render Dashboard)
```env
# Service port
PORT=8080

# Database configuration
DB_HOST=<postgres-host>
DB_PORT=5432
DB_NAME=vcat
DB_USER=vcat
DB_PASSWORD=<your-db-password>
``` 
```

### 3. Access Your API
```
https://your-app-name.onrender.com
├── /                    - Web Interface
├── /docs               - Swagger Documentation
├── /health            - Health Check
├── /search?q=query    - Search Documents
└── /export/*          - Export Functions
```

## 🖥️ Local Development

### 1. Clone Repository
```bash
git clone https://github.com/ck999kk/VCAT-Evidence-Repository
cd VCAT-Evidence-Repository
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables
```bash
cp .env.example .env
# Edit .env with your database credentials
```

### 4. Run Locally
```bash
# Method 1: Direct Python
python main.py

# Method 2: Uvicorn
uvicorn main:app --reload --port 8080

# Method 3: Docker
docker build -t vcat-evidence .
docker run -p 8080:8080 vcat-evidence
```

### 5. Access Local API
```
http://localhost:8080
├── /docs              - Swagger Documentation
├── /health           - Health Check
├── /search?q=test    - Search API
└── /export/*         - Export Functions
```

## 🔧 Configuration Options

### Database Modes
1. **PostgreSQL (Production)** - Full database with 634 documents
2. **Demo Mode (Free Tier)** - Mock data for testing
3. **In-Memory (Development)** - Temporary data

### API Features
- ✅ **Search API** - Full-text document search
- ✅ **Export API** - Court-ready evidence bundles
- ✅ **Web Interface** - Browser-based access
- ✅ **Swagger Docs** - Auto-generated API documentation
- ✅ **Health Checks** - System monitoring
- ✅ **CORS Enabled** - Cross-origin requests
- ✅ **Mobile Responsive** - Mobile-friendly UI

## 🐳 Docker Commands

### Build & Run
```bash
# Build image
docker build -t vcat-evidence .

# Run container
docker run -p 8080:8080 \
  -e DB_HOST=your-db-host \
  -e DB_PASSWORD=your-password \
  vcat-evidence

# Run with environment file
docker run -p 8080:8080 --env-file .env vcat-evidence
```

### Docker Compose (Optional)
```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8080:8080"
    environment:
      - DB_HOST=postgres
      - DB_PASSWORD=your-password
    depends_on:
      - postgres
  
  postgres:
    image: postgres:16
    environment:
      POSTGRES_DB: vcat_evidence_db
      POSTGRES_PASSWORD: your-password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## 🔍 Testing Deployment

### Health Check
```bash
curl https://your-app.onrender.com/health
```

### Search Test
```bash
curl "https://your-app.onrender.com/search?q=water+damage&limit=5"
```

### Export Test
```bash
curl "https://your-app.onrender.com/export/case-summary" -o case_summary.html
```

## 🆘 Troubleshooting

### Common Issues
1. **Port conflicts** → Check PORT environment variable
2. **Database connection** → Verify DB_* environment variables
3. **Build failures** → Check Dockerfile and requirements.txt
4. **Static files missing** → Ensure static/ directory exists

### Render.com Specific
1. **Build timeout** → Optimize Dockerfile, use .dockerignore
2. **Memory limits** → Free tier has 512MB limit
3. **Cold starts** → Free tier sleeps after inactivity

### Logs & Debugging
```bash
# Local logs
python main.py  # See console output

# Render logs
# Go to Render dashboard → Service → Logs tab

# Docker logs
docker logs container-name
```

## 📊 Performance

### Free Tier Limits (Render.com)
- **Memory**: 512MB
- **CPU**: 0.5 cores
- **Storage**: 1GB
- **Bandwidth**: 100GB/month
- **Sleep**: After 15 minutes inactivity

### Optimization
- ✅ Single worker process
- ✅ Minimal Docker image
- ✅ Static file serving
- ✅ Database connection pooling
- ✅ Gzip compression (auto)

---

**🎯 Quick Start**: Push to GitHub → Connect Render → Deploy automatically with `render.yaml`

**📚 Full API Docs**: Visit `/docs` after deployment for interactive Swagger documentation

**🔗 GitHub**: https://github.com/ck999kk/VCAT-Evidence-Repository
