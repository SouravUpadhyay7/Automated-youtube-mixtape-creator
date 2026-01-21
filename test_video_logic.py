import sys
import os

# Add logic to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.logic.video import create_video
from pydub import AudioSegment
import imageio_ffmpeg
import traceback

# Configure Pydub
AudioSegment.converter = imageio_ffmpeg.get_ffmpeg_exe()

# Paths
audio_path = "test_audio.mp3"
video_path = "test_video.mp4"
image_path = "assets/background.jpg"

print(f"Using FFmpeg at: {imageio_ffmpeg.get_ffmpeg_exe()}")

try:
    print("Generating dummy audio...")
    silence = AudioSegment.silent(duration=1000) # 1 sec
    silence.export(audio_path, format="mp3")
    print(f"Audio created: {os.path.exists(audio_path)}")

    print("Testing create_video...")
    create_video(audio_path, image_path, video_path)
    print("Video created successfully!")

except Exception as e:
    print("FAILED with error:")
    traceback.print_exc()

finally:
    # Cleanup
    if os.path.exists(audio_path):
        try: os.remove(audio_path) 
        except: pass
    if os.path.exists(video_path):
        try: os.remove(video_path)
        except: pass
