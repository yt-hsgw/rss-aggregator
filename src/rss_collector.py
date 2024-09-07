import feedparser
import requests
from datetime import datetime
from dotenv import load_dotenv
from src.utils import load_rss_feeds, get_env_variable, make_post_request, get_random_emoji

# 環境変数の読み込み
load_dotenv()

# Notion APIの設定
NOTION_API_URL = "https://api.notion.com/v1/pages"
NOTION_API_KEY = get_env_variable('NOTION_API_KEY')  # 環境変数からNotionのAPIキーを取得
DATABASE_ID = get_env_variable('NOTION_DATABASE_ID')  # 環境変数からNotionのデータベースIDを取得
NOTION_VERSION = get_env_variable('NOTION_VERSION')  # 環境変数からNotionのバージョンを取得

def get_latest_articles(rss_urls):
    """
    各RSSフィードから最新の記事を1件ずつ取得する関数
    """
    articles = []
    for url in rss_urls:
        feed = feedparser.parse(url)
        if 'entries' in feed and len(feed.entries) > 0:
            entry = feed.entries[0]  # 最新記事
            articles.append({
                'title': entry.title,
                'link': entry.link,
                'published': entry.get('published', entry.get('updated', None))
            })
    return articles

def create_notion_page(articles):
    """
    Notion APIで記事をカレンダーデータベースにページとして保存する関数
    """
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION
    }
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    # Notionページのデータ
    notion_page = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Name": {
                "title": [{"text": {"content": "今日のトピック"}}],
            },
            "Date": {
                "date": {"start": date_str}
            }
        },
        "icon": {
            "type": "emoji",
            "emoji": get_random_emoji()
        },
        "children": [
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": f"{article['title']}",
                                "link": {"url": article['link']}
                            }
                        }
                    ]
                }
            } for article in articles
        ]
    }

    response = make_post_request(NOTION_API_URL, headers, notion_page)
    if response:
        print("Notionページが正常に作成されました。")
    else:
        print("Notionページの作成に失敗しました。")

def main():
    rss_feeds_file = 'data/rss_feeds.txt'
    
    # RSSフィードURLリストをロード
    rss_urls = load_rss_feeds(rss_feeds_file)
    # 最新の記事を取得
    articles = get_latest_articles(rss_urls)
    # Notionに保存
    create_notion_page(articles)

if __name__ == "__main__":
    main()