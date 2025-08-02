#!/usr/bin/env python3
"""
VCAT Evidence Data Loader
Loads evidence files from VCAT_GMAIL_EVIDENCE and VCAT_NON_GMAIL_EVIDENCE into mygpt-vcat-db
"""

import os
import sys
import psycopg2
import hashlib
from pathlib import Path
from datetime import datetime
import email
import email.utils
from bs4 import BeautifulSoup
import re

# Database connection using mygpt-vcat-db container
DB_CONFIG = {
    'host': 'localhost',
    'database': 'vcat', 
    'user': 'vcat',
    'password': 'secret123',
    'port': 5432
}

def connect_db():
    """Connect to mygpt-vcat-db PostgreSQL"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return None

def parse_email_file(file_path):
    """Parse .eml file and extract metadata"""
    try:
        with open(file_path, 'rb') as f:
            msg = email.message_from_bytes(f.read())
        
        subject = msg.get('Subject', '')
        sender = msg.get('From', '')
        recipient = msg.get('To', '')
        date_str = msg.get('Date', '')
        
        # Parse date
        date_parsed = None
        if date_str:
            try:
                date_parsed = email.utils.parsedate_to_datetime(date_str)
            except:
                pass
        
        # Extract body content
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body += part.get_payload(decode=True).decode('utf-8', errors='ignore')
        else:
            body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
        
        return {
            'subject': subject,
            'sender': sender,
            'recipient': recipient,
            'date': date_parsed,
            'body': body
        }
    except Exception as e:
        print(f"❌ Error parsing email {file_path}: {e}")
        return None

def parse_html_file(file_path):
    """Parse HTML file and extract text content"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Extract title from filename if available
        title = file_path.stem
        
        # Extract text content
        text = soup.get_text(separator=' ', strip=True)
        
        # Try to extract date from filename
        date_match = re.search(r'(\d{8})', file_path.name)
        date_parsed = None
        if date_match:
            try:
                date_str = date_match.group(1)
                date_parsed = datetime.strptime(date_str, '%Y%m%d')
            except:
                pass
        
        return {
            'title': title,
            'content': text,
            'html_content': content,
            'date': date_parsed
        }
    except Exception as e:
        print(f"❌ Error parsing HTML {file_path}: {e}")
        return None

def calculate_file_hash(file_path):
    """Calculate SHA256 hash of file"""
    try:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception as e:
        print(f"❌ Error calculating hash for {file_path}: {e}")
        return None

def load_evidence_files():
    """Load all evidence files into database"""
    
    conn = connect_db()
    if not conn:
        return False
    
    cursor = conn.cursor()
    
    # Base directories
    base_dir = Path("/Users/chawakornkamnuansil/Desktop/ALL_FILES_COPY")
    gmail_dir = base_dir / "VCAT_GMAIL_EVIDENCE "
    non_gmail_dir = base_dir / "VCAT_NON_GMAIL_EVIDENCE"
    
    total_files = 0
    processed_files = 0
    
    print("🔄 Starting evidence data loading...")
    
    # Process Gmail Evidence (.eml files)
    eml_dir = gmail_dir / "All_Case_Parties_EML"
    if eml_dir.exists():
        print(f"📧 Processing Gmail evidence from {eml_dir}")
        for eml_file in eml_dir.glob("*.eml"):
            total_files += 1
            print(f"Processing: {eml_file.name}")
            
            # Parse email
            email_data = parse_email_file(eml_file)
            if not email_data:
                continue
            
            # Calculate file hash
            file_hash = calculate_file_hash(eml_file)
            if not file_hash:
                continue
            
            try:
                # Insert into evidence.emails table
                cursor.execute("""
                    INSERT INTO evidence.emails (
                        filename, file_path, file_hash, file_size,
                        subject, sender, recipient, email_date, body_text,
                        created_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (file_hash) DO NOTHING
                """, (
                    eml_file.name,
                    str(eml_file.relative_to(base_dir)),
                    file_hash,
                    eml_file.stat().st_size,
                    email_data['subject'],
                    email_data['sender'],
                    email_data['recipient'],
                    email_data['date'],
                    email_data['body'],
                    datetime.now()
                ))
                
                processed_files += 1
                
            except Exception as e:
                print(f"❌ Error inserting email {eml_file.name}: {e}")
                continue
    
    # Process Gmail Evidence (.html files)
    html_dir = gmail_dir / "All_Case_Parties_HTML"
    if html_dir.exists():
        print(f"🌐 Processing HTML evidence from {html_dir}")
        for html_file in html_dir.glob("*.html"):
            total_files += 1
            print(f"Processing: {html_file.name}")
            
            # Parse HTML
            html_data = parse_html_file(html_file)
            if not html_data:
                continue
            
            # Calculate file hash
            file_hash = calculate_file_hash(html_file)
            if not file_hash:
                continue
            
            try:
                # Insert into evidence.documents table
                cursor.execute("""
                    INSERT INTO evidence.documents (
                        filename, file_path, file_type, file_hash, file_size,
                        title, content, document_date, created_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (file_hash) DO NOTHING
                """, (
                    html_file.name,
                    str(html_file.relative_to(base_dir)),
                    'html',
                    file_hash,
                    html_file.stat().st_size,
                    html_data['title'],
                    html_data['content'],
                    html_data['date'],
                    datetime.now()
                ))
                
                processed_files += 1
                
            except Exception as e:
                print(f"❌ Error inserting HTML {html_file.name}: {e}")
                continue
    
    # Process PDF and other attachments
    if html_dir.exists():
        print(f"📎 Processing attachments from {html_dir}")
        for attachment_dir in html_dir.glob("Attachments*"):
            if attachment_dir.is_dir():
                for attachment_file in attachment_dir.rglob("*"):
                    if attachment_file.is_file():
                        total_files += 1
                        print(f"Processing: {attachment_file.name}")
                        
                        # Calculate file hash
                        file_hash = calculate_file_hash(attachment_file)
                        if not file_hash:
                            continue
                        
                        try:
                            # Insert into evidence.documents table
                            cursor.execute("""
                                INSERT INTO evidence.documents (
                                    filename, file_path, file_type, file_hash, file_size,
                                    title, created_at
                                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                                ON CONFLICT (file_hash) DO NOTHING
                            """, (
                                attachment_file.name,
                                str(attachment_file.relative_to(base_dir)),
                                attachment_file.suffix.lower(),
                                file_hash,
                                attachment_file.stat().st_size,
                                attachment_file.stem,
                                datetime.now()
                            ))
                            
                            processed_files += 1
                            
                        except Exception as e:
                            print(f"❌ Error inserting attachment {attachment_file.name}: {e}")
                            continue
    
    # Commit all changes
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"✅ Data loading complete!")
    print(f"📊 Total files found: {total_files}")
    print(f"📊 Files processed: {processed_files}")
    
    return True

def update_search_index():
    """Update full-text search index"""
    conn = connect_db()
    if not conn:
        return False
    
    cursor = conn.cursor()
    
    print("🔍 Updating full-text search indexes...")
    
    try:
        # Update document search vectors
        cursor.execute("""
            UPDATE evidence.documents 
            SET search_vector = to_tsvector('english', 
                COALESCE(title, '') || ' ' || 
                COALESCE(content, '') || ' ' || 
                COALESCE(filename, '')
            )
            WHERE search_vector IS NULL
        """)
        
        # Update email search vectors
        cursor.execute("""
            UPDATE evidence.emails 
            SET search_vector = to_tsvector('english',
                COALESCE(subject, '') || ' ' || 
                COALESCE(body_text, '') || ' ' || 
                COALESCE(sender, '') || ' ' ||
                COALESCE(recipient, '')
            )
            WHERE search_vector IS NULL
        """)
        
        conn.commit()
        print("✅ Search indexes updated successfully")
        
    except Exception as e:
        print(f"❌ Error updating search indexes: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()
    
    return True

def verify_data_loading():
    """Verify data was loaded correctly"""
    conn = connect_db()
    if not conn:
        return False
    
    cursor = conn.cursor()
    
    try:
        # Count documents
        cursor.execute("SELECT COUNT(*) FROM evidence.documents")
        doc_count = cursor.fetchone()[0]
        
        # Count emails
        cursor.execute("SELECT COUNT(*) FROM evidence.emails")
        email_count = cursor.fetchone()[0]
        
        print(f"📊 Verification Results:")
        print(f"   Documents loaded: {doc_count}")
        print(f"   Emails loaded: {email_count}")
        print(f"   Total evidence files: {doc_count + email_count}")
        
        # Test search functionality
        cursor.execute("""
            SELECT filename, title 
            FROM evidence.documents 
            WHERE search_vector @@ to_tsquery('english', 'water & damage')
            LIMIT 5
        """)
        search_results = cursor.fetchall()
        
        print(f"🔍 Sample search results for 'water damage':")
        for filename, title in search_results:
            print(f"   - {filename}: {title}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during verification: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    print("🏛️ VCAT Evidence Data Loader")
    print("=" * 50)
    
    # Load evidence files
    if not load_evidence_files():
        print("❌ Data loading failed")
        sys.exit(1)
    
    # Update search indexes
    if not update_search_index():
        print("❌ Search index update failed")
        sys.exit(1)
    
    # Verify loading
    if not verify_data_loading():
        print("❌ Data verification failed")
        sys.exit(1)
    
    print("🎉 VCAT evidence data loading completed successfully!")