from typing import Optional, List
from pydantic import BaseModel, Field


class ContestantInfo(BaseModel):
    """
    Pydantic model for contestant information extracted from video transcripts.
    """
    name: str = Field(description="Contestant's full name")
    age: Optional[int] = Field(None, description="Contestant's age")
    location: Optional[str] = Field(None, description="Where the contestant lives")
    occupation: Optional[str] = Field(None, description="What the contestant does for a living")
    
    strategist_type: Optional[str] = Field(
        None, 
        description="Type of strategist (Hero, Villain, Social, Brainiac, Charming, etc.)"
    )
    
    favorite_challenge: Optional[str] = Field(
        None,
        description="Favorite challenge from Beast Games Season 1"
    )
    
    favorite_challenge_reason: Optional[str] = Field(
        None,
        description="Why this was their favorite challenge"
    )
    
    favorite_contestant: Optional[str] = Field(
        None,
        description="Favorite contestant from Beast Games Season 1"
    )
    
    favorite_contestant_reason: Optional[str] = Field(
        None,
        description="Why this was their favorite contestant"
    )
    
    uniqueness_factors: Optional[List[str]] = Field(
        None,
        description="Factors that make the contestant unique"
    )
    
    prize_plans: Optional[List[str]] = Field(
        None,
        description="What the contestant would do with the $5,000,000 prize"
    )

    video_filename: str = Field(description="Filename of the original video")
    transcript: str = Field(description="Full transcript of the video") 