import streamlit as st
from google import genai
import os
import tempfile
import time
from pathlib import Path
import mimetypes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Video RAG with Gemini",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ===========================
#   Video Processing Class
# ===========================
class VideoProcessor:

    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)

    def upload_video(self, video_path, display_name=None):
        """Upload video to Gemini File API"""
        try:
            video_file = self.client.files.upload(
                file=video_path,
                config={
                    "display_name": display_name or "uploaded_video"
                }
            )

            return video_file

        except Exception as e:
            st.error(f"Error uploading video: {str(e)}")
            return None

    def wait_for_file_processing(self, video_file):
        """Wait for video processing"""

        try:
            while video_file.state.name == "PROCESSING":
                time.sleep(2)
                video_file = self.client.files.get(
                    name=video_file.name
                )

            if video_file.state.name == "FAILED":
                raise ValueError("Video processing failed")

            return video_file

        except Exception as e:
            st.error(f"Error processing video: {str(e)}")
            return None

    def chat_with_video(self, video_file, prompt):
        """Generate response based on video"""

        try:
            response = self.client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=[
                    video_file,
                    prompt
                ]
            )

            return response.text

        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
            return None


# ===========================
#   Helper Functions
# ===========================

def is_video_file(file):

    if file is None:
        return False

    mime_type, _ = mimetypes.guess_type(file.name)

    return mime_type and mime_type.startswith("video/")


def get_file_size_mb(file):

    return len(file.getvalue()) / (1024 * 1024)


def reset_chat():

    st.session_state.messages = []

    if st.session_state.video_file is not None:

        try:
            st.session_state.video_processor.client.files.delete(
                name=st.session_state.video_file.name
            )

        except Exception:
            pass

        st.session_state.video_file = None

    st.session_state.video_processor = None
    st.session_state.video_name = None


def display_video(video_bytes, video_name):

    st.markdown(f"### 🎬 {video_name}")

    st.video(video_bytes)


# ===========================
#   Session State
# ===========================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "video_file" not in st.session_state:
    st.session_state.video_file = None

if "video_processor" not in st.session_state:
    st.session_state.video_processor = None

if "video_name" not in st.session_state:
    st.session_state.video_name = None


# ===========================
#   Sidebar
# ===========================

with st.sidebar:

    st.header("🔑 API Configuration")

    default_api_key = os.getenv("GEMINI_API_KEY", "")

    api_key = st.text_input(
        "Gemini API Key",
        value=default_api_key,
        type="password"
    )

    if api_key:

        if (
            st.session_state.video_processor is None
            or st.session_state.video_processor.client is None
        ):
            st.session_state.video_processor = VideoProcessor(api_key)

    st.markdown("---")

    st.header("📹 Upload Video")

    uploaded_file = st.file_uploader(
        "Choose a video file",
        type=["mp4", "avi", "mov", "mkv", "webm"]
    )

    if uploaded_file is not None:

        if not is_video_file(uploaded_file):

            st.error("Please upload a valid video file.")

        else:

            file_size = get_file_size_mb(uploaded_file)

            st.info(f"File size: {file_size:.2f} MB")

            if file_size > 100:

                st.warning(
                    "Large files may take longer to process."
                )

            if (
                st.session_state.video_file is None
                or st.session_state.video_name != uploaded_file.name
            ):

                if st.session_state.video_processor is None:

                    st.error(
                        "Please enter your Gemini API key first."
                    )

                else:

                    with st.spinner(
                        "Uploading and processing video..."
                    ):

                        with tempfile.NamedTemporaryFile(
                            delete=False,
                            suffix=Path(
                                uploaded_file.name
                            ).suffix
                        ) as tmp_file:

                            tmp_file.write(
                                uploaded_file.getvalue()
                            )

                            tmp_file_path = tmp_file.name

                        try:

                            video_file = (
                                st.session_state
                                .video_processor
                                .upload_video(
                                    tmp_file_path,
                                    uploaded_file.name
                                )
                            )

                            if video_file:

                                processed_file = (
                                    st.session_state
                                    .video_processor
                                    .wait_for_file_processing(
                                        video_file
                                    )
                                )

                                if processed_file:

                                    st.session_state.video_file = (
                                        processed_file
                                    )

                                    st.session_state.video_name = (
                                        uploaded_file.name
                                    )

                                    st.session_state.messages = []

                                    st.success(
                                        "✅ Video processed successfully!"
                                    )

                        finally:

                            try:

                                os.unlink(tmp_file_path)

                            except Exception:

                                pass

            if st.session_state.video_file:

                display_video(
                    uploaded_file.getvalue(),
                    uploaded_file.name
                )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

        if st.button("🗑️ Clear Chat"):

            st.session_state.messages = []

            st.rerun()

    with col2:

        if st.button("🔄 Reset All"):

            reset_chat()

            st.rerun()


# ===========================
#   Main Chat Interface
# ===========================

st.title("🎬 Video RAG with Gemini")

st.markdown(
    "Upload a video and chat with it using Google's Gemini AI!"
)


if not api_key:

    st.info(
        "👈 Please enter your Gemini API key in the sidebar."
    )

elif st.session_state.video_file is None:

    st.info(
        "👈 Please upload a video file in the sidebar."
    )

else:

    st.success(
        f"✅ Ready to chat about: "
        f"**{st.session_state.video_name}**"
    )

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

    if prompt := st.chat_input(
        "Ask a question about your video..."
    ):

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )

        with st.chat_message("user"):

            st.markdown(prompt)

        with st.chat_message("assistant"):

            with st.spinner(
                "Analyzing video..."
            ):

                response = (
                    st.session_state
                    .video_processor
                    .chat_with_video(
                        st.session_state.video_file,
                        prompt
                    )
                )

            if response:

                st.markdown(response)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": response
                    }
                )

            else:

                st.error(
                    "Failed to generate response."
                )