import os
import json
import google.generativeai as genai
from src.models.contestant import ContestantInfo


class GeminiAnalyzer:
    """
    Client for Google's Gemini API to analyze video transcriptions.
    """
    
    def __init__(self, api_key=None):
        """
        Initialize the Gemini client with API key.
        
        Args:
            api_key: Gemini API key. If None, uses the GEMINI_API_KEY environment variable.
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API key is required. Set GEMINI_API_KEY in your .env file.")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro')
    
    def analyze_transcript(self, transcript, video_filename):
        """
        Analyze transcription using Gemini to extract contestant information.
        
        Args:
            transcript: Text transcription of the video
            video_filename: Original video filename
            
        Returns:
            ContestantInfo object with extracted information
        """
        prompt = f"""
        Analyze the following transcription from a Beast Games contestant video application:
        
        "{transcript}"
        
        Extract the following information, format the response as a JSON object:
        
        1. name: The contestant's full name
        2. age: The contestant's age (as an integer)
        3. location: Where the contestant lives
        4. occupation: What the contestant does for a living
        5. strategist_type: What type of strategist they are (Hero, Villain, Social, Brainiac, Charming, or other)
        6. favorite_challenge: Their favorite challenge from Beast Games Season 1
        7. favorite_challenge_reason: Why it was their favorite
        8. favorite_contestant: Their favorite contestant from Beast Games Season 1
        9. favorite_contestant_reason: Why they were their favorite
        10. uniqueness_factors: List of factors that make them unique (as an array)
        11. prize_plans: List of what they would do with the $5,000,000 prize (as an array)
        
        If any information is missing or unclear, set the value to null.
        """
        
        response = self.model.generate_content(prompt)
        
        # Extract JSON from response
        try:
            # Try to parse the response directly
            result_json = json.loads(response.text)
        except json.JSONDecodeError:
            # If direct parsing fails, try to extract JSON from markdown code blocks
            import re
            json_pattern = r'```(?:json)?\s*([\s\S]*?)\s*```'
            json_match = re.search(json_pattern, response.text)
            
            if json_match:
                try:
                    result_json = json.loads(json_match.group(1))
                except json.JSONDecodeError:
                    raise ValueError(f"Failed to parse JSON from Gemini response: {response.text}")
            else:
                raise ValueError(f"Could not find JSON in Gemini response: {response.text}")
        
        # Add the transcript and video filename
        result_json["transcript"] = transcript
        result_json["video_filename"] = video_filename
        
        # Create and return the Pydantic model
        return ContestantInfo(**result_json) 