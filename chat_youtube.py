#!/usr/bin/env python3
"""
Simple YouTube Chat Script
A command-line interface for chatting with YouTube videos
"""

import os
import sys
from youtubequery import YoutubeQuery

def main():
    print("🎥 YouTube to Chatbot - Command Line Version")
    print("=" * 50)
    
    # Get OpenAI API key
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        api_key = input("Enter your OpenAI API key: ").strip()
        if not api_key:
            print("❌ OpenAI API key is required!")
            sys.exit(1)
    
    # Initialize YoutubeQuery
    try:
        youtube_query = YoutubeQuery(api_key)
        print("✅ API key validated successfully!")
    except ValueError as e:
        print(f"❌ {e}")
        sys.exit(1)
    
    # Get YouTube URL
    print("\n📹 Enter YouTube Video Details")
    print("-" * 30)
    url = input("YouTube URL: ").strip()
    
    if not url:
        print("❌ YouTube URL is required!")
        sys.exit(1)
    
    # Process the video
    print("\n🔄 Processing video...")
    result = youtube_query.ingest(url)
    
    if result != "Success":
        print(f"❌ {result}")
        sys.exit(1)
    
    print("✅ Video processed successfully!")
    print(f"📺 Video: {youtube_query.get_current_video()}")
    
    # Chat loop
    print("\n💬 Start chatting! (Type 'quit' to exit)")
    print("-" * 40)
    
    while True:
        try:
            question = input("\n🤔 Your question: ").strip()
            
            if question.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not question:
                print("❌ Please enter a question.")
                continue
            
            print("🤖 Thinking...")
            response = youtube_query.ask(question)
            print(f"💡 Answer: {response}")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()