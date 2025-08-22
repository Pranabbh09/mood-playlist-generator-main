import requests

def finalize_playlist(state):
    playlist = state.get("playlist", [])

    for idx, song in enumerate(playlist):
        try:
            # Defensive unpacking
            if isinstance(song, str):
                print(f"[ERROR] Playlist item at index {idx} is a string: {song}")
                continue

            if isinstance(song, tuple):
                song = song[0]  # Assuming it's a (dict, meta) tuple

            if not isinstance(song, dict):
                print(f"[ERROR] Playlist item at index {idx} is not a dict: {song}")
                continue

            song_payload = {
                "title": song["title"],
                "artist": song["artist"],
                "mood": state.get("mood"),
                "youtube_url": song.get("youtube_url", ""),
                "mood_score": song.get("mood_score", 0.0),
                "genre": state.get("genre") or song.get("genre")
            }

            print(f"[INFO] Posting to DB: {song_payload}")
            requests.post("http://localhost:8000/songs/", json=song_payload)

        except Exception as e:
            print(f"[ERROR] Failed to process song at index {idx}: {e}")

    return state
