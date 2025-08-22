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
    else:
        st.warning("Please enter a song title.")

# View stored songs
with st.expander("🔍 View Stored Songs (from DB)"):
    try:
        res = requests.get("http://localhost:8000/songs/")
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
    except Exception as e:
        st.error(f"Failed to fetch songs: {e}")

# Footer
st.markdown("---")
st.markdown("🎧 Built with LangChain, LangGraph, HuggingFace, and FastAPI.")
