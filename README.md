# 🎵 iTunes + Vagalume 歌詞アプリ

## 概要
このアプリは、曲名やアーティスト名を入力すると、iTunes API から楽曲情報（タイトル・アーティスト・30秒プレビュー）を取得し、Vagalume APIまたはVagalumeサイトから歌詞を取得して表示する Streamlit アプリです。  
ユーザーは曲を選択すると、ブラウザ上で歌詞を閲覧・プレビュー再生できます。

## 使用技術
- BeautifulSoup4
- lxml

## 使用API
- **iTunes Search API**：曲情報の取得
- **Vagalume API / HTML**：歌詞の取得（APIがない場合はHTMLスクレイピング）

## システム設計図
<img width="431" height="290" alt="スクリーンショット 2025-08-17 211420" src="https://github.com/user-attachments/assets/6d5710fa-9115-4994-8811-b628837d7f21" />

## コード説明
main.py → UI と全体制御

itunes_api.py → search_song(term)

lyrics_api.py → get_vagalume_url(artist, track), get_lyrics(artist, track), get_lyrics_from_html(artist, track)
