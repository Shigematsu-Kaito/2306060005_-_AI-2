import requests
import re
from bs4 import BeautifulSoup
 
def normalize_for_vagalume(s):
    """
    Vagalume URL 用に正規化
    """
    s = s.lower()
    s = re.sub(r"\(.*?\)", "", s)
    s = re.sub(r"feat\.|featuring|with|&|,|×|x", "", s, flags=re.IGNORECASE)
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"[^\w\-]", "", s)
    return s.strip()
 
def get_vagalume_url(artist, track):
    artist_norm = normalize_for_vagalume(artist)
    track_norm = normalize_for_vagalume(track)
    return f"https://www.vagalume.com.br/{artist_norm}/{track_norm}.html"
 
def get_lyrics(artist, track):
    """
    Vagalume API で歌詞を取得、存在しない場合は None
    """
    artist_norm = normalize_for_vagalume(artist)
    track_norm = normalize_for_vagalume(track)
    url = f"https://api.vagalume.com.br/v1/lyrics/{artist_norm}/{track_norm}"
 
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            mus_list = data.get("mus", [])
            if mus_list and mus_list[0].get("text"):
                text = mus_list[0]["text"]
                text = re.sub(r"<br\s*/?>", "\n", text)
                text = re.sub(r"<.*?>", "", text)
                return text.strip()
        return None
    except requests.exceptions.RequestException:
        return None
 
def get_lyrics_from_html(artist, track):
    """
    API に歌詞がない場合、HTML をスクレイピングして取得
    """
    url = get_vagalume_url(artist, track)
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return None
 
        soup = BeautifulSoup(response.text, "lxml")
        lyrics_div = soup.find("div", class_="cnt-letra")  # 最新構造
        if not lyrics_div:
            lyrics_div = soup.find("div", id="lyrics")      # 旧構造
        if lyrics_div:
            for br in lyrics_div.find_all("br"):
                br.replace_with("\n")
            return lyrics_div.get_text().strip()
        return None
    except Exception as e:
        print("HTML lyrics fetch error:", e)
        return None