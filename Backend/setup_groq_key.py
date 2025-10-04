#!/usr/bin/env python3
"""
Quick setup script to configure your Groq API key
"""

import os
from pathlib import Path

def setup_groq_api_key():
    """Interactive setup for Groq API key"""
    
    print("🔧 Groq API Key Setup for Mental Wellness API")
    print("=" * 50)
    
    env_file = Path("app/.env")
    
    if not env_file.exists():
        print("❌ .env file not found at app/.env")
        print("Please run the main setup.py script first")
        return False
    
    # Read current .env file
    with open(env_file, 'r') as f:
        lines = f.readlines()
    
    # Check current Groq API key
    current_key = None
    for line in lines:
        if line.startswith('GROQ_API_KEY='):
            current_key = line.split('=', 1)[1].strip()
            break
    
    if current_key and current_key != 'your_groq_api_key_here':
        print(f"✅ Groq API key is already configured")
        print(f"Current key: {current_key[:8]}...{current_key[-4:]}")
        
        response = input("Do you want to update it? (y/N): ").lower()
        if response != 'y':
            return True
    
    print("\n📝 To get your Groq API key:")
    print("1. Go to https://console.groq.com/")
    print("2. Sign up or log in")
    print("3. Navigate to 'API Keys' section")
    print("4. Create a new API key")
    print("5. Copy the key (it starts with 'gsk_')")
    
    new_key = input("\n🔑 Enter your Groq API key: ").strip()
    
    if not new_key:
        print("❌ No API key entered")
        return False
    
    if not new_key.startswith('gsk_'):
        print("⚠️  Warning: Groq API keys usually start with 'gsk_'")
        response = input("Continue anyway? (y/N): ").lower()
        if response != 'y':
            return False
    
    # Update .env file
    updated_lines = []
    key_updated = False
    
    for line in lines:
        if line.startswith('GROQ_API_KEY='):
            updated_lines.append(f'GROQ_API_KEY={new_key}\n')
            key_updated = True
        else:
            updated_lines.append(line)
    
    if not key_updated:
        # Add the key if it doesn't exist
        updated_lines.append(f'\nGROQ_API_KEY={new_key}\n')
    
    # Write updated .env file
    with open(env_file, 'w') as f:
        f.writelines(updated_lines)
    
    print("✅ Groq API key updated successfully!")
    
    # Test the key
    print("\n🧪 Testing API key...")
    
    try:
        os.environ['GROQ_API_KEY'] = new_key
        from groq import Groq
        
        client = Groq(api_key=new_key)
        
        # Test call
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5
        )
        
        if response.choices:
            print("✅ API key is working!")
            print("🚀 You can now run: python test_groq_integration.py")
            return True
        else:
            print("❌ API key test failed - no response")
            return False
            
    except Exception as e:
        print(f"❌ API key test failed: {e}")
        return False

if __name__ == "__main__":
    success = setup_groq_api_key()
    
    if success:
        print("\n🎉 Setup complete!")
        print("\nNext steps:")
        print("1. Run: python test_groq_integration.py")
        print("2. Start the server: cd app && uvicorn main:app --reload")
        print("3. View API docs: http://localhost:8000/docs")
    else:
        print("\n❌ Setup failed. Please check your API key and try again.")