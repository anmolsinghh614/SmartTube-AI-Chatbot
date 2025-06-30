#!/usr/bin/env python3
"""
YouTube Channel Chat
Chat with all videos from a YouTube channel
"""

import os
import sys
import scrapetube
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import YoutubeLoader
from youtube_transcript_api import NoTranscriptFound, TranscriptsDisabled
import re

def validate_channel_id(channel_id):
    """Validate if the channel ID format is correct"""
    # YouTube channel IDs are typically 24 characters starting with UC
    return bool(re.match(r'^UC[a-zA-Z0-9_-]{22}$', channel_id))

def main():
    print("📺 YouTube Channel Chat")
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
    
    # Get channel ID
    print("\n📹 Enter YouTube Channel Details")
    print("-" * 30)
    channel_id = input("Channel ID (e.g., UC03sxjXYe4mSLqr5etxOXGA): ").strip()
    
    if not channel_id:
        print("❌ Channel ID is required!")
        sys.exit(1)
    
    if not validate_channel_id(channel_id):
        print("❌ Invalid channel ID format!")
        print("Channel ID should be 24 characters starting with 'UC'")
        sys.exit(1)
    
    try:
        # Initialize components
        print("\n🔄 Initializing...")
        embeddings = OpenAIEmbeddings(openai_api_key=api_key)
        llm = OpenAI(temperature=0, openai_api_key=api_key)
        
        # Get channel videos
        print("📺 Fetching channel videos...")
        videos = list(scrapetube.get_channel(channel_id))
        
        if not videos:
            print("❌ No videos found for this channel!")
            sys.exit(1)
        
        print(f"✅ Found {len(videos)} videos")
        
        # Process videos
        pages = []
        processed_count = 0
        failed_count = 0
        
        print("\n🔄 Processing videos...")
        for i, v in enumerate(videos, 1):
            try:
                video_id = v['videoId']
                url = f"https://www.youtube.com/watch?v={video_id}"
                print(f"Processing video {i}/{len(videos)}: {url}")
                
                loader = YoutubeLoader.from_youtube_url(url, add_video_info=False)
                video_pages = loader.load_and_split()
                pages.extend(video_pages)
                processed_count += 1
                
            except NoTranscriptFound:
                print(f"⚠️  No transcript for video {i}")
                failed_count += 1
            except TranscriptsDisabled:
                print(f"⚠️  Transcripts disabled for video {i}")
                failed_count += 1
            except Exception as e:
                print(f"❌ Error processing video {i}: {e}")
                failed_count += 1
        
        if not pages:
            print("❌ No transcripts found for any videos in this channel!")
            sys.exit(1)
        
        print(f"\n✅ Successfully processed {processed_count} videos")
        if failed_count > 0:
            print(f"⚠️  Failed to process {failed_count} videos")
        
        # Create vector store
        print("\n🔄 Creating search index...")
        docsearch = Chroma.from_documents(pages, embeddings).as_retriever()
        chain = load_qa_chain(llm, chain_type="stuff")
        
        print("✅ Channel ready for chatting!")
        
        # Chat loop
        print("\n💬 Start chatting! (Type 'quit' to exit)")
        print("-" * 40)
        
        while True:
            try:
                query = input("\n🤔 Your question: ").strip()
                
                if query.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if not query:
                    print("❌ Please enter a question.")
                    continue
                
                print("🤖 Searching and thinking...")
                docs = docsearch.get_relevant_documents(query)
                
                if not docs:
                    print("❌ No relevant information found in the channel.")
                    continue
                
                output = chain.run(input_documents=docs, question=query)
                print(f"💡 Answer: {output}")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()