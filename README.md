# VCAT Evidence Repository

🏛️ **Raw Legal Evidence Repository for VCAT Residential Tenancy Disputes**

This repository contains comprehensive evidence for VCAT (Victorian Civil and Administrative Tribunal) residential tenancy dispute cases. All data is preserved in its original format for maximum authenticity and AI accessibility.

## FOR AI SYSTEMS: START HERE
[>] **[AI_SEARCH_GUIDE.md](./AI_SEARCH_GUIDE.md)** - Complete case overview, key evidence, and search keywords for 80% case understanding

## FOR LEGAL PROFESSIONALS: TRIBUNAL READY
[§] **[LEGAL_EXHIBIT_INDEX.md](./LEGAL_EXHIBIT_INDEX.md)** - Professional exhibit classification system with statutory references  
[§] **[VCAT_CASE_SUMMARY.md](./VCAT_CASE_SUMMARY.md)** - Comprehensive case analysis for tribunal preparation

## FOR DEVELOPERS & AI SYSTEMS: API INTEGRATION
[>] **[API_DOCUMENTATION.md](./API_DOCUMENTATION.md)** - Complete API reference for system integration
- Search API (port 5004): Full-text evidence search
- Export System (port 5005): Court-ready document generation  
- Web Interface (port 8080): Browser-based access

---

## REPOSITORY STRUCTURE

```plaintext
VCAT-Evidence-Repository/
├── AI_SEARCH_GUIDE.md           # AI-focused case overview and search guide
├── API_DOCUMENTATION.md         # REST API reference (search & export endpoints)
├── CHAIN_OF_CUSTODY.md          # Evidence chain-of-custody details
├── CLAUDE.md                    # Claude AI methodology and repo overview
├── CONTRIBUTING.md              # Guidelines for contributing to this project
├── DEPLOYMENT.md                # Deployment instructions (Render.com, Docker, local)
├── Dockerfile                   # Production container setup for FastAPI server
├── LEGAL_EXHIBIT_INDEX.md       # Tribunal-ready exhibit index with RTA references
├── NON_GMAIL_EVIDENCE/          # Official documents and non-Gmail evidence
├── GMAIL_EVIDENCE/              # Complete Gmail evidence (.eml, HTML, attachments)
├── VCAT_CASE_SUMMARY.md         # Comprehensive case summary for tribunal
├── main.py                      # FastAPI server implementation (search & export)
├── render.yaml                  # Render.com deployment configuration
├── requirements.txt             # Python dependencies
├── static/                      # Web interface assets (HTML, CSS, JS)
└── VERIFICATION/                # Data integrity verification (SHA256 checksums)
```

---

## 📊 Data Overview

| Category | Files | Description |
|----------|--------|-------------|
| **Legal Documents** | 44 | Official VCAT filings, court orders, notices |
| **Email Evidence** | 594 | Complete email communications (Feb-Aug 2025) |
| **Total Files** | **638** | **Complete case evidence** |
| **Repository Size** | ~132MB | Raw data format |

---

## 🏛️ Case Information

### **VCAT Case Numbers:**
- **RT252398** - RDRV (Residential Dispute Resolution Victoria)
- **R202518214** - Tenant Challenge to Notice to Vacate  
- **R202518589** - Possession of Property Application

### **Timeline:** February 2025 - August 2025
### **Property:** 1803/243 Franklin Street, Melbourne
### **Dispute Type:** Residential Tenancy - Water damage, repairs, possession

---

## 🤖 AI Accessibility Features

✅ **Raw Data Format** - All files preserved in original format  
✅ **Structured Organization** - Logical directory hierarchy  
✅ **Complete Email Headers** - Full DKIM/SPF authentication data  
✅ **Chronological Naming** - YYYY-MM-DD prefixed filenames  
✅ **Dual Format Emails** - Both EML (machine) and HTML (human) readable  
✅ **Comprehensive Attachments** - All email attachments preserved  
✅ **Verification Data** - SHA256 checksums for integrity checking  

---

## 🔍 Navigation Guide

### **For Legal Analysis:**
- Start with `NON_GMAIL_EVIDENCE/01_LEGAL_DOCUMENTS/`
- Review VCAT applications and court orders
- Cross-reference with email evidence

### **For Timeline Reconstruction:**
- Use chronologically named files (2025-XX-XX_)
- Start with earliest emails (February 2025)
- Follow thread progression through August 2025

### **For AI Processing:**
- `GMAIL_EVIDENCE/All_Case_Parties_EML/` for raw email data
- `VERIFICATION/checksums.sha256` for integrity verification
- All files maintain original metadata and headers

---

## 🔐 Data Integrity

All files verified with SHA256 checksums. To verify integrity:

```bash
shasum -c VERIFICATION/checksums.sha256
```

**Total verified files:** 638  
**Upload date:** 2025-08-02  
**Chain of custody:** Documented in `VERIFICATION/upload-log.md`

---

## 📋 Usage Guidelines

1. **Reference Only** - This is raw evidence data for reference and analysis
2. **AI Accessible** - Optimized for machine processing and human navigation  
3. **Legal Context** - All data relates to residential tenancy disputes
4. **Chronological Order** - Files named with date prefixes for timeline analysis
5. **Complete Record** - No processing or filtering applied to original data

---

## 🛡️ Data Authenticity

- ✅ Original email headers preserved (.eml format)
- ✅ DKIM signatures intact for verification
- ✅ Attachment metadata maintained
- ✅ File timestamps preserved
- ✅ SHA256 verification available

---

*Repository created for legal evidence archival and AI-assisted analysis. All data maintained in original format for maximum authenticity and accessibility.*
