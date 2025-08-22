# from transformers import pipeline
import lyricsgenius
from dotenv import load_dotenv
import os
from langchain.chat_models import init_chat_model
from langchain.schema import SystemMessage, HumanMessage

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
os.environ["GROQ_API_KEY"] = GROQ_API_KEY


def classify_lyrics_emotion(lyrics: str) -> tuple[str, float]:

    llm = init_chat_model(model="llama-3.3-70b-versatile", model_provider="groq")

    if not lyrics:
        return "unknown", 0.0

    system_msg = SystemMessage(
        content="You are an expert in music emotion analysis. Given song lyrics, classify the primary mood into one of: happy, sad, angry, romantic, chill, energetic, nostalgic. Return the mood and a confidence score (0.0 to 1.0) based on the emotional tone."
    )
    human_msg = HumanMessage(
        content=f"Analyze the following lyrics and provide the mood and confidence score:\n\n{lyrics}\n\nReturn only: mood,confidence (e.g., 'happy,0.95')"
    )

    response = llm.invoke([system_msg, human_msg])
    mood, confidence = response.content.strip().split(",")
    return mood, float(confidence)

def get_lyrics_from_genius_api(song: str, artist: str) -> str:
    genius = lyricsgenius.Genius("fFfunqPryttREi690idLLNh5NBfyjeS7nt3kaFTq7jB0-F3fUQhFJ6_csffZ_NHB")
    try:
        track = genius.search_song(song, artist)
        return track.lyrics if track and track.lyrics else "Lyrics not found in API."
    except Exception as e:
        return f"API error: {str(e)}"