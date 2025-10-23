"""Simple script to start the FastAPI server"""

import os
import sys

def main():
    print("🚀 Starting UTD Career Guidance AI System")
    print("=" * 60)
    print("📍 Server will run at: http://127.0.0.1:8000")
    print("📚 API Documentation: http://127.0.0.1:8000/docs")
    print("=" * 60)
    print()
    
    # Check if we're in the right directory
    if not os.path.exists("src"):
        print("❌ Error: Please run this script from the aws-agetic-ai directory")
        print("   cd aws-agetic-ai")
        print("   python start_server.py")
        sys.exit(1)
    
    # Check if requirements are installed
    try:
        import fastapi
        import uvicorn
        import boto3
        import selenium
    except ImportError as e:
        print(f"❌ Error: Missing dependencies. Please install requirements:")
        print(f"   pip install -r requirements.txt")
        print(f"   Missing: {e.name}")
        sys.exit(1)
    
    print("✅ All dependencies found")
    print("🔄 Starting server with auto-reload enabled...")
    print()
    
    # Start uvicorn
    os.system("uvicorn src.api.app:app --reload --host 127.0.0.1 --port 8000")

if __name__ == "__main__":
    main()

