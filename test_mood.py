from agents.metadata_agent import fetch_metadata
from agents.mood_agent import classify_mood
from agents.playlist_agent import generate_playlist
from state import GraphState

state = GraphState({"song": "Happier Than Ever"})

# Step 1: Metadata extraction
state = fetch_metadata(state)

# Step 2: Mood classification
state = classify_mood(state)

# Step 3: Playlist generation
state = generate_playlist(state)

print("\n🎧 Final Mood State:")
print(state)
