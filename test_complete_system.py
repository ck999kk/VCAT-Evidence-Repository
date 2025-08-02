#!/usr/bin/env python3
"""
Complete System Test for VCAT Evidence Repository
Tests database connection, API functionality, and data integrity
"""

import psycopg2
import requests
import subprocess
import time
import threading
import sys
from datetime import datetime

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'database': 'vcat', 
    'user': 'vcat',
    'password': 'secret123',
    'port': 5432
}

def test_database_connection():
    """Test direct database connection and data integrity"""
    print("🔍 Testing Database Connection...")
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Basic connection test
        cursor.execute('SELECT current_database(), current_user, version()')
        db, user, version = cursor.fetchone()
        print(f"✅ Connected to database: {db} as {user}")
        print(f"   PostgreSQL version: {version.split(',')[0]}")
        
        # Check evidence data
        cursor.execute('SELECT COUNT(*) FROM evidence.documents')
        doc_count = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM evidence.emails') 
        email_count = cursor.fetchone()[0]
        print(f"📊 Evidence data: {doc_count} documents, {email_count} emails")
        
        # Test search capability
        cursor.execute("""
            SELECT filename, SUBSTRING(content, 1, 100) 
            FROM evidence.documents 
            WHERE content ILIKE '%water%damage%' 
            LIMIT 3
        """)
        results = cursor.fetchall()
        print(f"🔍 Sample search results ({len(results)} found):")
        for filename, preview in results:
            print(f"   - {filename}: {preview[:50]}...")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_api_endpoints():
    """Test FastAPI endpoints"""
    print("\n🌐 Testing API Endpoints...")
    
    base_url = "http://localhost:8080"
    
    # Start server in background
    def start_server():
        try:
            subprocess.run(['python3', 'main.py'], cwd='.', capture_output=True)
        except:
            pass
    
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    time.sleep(3)
    
    tests = [
        ("Health Check", "/health"),
        ("Search - water", "/search?q=water"),
        ("Search - VCAT", "/search?q=VCAT&limit=5"),
        ("Web Interface", "/"),
        ("API Documentation", "/docs"),
    ]
    
    results = []
    for test_name, endpoint in tests:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=5)
            if response.status_code == 200:
                print(f"✅ {test_name}: {response.status_code}")
                if endpoint == "/health":
                    data = response.json()
                    print(f"   Status: {data.get('status', 'unknown')}")
                    print(f"   Documents: {data.get('documents', 0)}")
                elif endpoint.startswith("/search"):
                    data = response.json()
                    results_count = len(data.get('results', []))
                    print(f"   Results: {results_count} found")
                    if results_count > 0:
                        first_result = data['results'][0]
                        print(f"   Sample: {first_result.get('filename', 'N/A')}")
                results.append((test_name, True))
            else:
                print(f"❌ {test_name}: HTTP {response.status_code}")
                results.append((test_name, False))
                
        except Exception as e:
            print(f"❌ {test_name}: {e}")
            results.append((test_name, False))
    
    return results

def test_system_performance():
    """Test system performance and response times"""
    print("\n⚡ Testing System Performance...")
    
    try:
        # Database query performance
        start_time = time.time()
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM evidence.documents WHERE content ILIKE \'%VCAT%\'')
        result = cursor.fetchone()[0]
        db_time = time.time() - start_time
        conn.close()
        
        print(f"✅ Database query: {db_time:.3f}s ({result} VCAT documents)")
        
        # API response time
        start_time = time.time()
        response = requests.get("http://localhost:8080/health", timeout=10)
        api_time = time.time() - start_time
        
        if response.status_code == 200:
            print(f"✅ API response: {api_time:.3f}s")
            return True
        else:
            print(f"❌ API performance test failed: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        return False

def generate_system_report():
    """Generate comprehensive system status report"""
    print("\n📋 System Status Report")
    print("=" * 50)
    
    # System info
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"System: VCAT Evidence Repository")
    print(f"Database: mygpt-vcat-db (PostgreSQL + pgvector)")
    print(f"API: FastAPI with Swagger documentation")
    
    # Evidence summary
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM evidence.documents')
        doc_count = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM evidence.emails') 
        email_count = cursor.fetchone()[0]
        
        # Get file type breakdown
        cursor.execute("""
            SELECT file_type, COUNT(*) 
            FROM evidence.documents 
            WHERE file_type IS NOT NULL 
            GROUP BY file_type 
            ORDER BY COUNT(*) DESC
        """)
        file_types = cursor.fetchall()
        
        print(f"\n📊 Evidence Statistics:")
        print(f"   Total Documents: {doc_count}")
        print(f"   Total Emails: {email_count}")
        print(f"   Total Evidence: {doc_count + email_count}")
        print(f"   File Types:")
        for file_type, count in file_types:
            print(f"     - {file_type}: {count}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Could not generate evidence statistics: {e}")
    
    print(f"\n🌐 API Endpoints Available:")
    print(f"   - Health Check: http://localhost:8080/health")
    print(f"   - Search: http://localhost:8080/search?q=<query>")
    print(f"   - Web Interface: http://localhost:8080/")
    print(f"   - API Docs: http://localhost:8080/docs")
    print(f"   - Export: http://localhost:8080/export/case-summary")

def main():
    """Run complete system test suite"""
    print("🏛️ VCAT Evidence Repository - Complete System Test")
    print("=" * 60)
    
    # Run all tests
    db_ok = test_database_connection()
    api_results = test_api_endpoints()
    perf_ok = test_system_performance()
    
    # Summary
    print("\n🎯 Test Summary:")
    print(f"   Database: {'✅ PASS' if db_ok else '❌ FAIL'}")
    print(f"   API Tests: {sum(1 for _, status in api_results if status)}/{len(api_results)} passed")
    print(f"   Performance: {'✅ PASS' if perf_ok else '❌ FAIL'}")
    
    # Generate report
    generate_system_report()
    
    # Final status
    all_passed = db_ok and all(status for _, status in api_results) and perf_ok
    if all_passed:
        print("\n🎉 ALL TESTS PASSED - System is fully operational!")
        print("\n✅ READY FOR USER:")
        print("   - VCAT evidence data loaded and searchable")
        print("   - API endpoints working correctly") 
        print("   - Web interface accessible")
        print("   - Database connection stable")
        return 0
    else:
        print("\n❌ SOME TESTS FAILED - Check errors above")
        return 1

if __name__ == "__main__":
    sys.exit(main())