from pydantic import BaseModel
from datetime import datetime

# --- Tweet Schemas ---

# Base schema for a tweet's properties
class TweetBase(BaseModel):
    tweet_text: str

# Schema for creating a new tweet (used in request body)
class TweetCreate(TweetBase):
    pass

# Schema for representing a tweet in an API response
class Tweet(TweetBase):
    tweet_id: int
    verification_status: str  # Pydantic will convert the Enum to a string
    submit_date: datetime

    class Config:
        from_attributes = True # Allows Pydantic to read data from ORM models