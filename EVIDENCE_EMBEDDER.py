#!/usr/bin/env python3
"""
VCAT Evidence Repository - PDF Report Generator
Embeds evidence files directly into PDF reports for complete self-contained documentation
"""

import os
import base64
from pathlib import Path
import markdown
from weasyprint import HTML, CSS
from datetime import datetime

class EvidenceEmbedder:
    def __init__(self, evidence_dir="./"):
        self.evidence_dir = Path(evidence_dir)
        self.embedded_files = {}
        
    def embed_file_as_base64(self, file_path):
        """Convert file to base64 for embedding in PDF"""
        try:
            with open(file_path, 'rb') as f:
                file_data = f.read()
                b64_data = base64.b64encode(file_data).decode('utf-8')
                
                # Determine MIME type
                ext = file_path.suffix.lower()
                mime_types = {
                    '.pdf': 'application/pdf',
                    '.html': 'text/html',
                    '.jpeg': 'image/jpeg',
                    '.jpg': 'image/jpeg',
                    '.png': 'image/png',
                    '.txt': 'text/plain'
                }
                mime = mime_types.get(ext, 'application/octet-stream')
                
                return f"data:{mime};base64,{b64_data}"
        except Exception as e:
            return f"Error embedding {file_path}: {str(e)}"
    
    def create_embedded_pdf_report(self, output_file="VCAT_Evidence_Report.pdf"):
        """Generate complete PDF report with embedded evidence files"""
        
        # Read the evidence index
        with open(self.evidence_dir / "PDF_EVIDENCE_LINKS.md", 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add embedded file sections
        embedded_content = content + "\n\n---\n\n# 📎 EMBEDDED EVIDENCE FILES\n\n"
        
        # Key files to embed
        key_files = [
            "GMAIL_EVIDENCE/All_Case_Parties_HTML/20250416-Urgent_ Water Damage on Bedroom Wall (Unit 1803)-100.html",
            "GMAIL_EVIDENCE/All_Case_Parties_HTML/Attachments-13/27-06-2025 - Strike out - Consent order - Order f058873a.pdf",
            "GMAIL_EVIDENCE/All_Case_Parties_HTML/Attachments/Receipt # 91716.pdf",
            "GMAIL_EVIDENCE/All_Case_Parties_HTML/Attachments-28/IMG_0548.jpeg"
        ]
        
        for file_rel_path in key_files:
            file_path = self.evidence_dir / file_rel_path
            if file_path.exists():
                embedded_content += f"\n## 📄 {file_path.name}\n"
                embedded_content += f"**Path**: `{file_rel_path}`\n\n"
                
                if file_path.suffix.lower() in ['.jpeg', '.jpg', '.png']:
                    # Embed images directly
                    b64_data = self.embed_file_as_base64(file_path)
                    embedded_content += f'<img src="{b64_data}" style="max-width:100%; height:auto;" alt="{file_path.name}">\n\n'
                
                elif file_path.suffix.lower() == '.html':
                    # Include HTML content as text
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            html_content = f.read()
                            # Extract body content only
                            if '<body>' in html_content:
                                body_start = html_content.find('<body>') + 6
                                body_end = html_content.find('</body>')
                                body_content = html_content[body_start:body_end]
                                embedded_content += f"```html\n{body_content[:1000]}...\n```\n\n"
                    except:
                        embedded_content += f"*Could not embed HTML content*\n\n"
                
                else:
                    embedded_content += f"*File available at: {file_rel_path}*\n\n"
        
        # Convert to HTML
        html_content = markdown.markdown(embedded_content, extensions=['tables', 'fenced_code'])
        
        # Add CSS for professional PDF
        css_style = """
        <style>
        body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
        h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
        h2 { color: #34495e; border-bottom: 1px solid #bdc3c7; padding-bottom: 5px; }
        h3 { color: #7f8c8d; }
        code { background: #f8f9fa; padding: 2px 4px; border-radius: 3px; }
        pre { background: #f8f9fa; padding: 15px; border-radius: 5px; overflow-x: auto; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        img { max-width: 100%; height: auto; border: 1px solid #ddd; margin: 10px 0; }
        .evidence-file { background: #e8f5e8; padding: 10px; border-left: 4px solid #27ae60; margin: 10px 0; }
        </style>
        """
        
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>VCAT Evidence Repository Report</title>
            {css_style}
        </head>
        <body>
            <h1>🏛️ VCAT Evidence Repository</h1>
            <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>Total Files:</strong> 1,171 evidence documents</p>
            <p><strong>Cases:</strong> RT252398, R202518214, R202518589</p>
            <hr>
            {html_content}
        </body>
        </html>
        """
        
        # Generate PDF
        try:
            HTML(string=full_html).write_pdf(output_file)
            print(f"✅ PDF report generated: {output_file}")
            return True
        except Exception as e:
            print(f"❌ PDF generation failed: {str(e)}")
            return False

if __name__ == "__main__":
    embedder = EvidenceEmbedder("./")
    embedder.create_embedded_pdf_report("VCAT_Complete_Evidence_Report.pdf")