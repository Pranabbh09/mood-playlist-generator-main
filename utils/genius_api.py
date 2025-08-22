from dotenv import load_dotenv
import os
import requests

load_dotenv()

GENIUS_ACCESS_TOKEN = os.getenv("GENIUS_ACCESS_TOKEN")
headers = {"Authorization": GENIUS_ACCESS_TOKEN}

if not GENIUS_ACCESS_TOKEN:
    print("❗ GENIUS_API_KEY not found in environment.")
else:
    print("✅ GENIUS_API_KEY loaded.")
    # print("Authorization header:", headers)

def search_song(song_title: str) -> dict:
    url = f"https://api.genius.com/search?q={song_title}"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("❌ API request failed with status:", response.status_code)
        print("Message:", response.json())
        return None

    data = response.json()
    hits = data.get("response", {}).get("hits", [])
    if not hits:
        print("❗ No results found for:", song_title)
        return None

    top_result = hits[0]["result"]
    print("✅ Found:", top_result["full_title"])
    print("🔗 URL:", top_result["url"])
    return top_result