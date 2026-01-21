from moviepy import AudioFileClip, concatenate_audioclips
import os
from typing import List, Tuple

def merge_audios(file_paths: List[str]):
    """
    Merges multiple audio files into one using MoviePy.
    
    Args:
        file_paths (List[str]): List of paths to audio files.
        
    Returns:
        Tuple[AudioFileClip, List[Tuple[str, int]]]: 
            - The combined Audio clip object.
            - A list of tuples containing (filename, start_time_ms).
    """
    clips = []
    timestamps = []
    current_time_ms = 0
    
    for path in file_paths:
        filename = os.path.basename(path)
        
        # Load audio clip
        clip = AudioFileClip(path)
        
        timestamps.append((filename, int(current_time_ms)))
        
        # Duration is in seconds, convert to ms for timestamps
        current_time_ms += clip.duration * 1000
        
        clips.append(clip)
        
    combined = concatenate_audioclips(clips)
    return combined, timestamps

def save_audio(audio, output_path: str):
    """Saves the audio clip to a file."""
    # Write audio file
    audio.write_audiofile(output_path, codec='libmp3lame')
    
    # Close the clips to release resources
    # (Note: In a more complex app, we might want to handle this explicitly)
    try:
        audio.close()
    except:
        pass
