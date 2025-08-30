import streamlit as st
import requests
from graph import graph
from state import GraphState
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Streamlit app configuration
st.set_page_config(page_title="Song Mood Playlist Generator", layout="centered")

# Title and input
st.title("🎵 Song Mood Playlist Generator")
song_input = st.text_input("Enter a song title:", placeholder="e.g., Happier Than Ever")

if st.button("Generate Playlist"):
    if song_input:
        with st.spinner("Processing..."):
            try:
                input_state = {"song": song_input}
                final_state = graph.invoke(input_state)

                if "error" in final_state:
                    st.error(final_state["error"])
                else:
                    # Display mood and playlist
                    mood = final_state.get("mood", "Unknown")
                    confidence = final_state.get("mood_confidence", 0.0)
                    artist = final_state.get("artist", "Unknown")
                    genre = final_state.get("genre")  # can be None
                    playlist = final_state.get("playlist", [])

                    st.success("Playlist generated successfully!")
                    st.write(f"**Mood:** {mood} (Confidence: {confidence:.2f})")
                    st.write("**Playlist:**")

                    if playlist:
                        for title, url in playlist:
                            st.write(f"- [{title}]({url})")

                            # Prepare payload for backend
                            payload = {
                                "query": song_input,
                                "title": title,
                                "artist": artist,
                                "mood": mood,
                                "youtube_url": url,
                                "mood_score": confidence,
                                "genre": genre,
                            }

                            # Send to FastAPI
                            try:
                                r = requests.post("http://localhost:8000/songs/", json=payload)
                                if r.status_code == 200:
                                    st.write(f"✅ Stored: {title}")
                                else:
                                    st.write(f"⚠️ Error storing {title}: {r.text}")
                            except Exception as e:
                                st.write(f"❌ Exception occurred: {str(e)}")
                    else:
                        st.warning("No songs found for this playlist.")
            except Exception as e:
                st.error(f"Error generating playlist: {str(e)}")
                st.info("Please check your API keys in the .env file")
    else:
        st.warning("Please enter a song title.")

# View stored songs
with st.expander("🔍 View Stored Songs (from DB)"):
    try:
        res = requests.get("http://localhost:8000/songs/", timeout=5)
        songs = res.json()

        if not songs:
            st.info("No songs stored yet.")
        else:
            for s in songs:
                st.markdown(f"""
                - 🎵 **{s['title']}** by *{s['artist']}*
                    - Mood: `{s['mood']}`
                    - Genre: `{s.get('genre', 'N/A')}`
                    - [🔗 YouTube]({s['youtube_url']})
                """)
    except requests.exceptions.ConnectionError:
        st.error("❌ Backend server not running. Please start with: `uvicorn main:app --reload --port 8000`")
    except Exception as e:
        st.error(f"Failed to fetch songs: {e}")

# API Status Check
with st.sidebar:
    st.header("🔧 API Status")
    
    # Check Genius API
    genius_token = os.getenv("GENIUS_ACCESS_TOKEN")
    if genius_token and genius_token != "your_actual_genius_token_here":
        st.success("✅ Genius API: Configured")
    else:
        st.error("❌ Genius API: Not configured")
    
    # Check Groq API
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key and groq_key != "your_actual_groq_api_key_here":
        st.success("✅ Groq API: Configured")
    else:
        st.error("❌ Groq API: Not configured")
    
    # Check Backend
    try:
        requests.get("http://localhost:8000/songs/", timeout=2)
        st.success("✅ Backend: Running")
    except:
        st.error("❌ Backend: Not running")

# Footer
st.markdown("---")
st.markdown("🎧 Built with LangChain, LangGraph, HuggingFace, and FastAPI.")
