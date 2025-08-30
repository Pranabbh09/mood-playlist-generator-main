from typing import TypedDict, Optional, List
from pydantic import BaseModel

class GraphState(TypedDict, total=False):
    song: str
    artist: str
    title: str
    full_title: str
    lyrics_url: str
    lyrics_text: str
    mood: str  # Primary mood
    mood_options: List[str]  # Multiple mood classifications
    mood_confidence: float  # Confidence of primary mood
    playlist: List[tuple[str, str]]  # [(title, YouTube link)]
    error: Optional[str]
    validated: bool  # Flag for playlist validation
    
class SongCreate(BaseModel):
    title: str
    artist: str
    mood: str
    youtube_url: str
    mood_score: float
    genre: Optional[str] = None

class SongOut(SongCreate):
    id: int

    class Config:
        from_attributes = True
