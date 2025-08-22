from utils.genius_api import search_song
from state import GraphState

def fetch_metadata(state: GraphState) -> GraphState:
    song_title = state.get("song")
    if not song_title:
        return {"error": "No song title provided."}

    song_data = search_song(song_title)
    if not song_data:
        return {"error": f"No results found for '{song_title}'"}

    return {
        "song": song_title,
        "artist": song_data["primary_artist"]["name"],
        "title": song_data["title"],
        "full_title": song_data["full_title"],
        "lyrics_url": song_data["url"],
    }