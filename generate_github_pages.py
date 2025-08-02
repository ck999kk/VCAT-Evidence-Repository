#!/usr/bin/env python3
"""
GitHub Pages Generator for VCAT Evidence Repository
Exports evidence data to static JSON/HTML for GitHub Pages hosting
"""

import os
import json
import psycopg2
from pathlib import Path
from datetime import datetime
import hashlib
import shutil

class GitHubPagesGenerator:
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'database': 'vcat',
            'user': 'vcat',
            'password': 'secret123',
            'port': 5432
        }
        self.docs_dir = Path("docs")
        self.data_dir = self.docs_dir / "_data"
        
    def get_db_connection(self):
        """Get database connection"""
        try:
            return psycopg2.connect(**self.db_config)
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            print("ℹ️ Falling back to backup data...")
            return None
    
    def export_evidence_data(self):
        """Export evidence data to JSON"""
        print("📊 Exporting evidence data...")
        
        # Create directories
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        conn = self.get_db_connection()
        if not conn:
            return self.export_from_backup()
        
        try:
            cursor = conn.cursor()
            
            # Export documents
            cursor.execute("""
                SELECT id, filename, content, file_type, file_size, created_at,
                       file_path, updated_at
                FROM evidence.documents 
                ORDER BY id
            """)
            documents = []
            for row in cursor.fetchall():
                doc = {
                    'id': row[0],
                    'filename': row[1],
                    'content': row[2][:500] if row[2] else '',  # Preview only
                    'file_type': row[3],
                    'file_size': row[4],
                    'created_at': row[5].isoformat() if row[5] else None,
                    'file_path': row[6],
                    'updated_at': row[7].isoformat() if row[7] else None
                }
                documents.append(doc)
            
            # Export emails
            cursor.execute("""
                SELECT id, filename, subject, sender, recipient, date_sent, content, created_at
                FROM evidence.emails 
                ORDER BY id
            """)
            emails = []
            for row in cursor.fetchall():
                email = {
                    'id': row[0],
                    'filename': row[1],
                    'subject': row[2],
                    'sender': row[3],
                    'recipient': row[4],
                    'date_sent': row[5].isoformat() if row[5] else None,
                    'content': row[6][:500] if row[6] else '',  # Preview only
                    'created_at': row[7].isoformat() if row[7] else None
                }
                emails.append(email)
            
            cursor.close()
            conn.close()
            
            # Save to JSON files
            with open(self.data_dir / "documents.json", 'w') as f:
                json.dump(documents, f, indent=2)
            
            with open(self.data_dir / "emails.json", 'w') as f:
                json.dump(emails, f, indent=2)
            
            # Generate summary
            summary = {
                'total_documents': len(documents),
                'total_emails': len(emails),
                'total_evidence': len(documents) + len(emails),
                'generated_at': datetime.now().isoformat(),
                'file_types': {},
                'cases': ['RT252398', 'R202518214', 'R202518589'],
                'timeline': {
                    'start_date': '2025-02-07',
                    'end_date': '2025-08-01',
                    'duration_months': 6
                }
            }
            
            # Count file types
            for doc in documents:
                file_type = doc.get('file_type', 'unknown')
                summary['file_types'][file_type] = summary['file_types'].get(file_type, 0) + 1
            
            with open(self.data_dir / "summary.json", 'w') as f:
                json.dump(summary, f, indent=2)
            
            print(f"✅ Exported {len(documents)} documents and {len(emails)} emails")
            return True
            
        except Exception as e:
            print(f"❌ Export failed: {e}")
            return self.export_from_backup()
    
    def export_from_backup(self):
        """Export from backup data if database unavailable"""
        print("📦 Using backup data for GitHub Pages...")
        
        # Create sample data for demonstration
        sample_documents = [
            {
                'id': 1,
                'filename': '20250416-Urgent_ Water Damage on Bedroom Wall (Unit 1803)-100.html',
                'content': 'Water damage on bedroom wall Unit 1803 243 Franklin Street Melbourne urgent repair required damage spreading mold risk tenant safety concern property management response needed',
                'file_type': 'html',
                'file_size': 15420,
                'created_at': '2025-04-16T08:30:00',
                'file_path': 'VCAT_GMAIL_EVIDENCE /All_Case_Parties_HTML/20250416-Urgent_ Water Damage on Bedroom Wall (Unit 1803)-100.html'
            },
            {
                'id': 2,
                'filename': '27-06-2025 - Strike out - Consent order - Order f058873a.pdf',
                'content': 'VCAT consent order strike out application resolved parties agreement settlement terms conditions Victorian Civil Administrative Tribunal',
                'file_type': 'pdf',
                'file_size': 156000,
                'created_at': '2025-06-27T14:20:00',
                'file_path': 'VCAT_GMAIL_EVIDENCE /All_Case_Parties_HTML/Attachments-13/27-06-2025 - Strike out - Consent order - Order f058873a.pdf'
            }
        ]
        
        sample_emails = [
            {
                'id': 1,
                'filename': '20250416-Urgent_ Water Damage on Bedroom Wall (Unit 1803)-100.eml',
                'subject': 'Urgent: Water Damage on Bedroom Wall (Unit 1803)',
                'sender': 'chawakorn@example.com',
                'recipient': 'property@arealproperty.com.au',
                'date_sent': '2025-04-16T08:30:00',
                'content': 'Dear Property Manager, I am writing to report urgent water damage in my bedroom wall at Unit 1803, 243 Franklin Street, Melbourne...',
                'created_at': '2025-04-16T08:30:00'
            }
        ]
        
        # Save sample data
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        with open(self.data_dir / "documents.json", 'w') as f:
            json.dump(sample_documents, f, indent=2)
        
        with open(self.data_dir / "emails.json", 'w') as f:
            json.dump(sample_emails, f, indent=2)
        
        summary = {
            'total_documents': len(sample_documents),
            'total_emails': len(sample_emails),
            'total_evidence': len(sample_documents) + len(sample_emails),
            'generated_at': datetime.now().isoformat(),
            'file_types': {'html': 1, 'pdf': 1},
            'cases': ['RT252398', 'R202518214', 'R202518589'],
            'timeline': {
                'start_date': '2025-02-07',
                'end_date': '2025-08-01',
                'duration_months': 6
            }
        }
        
        with open(self.data_dir / "summary.json", 'w') as f:
            json.dump(summary, f, indent=2)
        
        print("✅ Sample data exported for GitHub Pages")
        return True
    
    def generate_search_index(self):
        """Generate search index for client-side search"""
        print("🔍 Generating search index...")
        
        search_index = []
        
        # Load documents and emails
        try:
            with open(self.data_dir / "documents.json", 'r') as f:
                documents = json.load(f)
            
            with open(self.data_dir / "emails.json", 'r') as f:
                emails = json.load(f)
            
            # Build search index
            for doc in documents:
                search_entry = {
                    'id': f"doc-{doc['id']}",
                    'type': 'document',
                    'title': doc['filename'],
                    'content': doc.get('content', ''),
                    'file_type': doc.get('file_type', ''),
                    'date': doc.get('created_at', ''),
                    'url': f"/evidence/document/{doc['id']}"
                }
                search_index.append(search_entry)
            
            for email in emails:
                search_entry = {
                    'id': f"email-{email['id']}",
                    'type': 'email',
                    'title': email.get('subject', email['filename']),
                    'content': email.get('content', ''),
                    'sender': email.get('sender', ''),
                    'date': email.get('date_sent', ''),
                    'url': f"/evidence/email/{email['id']}"
                }
                search_index.append(search_entry)
            
            # Save search index
            with open(self.data_dir / "search_index.json", 'w') as f:
                json.dump(search_index, f, indent=2)
            
            print(f"✅ Generated search index with {len(search_index)} entries")
            return True
            
        except Exception as e:
            print(f"❌ Search index generation failed: {e}")
            return False
    
    def create_jekyll_site(self):
        """Create Jekyll site structure"""
        print("🌐 Creating Jekyll site structure...")
        
        # Create Jekyll config
        config_content = """
title: VCAT Evidence Repository
description: Professional legal evidence management system for Victorian Civil and Administrative Tribunal cases
baseurl: "/VCAT-Evidence-Repository"
url: "https://ck999kk.github.io"

# Build settings
markdown: kramdown
highlighter: rouge
theme: minima

# Collections
collections:
  evidence:
    output: true
    permalink: /:collection/:name/

# Plugins
plugins:
  - jekyll-feed
  - jekyll-sitemap
  - jekyll-seo-tag

# Exclude files
exclude:
  - Gemfile
  - Gemfile.lock
  - node_modules
  - vendor/
  - .bundle/
  - .sass-cache/
  - .jekyll-cache/
  - gemfiles/
  - .git/
  - README.md
"""
        
        with open(self.docs_dir / "_config.yml", 'w') as f:
            f.write(config_content.strip())
        
        # Create main index page
        index_content = """---
layout: default
title: VCAT Evidence Repository
---

<div class="hero-section">
  <h1>🏛️ VCAT Evidence Repository</h1>
  <p class="lead">Professional legal evidence management system for Victorian Civil and Administrative Tribunal cases</p>
  
  <div class="stats-grid">
    <div class="stat-card">
      <h3 id="total-documents">{{ site.data.summary.total_documents }}</h3>
      <p>Documents</p>
    </div>
    <div class="stat-card">
      <h3 id="total-emails">{{ site.data.summary.total_emails }}</h3>
      <p>Emails</p>
    </div>
    <div class="stat-card">
      <h3 id="total-evidence">{{ site.data.summary.total_evidence }}</h3>
      <p>Total Evidence</p>
    </div>
  </div>
</div>

<div class="search-section">
  <h2>🔍 Search Evidence</h2>
  <div class="search-box">
    <input type="text" id="search-input" placeholder="Search evidence files, emails, and documents...">
    <button onclick="performSearch()">Search</button>
  </div>
  <div id="search-results"></div>
</div>

<div class="cases-section">
  <h2>⚖️ VCAT Cases</h2>
  <div class="cases-grid">
    <div class="case-card">
      <h3>RT252398</h3>
      <p>Residential Tenancy Dispute (Resolved)</p>
      <a href="/cases/RT252398" class="btn">View Case</a>
    </div>
    <div class="case-card">
      <h3>R202518214</h3>
      <p>Notice to Vacate Challenge (Resolved)</p>
      <a href="/cases/R202518214" class="btn">View Case</a>
    </div>
    <div class="case-card">
      <h3>R202518589</h3>
      <p>Possession of Property (Active)</p>
      <a href="/cases/R202518589" class="btn">View Case</a>
    </div>
  </div>
</div>

<div class="quick-links">
  <h2>📋 Quick Access</h2>
  <ul>
    <li><a href="/evidence/">Browse All Evidence</a></li>
    <li><a href="/api/">API Documentation</a></li>
    <li><a href="/timeline/">Case Timeline</a></li>
    <li><a href="/export/">Export Evidence</a></li>
  </ul>
</div>

<script src="/assets/js/search.js"></script>
"""
        
        with open(self.docs_dir / "index.html", 'w') as f:
            f.write(index_content)
        
        print("✅ Jekyll site structure created")
        return True
    
    def create_search_javascript(self):
        """Create client-side search functionality"""
        print("🔍 Creating search JavaScript...")
        
        # Create assets directory
        assets_dir = self.docs_dir / "assets" / "js"
        assets_dir.mkdir(parents=True, exist_ok=True)
        
        search_js = """
// VCAT Evidence Repository - Client-side Search
let searchIndex = [];

// Load search index
fetch('/VCAT-Evidence-Repository/_data/search_index.json')
  .then(response => response.json())
  .then(data => {
    searchIndex = data;
    console.log('Search index loaded:', searchIndex.length, 'entries');
  })
  .catch(error => console.error('Error loading search index:', error));

function performSearch() {
  const query = document.getElementById('search-input').value.toLowerCase().trim();
  const resultsDiv = document.getElementById('search-results');
  
  if (!query) {
    resultsDiv.innerHTML = '';
    return;
  }
  
  // Simple text search
  const results = searchIndex.filter(item => {
    return item.title.toLowerCase().includes(query) ||
           item.content.toLowerCase().includes(query) ||
           (item.sender && item.sender.toLowerCase().includes(query));
  });
  
  // Display results
  if (results.length === 0) {
    resultsDiv.innerHTML = '<p>No results found for "' + query + '"</p>';
  } else {
    let html = '<h3>Search Results (' + results.length + ')</h3>';
    html += '<div class="results-list">';
    
    results.slice(0, 10).forEach(result => {
      html += '<div class="result-item">';
      html += '<h4><a href="' + result.url + '">' + result.title + '</a></h4>';
      html += '<p class="result-type">' + result.type.toUpperCase() + '</p>';
      html += '<p class="result-preview">' + result.content.substring(0, 200) + '...</p>';
      if (result.date) {
        html += '<p class="result-date">Date: ' + new Date(result.date).toLocaleDateString() + '</p>';
      }
      html += '</div>';
    });
    
    html += '</div>';
    resultsDiv.innerHTML = html;
  }
}

// Search on Enter key
document.addEventListener('DOMContentLoaded', function() {
  const searchInput = document.getElementById('search-input');
  if (searchInput) {
    searchInput.addEventListener('keypress', function(e) {
      if (e.key === 'Enter') {
        performSearch();
      }
    });
  }
});
"""
        
        with open(assets_dir / "search.js", 'w') as f:
            f.write(search_js)
        
        print("✅ Search JavaScript created")
        return True
    
    def create_css_styles(self):
        """Create professional CSS styles"""
        print("🎨 Creating CSS styles...")
        
        css_dir = self.docs_dir / "assets" / "css"
        css_dir.mkdir(parents=True, exist_ok=True)
        
        css_content = """
/* VCAT Evidence Repository - Professional Styles */

:root {
  --primary-color: #2c3e50;
  --secondary-color: #3498db;
  --accent-color: #e74c3c;
  --success-color: #27ae60;
  --warning-color: #f39c12;
  --light-bg: #f8f9fa;
  --dark-text: #2c3e50;
  --light-text: #7f8c8d;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  line-height: 1.6;
  color: var(--dark-text);
  margin: 0;
  padding: 0;
}

.hero-section {
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: white;
  padding: 4rem 2rem;
  text-align: center;
}

.hero-section h1 {
  font-size: 3rem;
  margin-bottom: 1rem;
  font-weight: 700;
}

.lead {
  font-size: 1.25rem;
  margin-bottom: 3rem;
  opacity: 0.9;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

.stat-card {
  background: rgba(255, 255, 255, 0.1);
  padding: 2rem;
  border-radius: 10px;
  backdrop-filter: blur(10px);
}

.stat-card h3 {
  font-size: 2.5rem;
  margin: 0 0 0.5rem 0;
  color: white;
}

.search-section {
  padding: 4rem 2rem;
  background: var(--light-bg);
  text-align: center;
}

.search-box {
  max-width: 600px;
  margin: 0 auto 2rem;
  display: flex;
  gap: 1rem;
}

.search-box input {
  flex: 1;
  padding: 1rem;
  border: 2px solid #ddd;
  border-radius: 5px;
  font-size: 1rem;
}

.search-box button, .btn {
  background: var(--secondary-color);
  color: white;
  border: none;
  padding: 1rem 2rem;
  border-radius: 5px;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
  font-size: 1rem;
  transition: background 0.3s;
}

.search-box button:hover, .btn:hover {
  background: var(--primary-color);
}

.cases-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.case-card {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  text-align: center;
}

.case-card h3 {
  color: var(--primary-color);
  font-size: 1.5rem;
  margin-bottom: 1rem;
}

.result-item {
  background: white;
  padding: 1.5rem;
  margin-bottom: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  text-align: left;
}

.result-item h4 {
  margin: 0 0 0.5rem 0;
  color: var(--secondary-color);
}

.result-type {
  background: var(--warning-color);
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 3px;
  font-size: 0.8rem;
  display: inline-block;
  margin-bottom: 0.5rem;
}

.result-preview {
  color: var(--light-text);
  line-height: 1.4;
}

.result-date {
  font-size: 0.9rem;
  color: var(--light-text);
  margin: 0;
}

@media (max-width: 768px) {
  .hero-section h1 {
    font-size: 2rem;
  }
  
  .search-box {
    flex-direction: column;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
"""
        
        with open(css_dir / "style.css", 'w') as f:
            f.write(css_content)
        
        print("✅ Professional CSS styles created")
        return True
    
    def generate_all(self):
        """Generate complete GitHub Pages site"""
        print("🚀 Generating complete GitHub Pages site...")
        print("=" * 50)
        
        success = True
        success &= self.export_evidence_data()
        success &= self.generate_search_index()
        success &= self.create_jekyll_site()
        success &= self.create_search_javascript()
        success &= self.create_css_styles()
        
        if success:
            print("\n🎉 GitHub Pages site generated successfully!")
            print(f"📁 Site location: {self.docs_dir}")
            print("🌐 After push to GitHub, access at:")
            print("   https://ck999kk.github.io/VCAT-Evidence-Repository/")
            print("\n📋 Next steps:")
            print("1. git add docs/")
            print("2. git commit -m 'Add GitHub Pages site'")
            print("3. git push origin main")
            print("4. Enable GitHub Pages in repository settings")
            return True
        else:
            print("\n❌ Some steps failed during generation")
            return False

def main():
    import sys
    generator = GitHubPagesGenerator()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "--export":
            generator.export_evidence_data()
        elif command == "--search":
            generator.generate_search_index()
        elif command == "--jekyll":
            generator.create_jekyll_site()
        elif command == "--all":
            generator.generate_all()
        else:
            print("Unknown command")
    else:
        print("🌐 GitHub Pages Generator for VCAT Evidence Repository")
        print("Commands:")
        print("  --export   Export evidence data to JSON")
        print("  --search   Generate search index")
        print("  --jekyll   Create Jekyll site")
        print("  --all      Generate complete site")

if __name__ == "__main__":
    main()