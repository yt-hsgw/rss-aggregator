import feedparser
import os
from datetime import datetime

# RSSフィードURLリストをファイルから読み込む
def load_rss_feeds(filename):
    with open(filename, 'r') as file:
        urls = file.read().splitlines()
    return urls

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

def save_to_notion(articles):
    """
    Notion APIで記事を保存する関数（仮の処理としてファイル出力）
    実際にはNotion APIを呼び出して記事を追加します。
    """
    date_str = datetime.now().strftime("%Y-%m-%d")
    with open(f"articles_{date_str}.txt", "w") as f:
        for article in articles:
            f.write(f"Title: {article['title']}\nLink: {article['link']}\nPublished: {article['published']}\n\n")

def main():
    rss_feeds_file = 'rss_feeds.txt'
    rss_urls = load_rss_feeds(rss_feeds_file)
    articles = get_latest_articles(rss_urls)
    save_to_notion(articles)

if __name__ == "__main__":
    main()
