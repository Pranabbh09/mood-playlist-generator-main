from youtube_search import YoutubeSearch

def search_youtube_songs(query: str, max_results: int = 5):
    results = YoutubeSearch(query, max_results=max_results).to_dict()
    playlist = []
    for item in results:
        title = item["title"]
        url = f"https://www.youtube.com{item['url_suffix']}"
        playlist.append((title, url))
    return playlist