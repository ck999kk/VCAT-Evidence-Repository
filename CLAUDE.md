# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## THINKING METHODOLOGY (MANDATORY)

**🧠 STANDARD COGNITIVE APPROACH:**
All Claude instances working on this project MUST use the following thinking methodology:

### **SEQUENCE THINK + ULTRATHINK + INTJ ANALYSIS**

1. **SEQUENCE THINKING:**
   - Break complex problems into logical sequential steps
   - Use sequential-thinking tool for multi-step analysis
   - Each thought builds on previous insights
   - Allow revision and course correction during analysis
   - Document decision-making process clearly

2. **ULTRATHINK APPROACH:**  
   - Apply 80:20 principle - focus on high-impact solutions
   - Think in terms of consequence chains and long-term effects
   - Consider multiple scenarios and failure modes
   - Prioritize practical implementation over theoretical perfection

3. **INTJ METHODOLOGY:**
   - Systems thinking - understand interconnected components
   - Evidence-based decision making
   - Strategic planning with clear objectives
   - Implementation-focused with measurable outcomes
   - Anticipate problems and prepare contingencies

**🎯 EXECUTION STANDARD:**
- Use TodoWrite tool to track multi-step tasks
- Apply consequence thinking before major changes
- Plan implementation steps before coding
- Test and verify solutions systematically
- Document decisions and reasoning for future reference

## Repository Overview

This is a **production VCAT Evidence Repository** containing a complete legal evidence management system for Victorian Civil and Administrative Tribunal cases.

**🏛️ SYSTEM COMPONENTS:**
- **634 legal documents** indexed and searchable
- **FastAPI production server** (main.py) with Swagger documentation
- **PostgreSQL database** with full-text search capabilities  
- **Docker deployment** ready for Render.com and local development
- **Court-ready export** functionality for evidence bundles
- **Web interface** for human and AI access

## Current State

**✅ PRODUCTION READY SYSTEM:**
- FastAPI server: `main.py` (20KB, multi-route API)
- Database: PostgreSQL with 634 documents, 114 emails
- Deployment: Docker + Render.com (srv-d26i9tmr433s73el0mfg)
- Documentation: Complete API docs at `/docs`
- Repository: https://github.com/ck999kk/VCAT-Evidence-Repository

**🔧 KEY FILES:**
- `Dockerfile` - Production container with Python 3.13 + FastAPI
- `requirements.txt` - Optimized dependencies (psycopg2-binary wheel fix)
- `main.py` - Complete API server (Search + Export + Web UI)
- `render.yaml` - Render.com deployment configuration
- `static/index.html` - Web interface for browser access

## API Endpoints

**🌐 LIVE SYSTEM:**
```
https://vcat-evidence-repository.onrender.com/
├── /                    → Web Interface + API access
├── /docs               → Swagger API Documentation
├── /health            → System status + database check
├── /search?q=query    → Full-text document search (634 docs)
├── /export/search     → Court-ready evidence bundles
├── /export/case-summary → Complete case overview
└── /export/legal-bundle → Top 25 evidence compilation
```

## Development Commands

**🐳 DOCKER (LOCAL TESTING):**
```bash
# Build and test locally (same as Render.com)
docker build -t vcat-evidence .
docker run -p 8080:8080 vcat-evidence

# Access: http://localhost:8080/docs
```

**🚀 DEPLOYMENT:**
```bash
# Push to trigger Render.com redeploy
git add .
git commit -m "Update message"
git push origin main
```

**🔍 DATABASE (LOCAL):**
```bash
# Start existing local system
cd vcat-ai-search && ./start.sh
# APIs available on ports 5004, 5005, 8080
```

## Case Information

**⚖️ VCAT CASES:** RT252398, R202518214, R202518589  
**🏠 PROPERTY:** 1803/243 Franklin Street, Melbourne  
**📅 TIMELINE:** February 2025 - August 2025  
**📋 DISPUTE:** Water damage, repairs, possession proceedings

## Working with This Repository

**🛡️ SECURITY & COMPLIANCE:**
- All evidence digitally verified with SHA256 checksums
- Chain of custody documented in `CHAIN_OF_CUSTODY.md`
- Professional legal exhibit classification system
- Australian Evidence Act 1995 compliant

**🤖 AI INTEGRATION:**
- OpenAPI/Swagger documentation for programmatic access
- CORS enabled for AI systems (GPT, Claude)
- JSON API responses with structured data
- Mobile-responsive web interface

**📋 DEVELOPMENT GUIDELINES:**
1. Use sequence thinking + ultrathink + INTJ methodology
2. Test locally with Docker before deploying
3. Monitor Render.com build logs for deployment issues
4. Update API documentation when adding endpoints
5. Maintain evidence integrity and legal compliance

---

**🎯 PROJECT STATUS:** Production system serving 634+ legal documents with court-ready export capabilities

**🔗 LIVE API:** https://vcat-evidence-repository.onrender.com/docs