from urllib.parse import urlparse
import feedparser
import requests
from datetime import datetime
from dotenv import load_dotenv
from src.utils import load_rss_feeds, get_env_variable, make_post_request, get_random_emoji
import time

# 環境変数の読み込み
load_dotenv()

# Notion APIの設定
NOTION_API_URL = "https://api.notion.com/v1/pages"
NOTION_API_KEY = get_env_variable('NOTION_API_KEY')  
DATABASE_ID = get_env_variable('NOTION_DATABASE_ID')  
NOTION_VERSION = get_env_variable('NOTION_VERSION')  

def get_latest_articles(rss_feeds):
    """
    各RSSフィードから最新の記事を取得する関数
    """
    articles_dict = {}
    for site_name, url in rss_feeds.items():
        try:
            feed = feedparser.parse(url)
            if 'entries' in feed and len(feed.entries) > 0:
                entry = feed.entries[0]
                published_date = entry.get('published', entry.get('updated', None))
                articles_dict[site_name] = {
                    'title': entry.title,
                    'link': entry.link,
                    'host_link': urlparse(entry.link).netloc,
                    'published': published_date if published_date else datetime.now().isoformat()
                }
        except Exception as e:
            print(f"RSS取得エラー: {site_name} - {url}\n詳細: {e}")
    return articles_dict

def create_notion_page(articles_dict, rss_feeds):
    """
    Notion APIで各サイトの記事をカレンダーデータベースにページとして保存する関数
    """
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION
    }
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    
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
        "children": []
    }
    
    for site_name, article in articles_dict.items():
        parsed_url = urlparse(article['link'])
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        
        # サイト情報のセクションタイトル
        notion_page["children"].append({
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": site_name,
                            "link": {"url": base_url},
                        }
                    }
                ]
            }
        })
        
        # 記事情報をリスト形式で追加し、リンクをホスト部分のみにする
        notion_page["children"].append({
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": article['title'],
                            "link": {"url": article['link']}
                        }
                    }
                ]
            }
        })
    max_retries = 3
    for attempt in range(max_retries):
        response = make_post_request(NOTION_API_URL, headers, notion_page)
        if response:
            print("Notionページが正常に作成されました。")
            return
        else:
            print(f"Notionページの作成に失敗しました。リトライ {attempt + 1}/{max_retries}")
            time.sleep(2)  # リトライ間隔

    print("Notionページの作成に失敗しました。全リトライが完了しました。")

def main():
    rss_feeds_file = 'data/rss_feeds.txt'
    
    try:
        # 辞書形式でRSSフィードを読み込む
        rss_feeds = load_rss_feeds(rss_feeds_file)
    except Exception as e:
        print(f"RSSフィードURLリストのロードに失敗しました: {e}")
        return

    # 最新の記事を取得
    articles_dict = get_latest_articles(rss_feeds)
    
    # Notionに保存
    if articles_dict:
        create_notion_page(articles_dict, rss_feeds)
    else:
        print("取得できる最新の記事がありませんでした。")

if __name__ == "__main__":
    main()
