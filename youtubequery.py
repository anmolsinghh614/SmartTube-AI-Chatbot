import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.chains.question_answering import load_qa_chain
from langchain.document_loaders import YoutubeLoader
from langchain.llms import OpenAI
from langchain.docstore.document import Document
from youtube_transcript_api import NoTranscriptFound, TranscriptsDisabled
import re

class YoutubeQuery:
    def __init__(self, openai_api_key=None) -> None:
        if not openai_api_key:
            raise ValueError("OpenAI API key is required")
        
        if not openai_api_key.startswith('sk-'):
            raise ValueError("Invalid OpenAI API key format")
            
        self.embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        os.environ["OPENAI_API_KEY"] = openai_api_key
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        self.llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
        self.chain = None
        self.db = None
        self.current_video_url = None

    def _validate_youtube_url(self, url: str) -> bool:
        """Validate if the URL is a valid YouTube URL"""
        youtube_regex = r'(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})'
        return bool(re.match(youtube_regex, url))

    def ask(self, question: str) -> str:
        """Ask a question about the loaded video"""
        if not question or not question.strip():
            return "Please provide a question to ask."
            
        if self.chain is None or self.db is None:
            return "Please add a video first before asking questions."
        
        try:
            docs = self.db.get_relevant_documents(question)
            if not docs:
                return "I couldn't find relevant information in the video to answer your question. Try asking something else."
            
            response = self.chain.run(input_documents=docs, question=question)
            return response if response else "I couldn't generate a response for your question. Please try rephrasing it."
            
        except Exception as e:
            return f"Error processing your question: {str(e)}"

    def ingest(self, url: str) -> str:
        """Load and process a YouTube video"""
        if not url or not url.strip():
            return "Please provide a valid YouTube URL."
            
        if not self._validate_youtube_url(url):
            return "Invalid YouTube URL format. Please provide a valid YouTube video URL."
        
        try:
            # Load the video transcript
            loader = YoutubeLoader.from_youtube_url(url, add_video_info=False)
            documents = loader.load()
            
            if not documents:
                return "No transcript found for this video. Please try a video with captions/transcripts."
            
            # Split documents for processing
            splitted_documents = self.text_splitter.split_documents(documents)
            
            if not splitted_documents:
                return "Failed to process video transcript. Please try another video."
            
            # Create vector store
            self.db = Chroma.from_documents(splitted_documents, self.embeddings).as_retriever()
            self.chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff")
            self.current_video_url = url
            
            return "Success"
            
        except NoTranscriptFound:
            return "This video doesn't have any transcripts available. Please try a video with captions."
        except TranscriptsDisabled:
            return "Transcripts are disabled for this video. Please try another video."
        except Exception as e:
            return f"Error processing video: {str(e)}"

    def forget(self) -> None:
        """Clear the current video data"""
        self.db = None
        self.chain = None
        self.current_video_url = None

    def get_current_video(self) -> str:
        """Get the currently loaded video URL"""
        return self.current_video_url or "No video loaded"

    def is_video_loaded(self) -> bool:
        """Check if a video is currently loaded"""
        return self.db is not None and self.chain is not None