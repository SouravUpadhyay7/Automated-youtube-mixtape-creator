from fastapi import FastAPI, UploadFile, File, HTTPException
from typing import List
import shutil
import os
import sys

# Add the current directory to sys.path to import logic modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from logic.audio import merge_audios, save_audio
from logic.description import generate_description, save_description
from logic.video import create_video

app = FastAPI()

# define paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
TEMP_DIR = os.path.join(OUTPUTS_DIR, "temp")

# Ensure directories exist
os.makedirs(OUTPUTS_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)

@app.post("/create-mixtape")
async def create_mixtape(
    files: List[UploadFile] = File(...), 
    background: UploadFile = File(None)
):
    """
    Endpoint to process audio files, create a mixtape, description, and video.
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")

    saved_file_paths = []
    
    try:
        # 1. Save uploaded files to temp dir
        for file in files:
            file_path = os.path.join(TEMP_DIR, file.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            saved_file_paths.append(file_path)
            
        # 2. Merge Audio
        combined_audio, timestamps = merge_audios(saved_file_paths)
        
        mixtape_audio_path = os.path.join(OUTPUTS_DIR, "mixtape.mp3")
        save_audio(combined_audio, mixtape_audio_path)
        
        # 3. Generate Description
        description_text = generate_description(timestamps)
        description_path = os.path.join(OUTPUTS_DIR, "description.txt")
        save_description(description_text, description_path)
        
        # 4. Generate Video
        background_path = os.path.join(ASSETS_DIR, "background.jpg")
        
        # Check if user uploaded a custom background
        if background:
            custom_bg_path = os.path.join(TEMP_DIR, background.filename)
            with open(custom_bg_path, "wb") as buffer:
                shutil.copyfileobj(background.file, buffer)
            saved_file_paths.append(custom_bg_path)
            background_path = custom_bg_path

        mixtape_video_path = os.path.join(OUTPUTS_DIR, "mixtape.mp4")
        
        # Pass background path to video logic (it handles images and videos)
        create_video(mixtape_audio_path, background_path, mixtape_video_path)
        
        return {
            "status": "success",
            "message": "Mixtape created successfully!",
            "files": {
                "audio": mixtape_audio_path,
                "video": mixtape_video_path,
                "description": description_path
            },
            "description_content": description_text
        }
        
    except Exception as e:
        print(f"Error processing request: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # Cleanup temp files
        for path in saved_file_paths:
            try:
                if os.path.exists(path):
                    os.remove(path)
            except Exception as cleanup_error:
                print(f"Warning: Could not delete temp file {path}: {cleanup_error}")
