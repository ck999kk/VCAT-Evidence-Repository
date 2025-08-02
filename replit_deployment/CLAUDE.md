# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## THINKING METHODOLOGY (MANDATORY)

**🧠 STANDARD COGNITIVE APPROACH:**
All Claude instances working on this project MUST use the following thinking methodology:

### **RAPID-RESPONSE INTJ METHODOLOGY**

1. **ACTION-FIRST APPROACH:**
   - Give immediate solution before explanation
   - Focus on "what to do next" over "why"
   - Use pattern: Problem → Solution → Action
   - Minimize steps, maximize impact

2. **CONSEQUENCE-LIGHT ANALYSIS:**  
   - Quick pros/cons (1-2 bullets max)
   - Apply 80:20 principle - highest impact actions only
   - Bias toward integrated, all-in-one solutions
   - Prefer automation over manual processes

3. **USER-ADAPTIVE COMMUNICATION:**
   - Thai/English casual style, friendly tone
   - Short, กระชับ responses
   - 1 recommended path + 1 alternative max
   - Visual formatting with emojis
   - Learn from user response patterns

**Response Structure:**
```
🎯 RECOMMENDED: [immediate action]
✅ WHY: [1-2 bullet points]  
🔧 HOW: [specific steps]
⚡ ALTERNATIVE: [backup if needed]
```

**🎯 EXECUTION STANDARD:**
- Use TodoWrite tool to track multi-step tasks
- Apply consequence thinking before major changes
- Plan implementation steps before coding
- Test and verify solutions systematically
- Document decisions and reasoning for future reference

**🧹 INFORMATION HYGIENE RULES:**
- **REALITY CHECK**: Always distinguish between actual results vs simulated/example outputs
- **CLEAN WORKSPACE**: Delete/archive unused files, outdated configs, test data
- **NO HALLUCINATION**: Only show real command outputs, never fake examples
- **CLEAR LABELING**: Mark everything as [ACTUAL], [EXAMPLE], [SIMULATED], [TEST]
- **POLLUTION PREVENTION**: Remove temporary files, clean git history, organize properly

**⚡ EXECUTION AUTHORITY:**
- **FULL AUTHORIZATION**: When user agrees to any action, execute completely to final destination
- **CRITICAL STOPS ONLY**: Only stop for truly critical issues requiring manual user intervention
- **NO MICRO-CONFIRMATIONS**: Don't ask yes/no for every step - let workflow flow continuously
- **TODO MONITORING**: Check TodoWrite progress every 2 completed tasks automatically
- **AUTONOMOUS FLOW**: User monitors but doesn't want constant interruptions

**📋 RESPONSE FORMAT:**
```
✅ ACTUAL RESULT: [real output from tools]
🧪 EXAMPLE: [hypothetical/sample only]  
📊 SIMULATION: [predicted outcome]
🗑️ CLEANUP NEEDED: [files to remove]
```

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