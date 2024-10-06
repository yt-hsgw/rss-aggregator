import os
import requests
from datetime import datetime
import random


def load_rss_feeds(file_path='rss_feeds.txt'):
    rss_feeds = {}
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if line.strip():  # 空行はスキップ
                    site_name, url = line.strip().split('|')
                    rss_feeds[site_name] = url
    except FileNotFoundError:
        print("指定されたファイルが見つかりませんでした。")
    except Exception as e:
        print(f"RSSフィードの読み込みエラー: {e}")
    return rss_feeds

def format_date(date_str):
    """
    日付文字列を指定のフォーマットに変換する関数
    """
    try:
        dt = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")
        return dt.strftime("%Y-%m-%d %H:%M")
    except ValueError:
        return date_str  # フォーマットできなかった場合はそのまま返す

def format_notion_article(article):
    """
    Notionに記事情報を渡すためのフォーマットに変換する関数
    """
    return {
        "title": article['title'],
        "link": article['link'],
        "published": article.get('published', '不明')
    }

def make_post_request(url, headers, data):
    """
    汎用のPOSTリクエスト関数
    """
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # ステータスコードが200以外なら例外を発生
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        print(f"Response Body: {response.json()}")
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
    except requests.exceptions.RequestException as err:
        print(f"Request failed: {err}")
    return None

def get_env_variable(key):
    """
    環境変数を取得する関数。見つからない場合は例外を発生。
    """
    value = os.getenv(key)
    if value is None:
        print(f"Environment variable {key} is not set.")
        raise ValueError(f"Environment variable {key} is not set.")
    else:
        print("get env success")
    return value

def get_random_emoji():
    """
    ランダムなアイコンを設定する関数
    """
    emojis = ["📚", "📰", "💡", "🚀", "🔍", "⚙️", "🌍", "💻", "📈", "🧠"]
    return random.choice(emojis)