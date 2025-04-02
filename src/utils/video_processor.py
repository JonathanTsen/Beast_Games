import os
from pathlib import Path
from typing import List

from src.api.openai_client import OpenAITranscriber
from src.api.gemini_client import GeminiAnalyzer
from src.models.contestant import ContestantInfo


class VideoProcessor:
    """
    Utility to process videos in a directory.
    """
    
    def __init__(self, input_dir=None):
        """
        Initialize the video processor.
        
        Args:
            input_dir: Directory containing input videos. If None, uses INPUT_VIDEO_DIR env var.
        """
        self.input_dir = input_dir or os.getenv("INPUT_VIDEO_DIR")
        if not self.input_dir:
            raise ValueError("Input directory is required. Set INPUT_VIDEO_DIR in your .env file.")
        
        self.transcriber = OpenAITranscriber()
        self.analyzer = GeminiAnalyzer()
    
    def get_video_files(self):
        """
        Get all video files in the input directory.
        
        Returns:
            List of paths to video files
        """
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv']
        video_files = []
        
        for file in os.listdir(self.input_dir):
            file_path = os.path.join(self.input_dir, file)
            if os.path.isfile(file_path) and any(file.lower().endswith(ext) for ext in video_extensions):
                video_files.append(file_path)
        
        return video_files
    
    def process_videos(self) -> List[ContestantInfo]:
        """
        Process all videos in the input directory.
        
        Returns:
            List of ContestantInfo objects
        """
        video_files = self.get_video_files()
        if not video_files:
            print(f"No video files found in {self.input_dir}")
            return []
        
        contestant_info_list = []
        
        for video_path in video_files:
            try:
                filename = os.path.basename(video_path)
                print(f"Processing video: {filename}")
                
                # Transcribe video
                print("  Transcribing...")
                transcript = self.transcriber.transcribe_video(video_path)
                
                # Analyze transcript
                print("  Analyzing transcript...")
                contestant_info = self.analyzer.analyze_transcript(transcript, filename)
                
                contestant_info_list.append(contestant_info)
                print(f"  Extracted info for: {contestant_info.name}")
                
            except Exception as e:
                print(f"Error processing video {video_path}: {e}")
        
        return contestant_info_list 