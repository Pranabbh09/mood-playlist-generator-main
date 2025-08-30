from langgraph.graph import StateGraph, END
from state import GraphState

# Import agent functions
from agents.metadata_agent import fetch_metadata
from agents.mood_agent import classify_mood
from agents.playlist_agent import generate_playlist
from agents.finalize_playlist import finalize_playlist

# New validation function
def validate_playlist(state: GraphState) -> GraphState:
    playlist = state.get("playlist", [])
    if len(playlist) < 3:
        return {"error": "Playlist too short; consider adjusting the mood or query.", "validated": False}
    return {"validated": True}

# Step 1: Define the graph
workflow = StateGraph(GraphState)

# Step 2: Add nodes
workflow.add_node("metadata", fetch_metadata)
workflow.add_node("mood", classify_mood)
workflow.add_node("playlist", generate_playlist)
workflow.add_node("validate", validate_playlist)
workflow.add_node("finalize", finalize_playlist)

# Step 3: Define edges with conditional logic
workflow.set_entry_point("metadata")
workflow.add_edge("metadata", "mood")
workflow.add_conditional_edges(
    "mood",
    lambda state: "playlist" if not state.get("error") else END
)
workflow.add_edge("playlist", "validate")
workflow.add_conditional_edges(
    "validate",
    lambda state: "playlist" if not state.get("validated", False) else END
)
workflow.add_edge("validate", "finalize")
workflow.add_edge("finalize", END)

# Step 4: Compile the DAG
graph = workflow.compile()

# Remove IPython display code to avoid import errors
# from IPython.display import Image, display
# try:
#     display(Image(graph.get_graph().draw_mermaid_png()))
# except Exception as e:
#     print(e)

if __name__ == "__main__":
    input_state = {"song": "Happier Than Ever"}
    final_state = graph.invoke(input_state)
    print("✅ Final Playlist State:")
    if "error" in final_state:
        print(f"❌ Error: {final_state['error']}")
    else:
        for song in final_state.get("playlist", []):
            print(f"🎵 {song[0]} → {song[1]}")
        print(f"Mood: {final_state.get('mood')}, Confidence: {final_state.get('mood_confidence'):.2f}")