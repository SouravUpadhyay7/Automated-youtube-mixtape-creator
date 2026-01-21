from moviepy import AudioFileClip, ImageClip, VideoFileClip
import os

def create_video(audio_path: str, background_path: str, output_path: str):
    """
    Creates a video file from an audio file and a background (Image or Video).
    
    Args:
        audio_path (str): Path to the input audio file.
        background_path (str): Path to the background image or video.
        output_path (str): Path to save the final video.
    """
    # Load the audio
    audio = AudioFileClip(audio_path)
    duration = audio.duration
    
    # Check extension
    ext = os.path.splitext(background_path)[1].lower()
    is_video_file = ext in ['.mp4', '.mov', '.avi', '.webm']
    
    if is_video_file:
        # Load video
        clip = VideoFileClip(background_path)
        
        # Loop it to match audio duration
        # MoviePy v2 uses looped()
        video = clip.looped().with_duration(duration)
        
        # Ensure it fits 1080p (optional, but good practice)
        # video = video.resized(height=1080) 
        
    else:
        # Static Image
        # To make it "move" (Zoom effect), we need to use 'resized' with a function.
        # However, purely static is safer if we don't want render errors.
        # User asked "can we use something else moving video?" 
        # -> implying they might want to swap the file.
        # So enabling Video File support is the best answer.
        video = ImageClip(background_path).with_duration(duration)

    # Set audio
    video = video.with_audio(audio)
    
    # Write file
    video.write_videofile(
        output_path, 
        fps=24 if is_video_file else 1, # Low FPS for image to save time
        codec="libx264", 
        audio_codec="aac"
    )
