# Chat-Youtube
Chat with any Youtube video using AI. 

Easily input the video url you'd like to chat with. Instant answers. Ask questions, extract information, and summarize documents with AI. Sources included.

## ✨ Features

- **🎥 Video Chat**: Chat with any YouTube video that has captions/transcripts
- **📺 Channel Chat**: Chat with all videos from a YouTube channel
- **📝 Video Summarization**: Generate AI-powered summaries of YouTube videos
- **🌐 Web Interface**: Beautiful Streamlit web application
- **💻 Command Line**: Simple command-line interface
- **🔒 Secure**: API key validation and error handling
- **⚡ Fast**: Efficient vector search and retrieval

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- OpenAI API key
- YouTube video with captions/transcripts

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Anil-matcha/Chat-Youtube.git
   cd Chat-Youtube
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set your OpenAI API key**
   ```bash
   export OPENAI_API_KEY="your-api-key-here"  # On Windows: set OPENAI_API_KEY=your-api-key-here
   ```

## 🎯 Usage

### Web Interface (Recommended)

Run the Streamlit web application:

```bash
streamlit run streamlitui.py
```

Then open your browser to `http://localhost:8501`

### Command Line Interface

#### Chat with a Single Video
```bash
python chat_youtube.py
```

#### Chat with a Channel
```bash
python chat_channel.py
```

#### Summarize a Video
```bash
python summarize_youtube.py
```

## 📁 Project Structure

```
Youtube-to-chatbot-main/
├── streamlitui.py          # Main Streamlit web application
├── youtubequery.py         # Core YouTube query functionality
├── chat_youtube.py         # Command-line video chat
├── chat_channel.py         # Command-line channel chat
├── summarize_youtube.py    # Video summarization tool
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🔧 Configuration

The application uses a configuration file (`config.py`) for centralized settings:

- **OpenAI Settings**: Model, temperature, API key validation
- **LangChain Settings**: Chunk size, overlap, token limits
- **Application Settings**: Debug mode, file paths

## 🛠️ Features & Improvements

### ✅ Fixed Issues
- Added missing dependencies (`scrapetube`, `streamlit-chat`)
- Improved error handling and validation
- Added input validation for URLs and API keys
- Enhanced user experience with better UI/UX
- Added comprehensive error messages
- Improved code organization and documentation

### 🆕 New Features
- **URL Validation**: Validates YouTube URLs before processing
- **API Key Validation**: Checks OpenAI API key format
- **Progress Indicators**: Shows processing status
- **File Saving**: Save summaries to files
- **Channel Processing**: Process entire YouTube channels
- **Better Error Messages**: Clear, helpful error messages
- **Configuration Management**: Centralized settings

### 🎨 UI/UX Improvements
- Modern Streamlit interface with emojis and icons
- Better visual feedback and status messages
- Improved chat interface with message history
- Helpful tooltips and instructions
- Responsive design elements

## 🚨 Troubleshooting

### Common Issues

1. **"No transcript found"**
   - Make sure the video has captions/transcripts enabled
   - Try a different video

2. **"Invalid API key"**
   - Check that your OpenAI API key starts with `sk-`
   - Ensure the key is valid and has sufficient credits

3. **"Invalid YouTube URL"**
   - Use the full YouTube URL (e.g., `https://www.youtube.com/watch?v=VIDEO_ID`)
   - Make sure the video is public and accessible

4. **Installation Issues**
   - Make sure you're using Python 3.8+
   - Try upgrading pip: `pip install --upgrade pip`
   - Install dependencies one by one if needed

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [LangChain](https://langchain.com/) for the AI framework
- [OpenAI](https://openai.com/) for the language models
- [Streamlit](https://streamlit.io/) for the web interface
- [YouTube Transcript API](https://github.com/jdepoix/youtube-transcript-api) for transcript extraction

## 🔗 Related Projects

- [Chat with PDF](https://github.com/Anil-matcha/ChatPDF)
- [Chat with Website](https://github.com/Anil-matcha/Website-to-Chatbot)
- [Chat with CSV](https://github.com/Anil-matcha/Chat-With-Excel)
- [ChatGPT in Discord](https://github.com/Anil-matcha/DiscordGPT)

## 📞 Support

- **Demo**: https://heybot.thesamur.ai/
- **Twitter**: [@matchaman11](https://twitter.com/matchaman11)
- **YouTube**: [Anil Chandra Naidu Matcha](https://www.youtube.com/@AnilChandraNaiduMatcha)

---

⭐ **Star this repo** to receive updates and show your support!

