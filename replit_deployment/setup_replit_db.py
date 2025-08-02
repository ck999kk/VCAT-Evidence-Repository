#!/usr/bin/env python3
"""
Replit Database Setup for VCAT Evidence Repository
Sets up PostgreSQL database and loads evidence data on Replit
"""

import os
import subprocess
import psycopg2
import sys
from pathlib import Path

def setup_postgresql():
    """Initialize PostgreSQL on Replit"""
    print("🔧 Setting up PostgreSQL on Replit...")
    
    # Start PostgreSQL service
    try:
        subprocess.run(['pg_ctl', '-D', '/tmp/postgresql', 'start'], check=True)
        print("✅ PostgreSQL started")
    except subprocess.CalledProcessError:
        # Initialize database if doesn't exist
        try:
            subprocess.run(['initdb', '-D', '/tmp/postgresql'], check=True)
            subprocess.run(['pg_ctl', '-D', '/tmp/postgresql', 'start'], check=True)
            print("✅ PostgreSQL initialized and started")
        except Exception as e:
            print(f"❌ PostgreSQL setup failed: {e}")
            return False
    
    return True

def create_database_and_user():
    """Create VCAT database and user"""
    print("🏗️ Creating database and user...")
    
    try:
        # Connect as default user to create database
        conn = psycopg2.connect(
            host='localhost',
            database='postgres',
            user=os.getenv('USER', 'runner'),
            port=5432
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Create user and database
        cursor.execute("CREATE USER vcat WITH PASSWORD 'secret123';")
        cursor.execute("CREATE DATABASE vcat OWNER vcat;")
        cursor.execute("GRANT ALL PRIVILEGES ON DATABASE vcat TO vcat;")
        
        cursor.close()
        conn.close()
        print("✅ Database and user created")
        return True
        
    except psycopg2.Error as e:
        if "already exists" in str(e):
            print("✅ Database and user already exist")
            return True
        else:
            print(f"❌ Database creation failed: {e}")
            return False

def restore_database():
    """Restore database from backup"""
    print("📊 Restoring database from backup...")
    
    backup_file = Path("vcat_database_backup.dump")
    if not backup_file.exists():
        print("❌ Backup file not found")
        return False
    
    try:
        # Restore using pg_restore
        subprocess.run([
            'pg_restore',
            '-h', 'localhost',
            '-U', 'vcat',
            '-d', 'vcat',
            '--no-owner',
            '--no-privileges',
            str(backup_file)
        ], check=True, env={**os.environ, 'PGPASSWORD': 'secret123'})
        
        print("✅ Database restored successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Database restore failed: {e}")
        return False

def verify_data():
    """Verify data was loaded correctly"""
    print("🔍 Verifying data...")
    
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='vcat',
            user='vcat',
            password='secret123',
            port=5432
        )
        cursor = conn.cursor()
        
        # Count documents and emails
        cursor.execute("SELECT COUNT(*) FROM evidence.documents")
        doc_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM evidence.emails")
        email_count = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        print(f"✅ Verification complete:")
        print(f"   📄 Documents: {doc_count}")
        print(f"   📧 Emails: {email_count}")
        print(f"   📊 Total evidence: {doc_count + email_count}")
        
        return doc_count > 0 or email_count > 0
        
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🏛️ VCAT Evidence Repository - Replit Setup")
    print("=" * 50)
    
    # Setup steps
    if not setup_postgresql():
        sys.exit(1)
    
    if not create_database_and_user():
        sys.exit(1)
    
    if not restore_database():
        sys.exit(1)
    
    if not verify_data():
        sys.exit(1)
    
    print("\n🎉 Replit database setup completed successfully!")
    print("🌐 Ready to start the API server with: python3 main.py")

if __name__ == "__main__":
    main()