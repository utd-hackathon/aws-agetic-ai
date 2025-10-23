"""Simple system test script"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_system():
    print("🧪 Testing UTD Career Guidance AI System")
    print("=" * 60)
    
    # Test 1: Health check
    print("\n1️⃣ Testing Health Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Server is healthy")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        print("   Please start the server first: python start_server.py")
        return
    
    # Test 2: Career guidance (main feature)
    print("\n2️⃣ Testing Career Guidance...")
    test_cases = [
        {"query": "I want to become a Financial Analyst", "location": "Dallas, TX"},
        {"query": "I want to become a Data Scientist", "location": "Dallas, TX"},
        {"query": "I want to become a Neuro Scientist", "location": "Dallas, TX"},
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n   Test {i}: {test_case['query']}")
        try:
            response = requests.post(
                f"{BASE_URL}/api/career-guidance",
                json=test_case,
                timeout=30
            )
            if response.status_code == 200:
                data = response.json()
                courses = data.get('course_recommendations', [])
                job_market = data.get('job_market_analysis', {})
                
                print(f"   ✅ Success!")
                print(f"      - Courses recommended: {len(courses)}")
                if courses:
                    print(f"      - Top course: {courses[0].get('course_code', 'N/A')} - {courses[0].get('title', 'N/A')}")
                print(f"      - Jobs analyzed: {job_market.get('total_jobs', 0)}")
                print(f"      - Trending skills: {', '.join(job_market.get('trending_skills', [])[:3])}")
            else:
                print(f"   ❌ Failed: {response.status_code}")
                print(f"      {response.text[:200]}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Test 3: Course search
    print("\n3️⃣ Testing Course Search...")
    try:
        response = requests.post(
            f"{BASE_URL}/course-search",
            json={"query": "neuroscience"},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            courses = data.get('courses', [])
            print(f"   ✅ Found {len(courses)} courses")
            if courses:
                print(f"      Example: {courses[0].get('course_code', 'N/A')} - {courses[0].get('title', 'N/A')}")
        else:
            print(f"   ❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Job market analysis
    print("\n4️⃣ Testing Job Market Analysis...")
    try:
        response = requests.post(
            f"{BASE_URL}/job-market",
            json={"job_title": "Software Engineer", "location": "Dallas, TX", "limit": 2},
            timeout=15
        )
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Job analysis complete")
            print(f"      - Jobs found: {data.get('job_count', 0)}")
            print(f"      - Avg salary: ${data.get('salaries', {}).get('overall_average', 0):,.0f}")
        else:
            print(f"   ❌ Failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ System test complete!")
    print("\n📝 Next steps:")
    print("   - Check API docs: http://127.0.0.1:8000/docs")
    print("   - Read SETUP.md for detailed information")

if __name__ == "__main__":
    test_system()

