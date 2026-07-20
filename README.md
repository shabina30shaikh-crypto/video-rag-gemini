# 🎬 Video RAG Chatbot with Gemini

An AI-powered video question-answering application built with Streamlit and Google's Gemini API.

The application allows users to upload videos and ask natural-language questions about their content. Gemini's multimodal capabilities analyze the video and generate context-aware responses based on the visual and temporal information in the video.

## 🚀 Features

- 📹 Upload videos in multiple formats
- 🤖 Ask natural-language questions about video content
- 🧠 Multimodal video understanding using Google Gemini
- 💬 Interactive chat interface
- 🔄 Maintains conversation history during the session
- ⚡ Video processing with progress feedback
- 🔐 API key entered securely at runtime
- 🖥️ Simple Streamlit web interface

## 🧠 How It Works

```text
Upload Video
     ↓
Video Upload to Gemini File API
     ↓
Video Processing
     ↓
User Asks a Question
     ↓
Gemini Multimodal Analysis
     ↓
Context-Aware AI Response
```
🛠️ Tech Stack
Python
Streamlit
Google Gemini API
Google Generative AI SDK
Python-dotenv
Pillow
⚙️ Installation
1. Clone the Repository
git clone https://github.com/shabina30shaikh-crypto/video-rag-gemini.git
cd video-rag-gemini
2. Create a Virtual Environment
python -m venv venv
3. Activate the Virtual Environment

Windows PowerShell:

.\venv\Scripts\Activate.ps1
4. Install Dependencies
pip install -r requirements.txt
🔑 Gemini API Key Setup
Create a Gemini API key using Google AI Studio.
Start the application.
Enter your API key in the application sidebar.

⚠️ Security Note: Never commit your actual API key to GitHub. Do not store API keys directly in source code.

▶️ Run the Application
streamlit run app.py

Then open the local URL displayed in the terminal:

http://localhost:8501
💬 Example Questions

After uploading a video, you can ask questions such as:

What is happening in this video?
Summarize the main events.
What objects can you see?
Describe the setting and environment.
What actions are taking place?
Explain the main content of the video.
What are the important events in this video?
🔧 Technical Details
Video Processing: Videos are uploaded and processed using the Gemini File API.
Multimodal AI: Gemini analyzes video content together with natural-language questions.
Session Management: Chat history and video context are maintained during the active session.
Supported Formats: MP4, AVI, MOV, MKV, and WEBM.
⚠️ Limitations
Processing time depends on video size and complexity.
Large videos may take longer to upload and process.
API usage limits depend on the Gemini API plan.
Some video formats may have compatibility limitations.
🐛 Troubleshooting
Upload Fails

Check the video format and file size.

Processing Takes Too Long

Large videos may require additional processing time.

API Errors

Verify that your Gemini API key is correct and has sufficient quota.

No Response

Try refreshing the application and uploading the video again.

🌟 Future Improvements
Support for additional video formats
Conversation memory across sessions
Video timestamp-based answers
Automatic video summarization
Multi-video question answering
Cloud deployment
Improved error handling
👩‍💻 Author

Shabina Shaikh

GitHub: https://github.com/shabina30shaikh-crypto