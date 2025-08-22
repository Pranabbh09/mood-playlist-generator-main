from state import GraphState
from utils.emotional_model import classify_lyrics_emotion, get_lyrics_from_genius_api

def classify_mood(state: GraphState) -> GraphState:
    song = state.get("song")
    artist = state.get("artist")

    lyrics = get_lyrics_from_genius_api(song, artist)

    if lyrics.startswith("Error"):
        return {"error": lyrics}

    mood, confidence = classify_lyrics_emotion(lyrics)

    # Simulate secondary mood analysis (e.g., using a different method or model)
    secondary_mood, _ = classify_lyrics_emotion(lyrics.replace(" ", "_"))  # Simple variation

    return {
        **state,
        "lyrics_text": lyrics,
        "mood": mood,
        "mood_options": [mood, secondary_mood],
        "mood_confidence": confidence,
    }