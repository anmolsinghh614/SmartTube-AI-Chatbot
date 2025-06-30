#!/usr/bin/env python3
"""
YouTube Video Summarizer
Summarize any YouTube video using AI
"""

import os
import sys
from langchain.document_loaders import YoutubeLoader
from langchain import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import CharacterTextSplitter
from youtube_transcript_api import NoTranscriptFound, TranscriptsDisabled
import re

def validate_youtube_url(url):
    """Validate if the URL is a valid YouTube URL"""
    youtube_regex = r'(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})'
    return bool(re.match(youtube_regex, url))

def main():
    print("📝 YouTube Video Summarizer")
    print("=" * 40)
    
    # Get OpenAI API key
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        api_key = input("Enter your OpenAI API key: ").strip()
        if not api_key:
            print("❌ OpenAI API key is required!")
            sys.exit(1)
    
    # Validate API key
    if not api_key.startswith('sk-'):
        print("❌ Invalid OpenAI API key format!")
        sys.exit(1)
    
    # Get YouTube URL
    print("\n📹 Enter YouTube Video Details")
    print("-" * 30)
    url = input("YouTube URL: ").strip()
    
    if not url:
        print("❌ YouTube URL is required!")
        sys.exit(1)
    
    if not validate_youtube_url(url):
        print("❌ Invalid YouTube URL format!")
        sys.exit(1)
    
    try:
        # Initialize OpenAI
        llm = OpenAI(temperature=0, openai_api_key=api_key)
        
        # Load video transcript
        print("\n🔄 Loading video transcript...")
        loader = YoutubeLoader.from_youtube_url(url, add_video_info=False)
        docs = loader.load()
        
        if not docs:
            print("❌ No transcript found for this video!")
            sys.exit(1)
        
        # Split documents
        print("📄 Processing transcript...")
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        split_docs = text_splitter.split_documents(docs)
        
        if not split_docs:
            print("❌ Failed to process transcript!")
            sys.exit(1)
        
        # Create summarization chain
        print("🤖 Generating summary...")
        chain = load_summarize_chain(llm, chain_type="map_reduce")
        summary = chain.run(split_docs)
        
        # Display results
        print("\n" + "=" * 50)
        print("📋 SUMMARY")
        print("=" * 50)
        print(summary)
        print("=" * 50)
        
        # Save summary to file
        save_option = input("\n💾 Save summary to file? (y/n): ").strip().lower()
        if save_option in ['y', 'yes']:
            filename = input("Enter filename (default: summary.txt): ").strip()
            if not filename:
                filename = "summary.txt"
            
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"YouTube Video Summary\n")
                    f.write(f"URL: {url}\n")
                    f.write(f"{'='*50}\n\n")
                    f.write(summary)
                print(f"✅ Summary saved to {filename}")
            except Exception as e:
                print(f"❌ Error saving file: {e}")
        
    except NoTranscriptFound:
        print("❌ This video doesn't have any transcripts available!")
    except TranscriptsDisabled:
        print("❌ Transcripts are disabled for this video!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()