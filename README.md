# 🚀 Automated YouTube Mixtape Creator

An end-to-end Python application that automatically creates YouTube-ready mixtape videos from multiple audio files.

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![MoviePy](https://img.shields.io/badge/MoviePy-Uses_FFmpeg-blue?style=for-the-badge&logo=python&logoColor=white)
![FFmpeg](https://img.shields.io/badge/FFmpeg-007808?style=for-the-badge&logo=ffmpeg&logoColor=white)

</div>

## 📂 Project Structure

```
youtube-mixtape/
│
├── backend/
│ ├── main.py
│ └── logic/
│ ├── audio.py
│ ├── description.py
│ └── video.py
│
├── frontend/
│ └── app.py
│
├── assets/
│ └── background.jpg
│
├── outputs/    <-- Generated files appear here
│
├── requirements.txt
└── README.md
```

## 🛠️ Setup

1. **Install Dependencies**
   Ensure you have Python 3.10+ installed.
   ```bash
   pip install -r requirements.txt
   ```
   *Note: The project uses `moviepy` and `imageio-ffmpeg`, so FFmpeg binaries are automatically handled.*

## 🏃‍♂️ How to Run

You need to run the Backend and Frontend in separate terminals.

### 1. Start the Backend (API)
From the `youtube-mixtape` directory:
```bash
uvicorn backend.main:app --reload
```
The API will start at `http://127.0.0.1:8000`.

### 2. Start the Frontend (UI)
Open a new terminal, navigate to `youtube-mixtape`, and run:
```bash
streamlit run frontend/app.py
```
The UI will open in your browser (usually `http://localhost:8501`).

## 🎮 How to Use

1. **Upload Audio**: Select your MP3 or WAV audio tracks.
2. **Choose Background**:
   - Use the **Default Retro Style** image.
   - Or **Upload Custom Video/Image** (Supports .mp4, .jpg, .png).
3. **Create Mixtape**: Click the button and let the magic happen.
4. **Get Results**:
   - Copy the auto-generated **Description** (with timestamps!) for YouTube.
   - Watch the final video directly in the app.
   - Find the files in the `outputs/` folder (`mixtape.mp4`).

## ✨ Features

- **Audio Merging**: Seamlessly combines multiple tracks into one continuous mix.
- **Dynamic Backgrounds**: Support for **Looping Video Backgrounds** (.mp4) or static images.
- **Smart Description**: Auto-generates `MM:SS - Track Name` timestamps for easy navigation.
- **End-to-End Automation**: Simple UI that abstracts away complex FFmpeg processing.
