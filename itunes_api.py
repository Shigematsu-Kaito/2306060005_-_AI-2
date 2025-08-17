import requests
 
def search_song(term, limit=10):
    """
    iTunes API で曲情報を検索
    """
    term = term.strip().replace("&", "and")
    url = "https://itunes.apple.com/search"
    params = {"term": term, "media": "music", "limit": limit}
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        results = response.json().get("results", [])
        songs = []
        for r in results:
            songs.append({
                "trackName": r.get("trackName"),
                "artistName": r.get("artistName"),
                "previewUrl": r.get("previewUrl"),
            })
        return songs
    return []