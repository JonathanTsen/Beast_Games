import os
from openai import OpenAI
from pathlib import Path
import tempfile
from moviepy.editor import VideoFileClip


class OpenAITranscriber:
    """
    Client for OpenAI's Whisper API to transcribe video content.
    """
    
    def __init__(self, api_key=None):
        """
        Initialize the OpenAI client with API key.
        
        Args:
            api_key: OpenAI API key. If None, uses the OPENAI_API_KEY environment variable.
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY in your .env file.")
        
        self.client = OpenAI(api_key=self.api_key)
    
    def extract_audio_from_video(self, video_path):
        """
        Extract audio from video file and save to temporary file.
        
        Args:
            video_path: Path to the video file
            
        Returns:
            Path to the temporary audio file
        """
        # Create temporary file for audio
        temp_audio = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
        temp_audio_path = temp_audio.name
        temp_audio.close()
        
        # Extract audio using moviepy
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(temp_audio_path, verbose=False, logger=None)
        video.close()
        
        return temp_audio_path
    
    def transcribe_video(self, video_path):
        """
        Transcribe video using OpenAI's Whisper API.
        
        Args:
            video_path: Path to the video file
            
        Returns:
            Transcription text
        """
        try:
            # Extract audio from video
            audio_path = self.extract_audio_from_video(video_path)
            
            # Transcribe audio
            with open(audio_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
            
            # Clean up temporary audio file
            os.unlink(audio_path)
            
            return transcript.text
            
        except Exception as e:
            print(f"Error transcribing video: {e}")
            raise 