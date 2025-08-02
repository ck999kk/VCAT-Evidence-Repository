#!/usr/bin/env python3
"""
Graceful startup for VCAT Evidence Repository on Replit
Handles database availability gracefully without failing deployment
"""

import os
import sys
import psycopg2
import subprocess
from pathlib import Path

def check_database_connection():
    """Check if database is available and accessible"""
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_NAME', 'vcat'),
            user=os.getenv('DB_USER', 'vcat'),
            password=os.getenv('DB_PASSWORD', 'secret123'),
            port=int(os.getenv('DB_PORT', 5432)),
            connect_timeout=5
        )
        cursor = conn.cursor()
        cursor.execute("SELECT 1;")
        cursor.close()
        conn.close()
        print("✅ Database connection successful")
        return True
    except Exception as e:
        print(f"⚠️ Database not available: {e}")
        return False

def try_backup_restore():
    """Attempt to restore from backup if available"""
    backup_file = Path(__file__).parent / 'vcat_database_backup.dump'
    
    if not backup_file.exists():
        print("⚠️ No backup file found")
        return False
    
    try:
        print("🔄 Attempting database restore from backup...")
        
        # Try to create database
        subprocess.run(['createdb', 'vcat'], check=False, capture_output=True)
        
        # Restore from backup
        result = subprocess.run([
            'pg_restore', '--clean', '--no-acl', '--no-owner', 
            '-d', 'vcat', str(backup_file)
        ], check=False, capture_output=True)
        
        if result.returncode == 0:
            print("✅ Backup restore successful")
            return True
        else:
            print(f"⚠️ Backup restore failed: {result.stderr.decode()}")
            return False
            
    except Exception as e:
        print(f"⚠️ Backup restore error: {e}")
        return False

def main():
    """Main startup sequence"""
    print("🚀 Starting VCAT Evidence Repository...")
    
    # Check if database is available
    if check_database_connection():
        print("🎉 Database ready - full functionality available")
        sys.exit(0)
    
    # Try to set up database
    try:
        from setup_replit_db import main as setup_db
        setup_db()
        if check_database_connection():
            print("🎉 Database setup successful")
            sys.exit(0)
    except Exception as e:
        print(f"⚠️ Database setup failed: {e}")
    
    # Try backup restore
    if try_backup_restore():
        if check_database_connection():
            print("🎉 Database restored from backup")
            sys.exit(0)
    
    # Continue without database
    print("⚠️ Continuing without database - limited functionality")
    print("📋 API will provide error messages for database-dependent endpoints")
    sys.exit(0)  # Don't fail deployment

if __name__ == "__main__":
    main()