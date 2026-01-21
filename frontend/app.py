import streamlit as st
import requests
import os

# Backend URL
API_URL = "http://127.0.0.1:8000/create-mixtape"

st.set_page_config(page_title="Automated Mixtape Creator", page_icon="🎵")

st.title("🚀 Automated YouTube Mixtape Creator")
st.markdown("Upload your audio tracks, and we'll merge them, create a video, and generate a description for you!")

# File Uploader
uploaded_files = st.file_uploader("1. Upload Audio Files (MP3, WAV)", type=["mp3", "wav"], accept_multiple_files=True)

# Background Uploader
st.markdown("### 2. Choose Background")
bg_option = st.radio("Background Source:", ["Default Retro Image", "Upload Custom Video/Image"])
custom_bg = None
if bg_option == "Upload Custom Video/Image":
    custom_bg = st.file_uploader("Upload Background (JPG, PNG, MP4)", type=["jpg", "png", "mp4"])

if st.button("Create Mixtape"):
    if not uploaded_files:
        st.warning("Please upload at least one audio file.")
    else:
        with st.spinner("Processing... mixing audio, generating video... this may take a minute."):
            try:
                # Prepare files for the API request
                files_payload = []
                for file in uploaded_files:
                    # requests expects ('key', (filename, fileobj, content_type))
                    files_payload.append(
                        ("files", (file.name, file, file.type))
                    )
                
                # Add background if present
                if custom_bg:
                    files_payload.append(
                        ("background", (custom_bg.name, custom_bg, custom_bg.type))
                    )
                
                # Send request
                response = requests.post(API_URL, files=files_payload)
                
                if response.status_code == 200:
                    result = response.json()
                    st.success(result["message"])
                    
                    st.subheader("Generated Description")
                    st.text_area("Copy this for YouTube:", value=result["description_content"], height=200)
                    
                    st.subheader("Outputs")
                    st.info(f"files saved to: {os.path.dirname(result['files']['video'])}")
                    
                    # If running locally, we can try to show the video/audio
                    # Note: accessing local paths directly works if Streamlit host == backend host
                    video_path = result['files']['video']
                    if os.path.exists(video_path):
                        st.video(video_path)
                    
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
                    
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.info("Make sure the Backend API is running! (uvicorn backend.main:app --reload)")
