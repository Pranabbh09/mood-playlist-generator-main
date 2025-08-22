from state import GraphState
from utils.youtube_search import search_youtube_songs
from langchain.chat_models import init_chat_model
from langchain.schema import SystemMessage, HumanMessage
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

def generate_playlist(state: GraphState) -> GraphState:
    mood = state.get("mood", "POSITIVE")
    title = state.get("title", "")
    artist = state.get("artist", "")
    mood_confidence = state.get("mood_confidence", 0.0)

    system_msg = SystemMessage(
        content="You are a music assistant that generates smart YouTube search queries to find songs similar in mood and style."
    )

    human_msg = HumanMessage(
        content=f"""Generate a YouTube search query to find songs that are similar to "{title}" by {artist}, with a {mood} mood (confidence: {mood_confidence:.2f}). 
Avoid suggesting the same song or exact duplicates. Focus on single tracks with emotional themes and musical feel.

STRICTLY RETURN FINAL SEARCH QUERY ONLY AND NOT INCLUDE ARTIST NAME AND HIS/HER SONG, NO ADDITIONAL TEXT OR EXPLANATIONS."""
    )

    llm = init_chat_model(model="llama-3.3-70b-versatile", model_provider="groq")

    result = llm([system_msg, human_msg])
    search_query = result.content.strip()

    print(f"🎯 Searching YouTube for: {search_query}")
    results = search_youtube_songs(search_query, max_results=10)

    return {
        **state,
        "playlist": results,
    }