import streamlit as st
from itunes_api import search_song
from lyrics_api import get_vagalume_url, get_lyrics, get_lyrics_from_html
 
st.set_page_config(page_title="🎵 歌詞＆試聴アプリ", layout="centered")
st.title("🎧 iTunes + Vagalume 歌詞アプリ")
 
query = st.text_input("曲名またはアーティスト名を入力してください")
 
if query:
    songs = search_song(query, limit=5)
    
    if songs:
        song_names = [f"{s['trackName']} - {s['artistName']}" for s in songs]
        choice = st.selectbox("曲を選択してください", song_names)
        selected = songs[song_names.index(choice)]
        
        # プレビュー再生
        if selected.get("previewUrl"):
            st.audio(selected["previewUrl"], format="audio/mp4")
        
        # 歌詞ページ URL
        url = get_vagalume_url(selected["artistName"], selected["trackName"])
        st.markdown(f"🎵 歌詞ページ: [こちらをクリック]({url})", unsafe_allow_html=True)
        
        # 歌詞取得
        lyrics = get_lyrics(selected["artistName"], selected["trackName"])
        if not lyrics:
            lyrics = get_lyrics_from_html(selected["artistName"], selected["trackName"])
        
        if lyrics:
            st.subheader("📝 歌詞")
            st.text_area("歌詞", lyrics, height=400)
        else:
            st.info("歌詞は見つかりませんでした。リンクから確認してください。")
        
    else:
        st.warning("曲が見つかりませんでした。")