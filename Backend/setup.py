#!/usr/bin/env python3
"""
Setup script for Mental Wellness API - Groq Integration
Helps configure the environment and validate setup
"""

import os
import secrets
import base64
from pathlib import Path
from cryptography.fernet import Fernet


def create_env_file():
    """Create .env file with necessary configuration"""
    
    env_path = Path("app/.env")
    
    if env_path.exists():
        print("📄 .env file already exists")
        response = input("Do you want to overwrite it? (y/N): ").lower()
        if response != 'y':
            print("Keeping existing .env file")
            return
    
    print("🔧 Creating .env file...")
    
    # Generate secrets
    secret_key = secrets.token_urlsafe(32)
    fernet_key = Fernet.generate_key().decode()
    
    # Get Groq API key
    groq_api_key = input("\n🔑 Enter your Groq API Key (required): ").strip()
    if not groq_api_key:
        print("❌ Groq API Key is required!")
        return False
    
    # Optional configurations
    print("\n⚙️  Optional configurations (press Enter for defaults):")
    mongodb_url = input("MongoDB URL [mongodb://localhost:27017]: ").strip() or "mongodb://localhost:27017"
    redis_url = input("Redis URL [redis://localhost:6379/0]: ").strip() or "redis://localhost:6379/0"
    groq_model = input("Groq Model [mixtral-8x7b-32768]: ").strip() or "mixtral-8x7b-32768"
    
    env_content = f"""# ==========================
# FastAPI App Configuration
# ==========================
SECRET_KEY={secret_key}
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# ==========================
# MongoDB Configuration
# ==========================
MONGODB_URL={mongodb_url}
MONGODB_DB=mental_wellness

# ==========================
# Redis / Celery
# ==========================
REDIS_URL={redis_url}

# ==========================
# Encryption Key (Fernet)
# ==========================
FERNET_KEY={fernet_key}

# ==========================
# Groq API Configuration
# ==========================
GROQ_API_KEY={groq_api_key}
GROQ_MODEL={groq_model}
"""
    
    # Create app directory if it doesn't exist
    env_path.parent.mkdir(exist_ok=True)
    
    # Write .env file
    with open(env_path, 'w') as f:
        f.write(env_content)
    
    print(f"✅ .env file created at {env_path}")
    return True


def check_dependencies():
    """Check if required dependencies are installed"""
    
    print("\n📦 Checking dependencies...")
    
    required_packages = [
        "fastapi",
        "uvicorn", 
        "motor",
        "beanie",
        "groq",
        "pydantic",
        "cryptography",
        "python-jose",
        "passlib",
        "redis",
        "celery"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📥 Missing packages: {', '.join(missing_packages)}")
        print("Install with: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies installed")
    return True


def test_groq_connection():
    """Test Groq API connection"""
    
    print("\n🔌 Testing Groq API connection...")
    
    try:
        # Load environment
        env_path = Path("app/.env")
        if not env_path.exists():
            print("❌ .env file not found. Run setup first.")
            return False
        
        # Read GROQ_API_KEY from .env
        groq_api_key = None
        with open(env_path, 'r') as f:
            for line in f:
                if line.startswith('GROQ_API_KEY='):
                    groq_api_key = line.split('=', 1)[1].strip()
                    break
        
        if not groq_api_key:
            print("❌ GROQ_API_KEY not found in .env file")
            return False
        
        # Test connection
        from groq import Groq
        
        client = Groq(api_key=groq_api_key)
        
        # Simple test call
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": "Hello, test connection"}],
            max_tokens=10
        )
        
        if response.choices:
            print("✅ Groq API connection successful")
            return True
        else:
            print("❌ Groq API connection failed - no response")
            return False
            
    except Exception as e:
        print(f"❌ Groq API connection failed: {e}")
        return False


def check_services():
    """Check if required services are running"""
    
    print("\n🔧 Checking required services...")
    
    # Check MongoDB
    try:
        import pymongo
        client = pymongo.MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=2000)
        client.server_info()
        print("✅ MongoDB running")
        mongodb_ok = True
    except Exception:
        print("❌ MongoDB not running (start with: mongod)")
        mongodb_ok = False
    
    # Check Redis
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, db=0, socket_timeout=2)
        r.ping()
        print("✅ Redis running")
        redis_ok = True
    except Exception:
        print("❌ Redis not running (start with: redis-server)")
        redis_ok = False
    
    return mongodb_ok and redis_ok


def main():
    """Main setup function"""
    
    print("🚀 Mental Wellness API - Groq Setup")
    print("=" * 40)
    
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Step 1: Create .env file
    if not create_env_file():
        return
    
    # Step 2: Check dependencies
    if not check_dependencies():
        print("\n❌ Please install missing dependencies first")
        return
    
    # Step 3: Test Groq connection
    if not test_groq_connection():
        print("\n❌ Please check your Groq API key")
        return
    
    # Step 4: Check services
    services_ok = check_services()
    
    # Summary
    print("\n" + "=" * 40)
    print("📋 Setup Summary")
    print("=" * 40)
    print("✅ Environment configuration complete")
    print("✅ Dependencies installed")
    print("✅ Groq API connection working")
    
    if services_ok:
        print("✅ Required services running")
        print("\n🎉 Setup complete! You can now start the server:")
        print("   cd app && uvicorn main:app --reload")
    else:
        print("⚠️  Some services need to be started")
        print("\n📝 Next steps:")
        print("1. Start MongoDB: mongod")
        print("2. Start Redis: redis-server") 
        print("3. Start the server: cd app && uvicorn main:app --reload")
    
    print("\n📖 View API docs at: http://localhost:8000/docs")
    print("🧪 Run tests with: python test_groq_integration.py")


if __name__ == "__main__":
    main()