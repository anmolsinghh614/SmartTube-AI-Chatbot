#!/usr/bin/env python3
"""
Test script to verify the YouTube to Chatbot setup
"""

import sys
import importlib
from config import Config

def test_imports():
    """Test if all required packages can be imported"""
    required_packages = [
        'langchain',
        'openai',
        'streamlit',
        'streamlit_chat',
        'youtube_transcript_api',
        'chromadb',
        'scrapetube',
        're',
        'os'
    ]
    
    print("🔍 Testing package imports...")
    failed_imports = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError as e:
            print(f"❌ {package}: {e}")
            failed_imports.append(package)
    
    if failed_imports:
        print(f"\n❌ Failed to import: {', '.join(failed_imports)}")
        print("Please install missing packages: pip install -r requirements.txt")
        return False
    
    print("✅ All packages imported successfully!")
    return True

def test_config():
    """Test configuration settings"""
    print("\n🔧 Testing configuration...")
    
    try:
        # Test API key validation
        if Config.validate_api_key():
            print("✅ OpenAI API key is set and valid")
        else:
            print("⚠️  OpenAI API key not set or invalid")
            print("   Set OPENAI_API_KEY environment variable")
        
        # Test directory creation
        Config.create_directories()
        print("✅ Configuration directories created")
        
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_youtube_url_validation():
    """Test YouTube URL validation"""
    print("\n🔗 Testing YouTube URL validation...")
    
    import re
    
    test_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtu.be/dQw4w9WgXcQ",
        "youtube.com/watch?v=dQw4w9WgXcQ",
        "https://www.youtube.com/playlist?list=PL123",
        "https://www.google.com",
        "invalid-url"
    ]
    
    expected_results = [True, True, True, False, False, False]
    
    for url, expected in zip(test_urls, expected_results):
        result = bool(re.match(Config.YOUTUBE_URL_PATTERN, url))
        status = "✅" if result == expected else "❌"
        print(f"{status} {url}: {result} (expected {expected})")

def main():
    """Run all tests"""
    print("🧪 YouTube to Chatbot - Setup Test")
    print("=" * 50)
    
    # Test imports
    if not test_imports():
        sys.exit(1)
    
    # Test configuration
    if not test_config():
        sys.exit(1)
    
    # Test URL validation
    test_youtube_url_validation()
    
    print("\n" + "=" * 50)
    print("🎉 Setup test completed!")
    print("\n📝 Next steps:")
    print("1. Set your OPENAI_API_KEY environment variable")
    print("2. Run 'streamlit run streamlitui.py' for web interface")
    print("3. Or run 'python chat_youtube.py' for command line")
    print("=" * 50)

if __name__ == "__main__":
    main() 