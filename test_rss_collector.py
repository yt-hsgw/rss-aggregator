import unittest
from rss_collector import get_latest_articles

class TestRSSCollector(unittest.TestCase):

    def test_get_latest_articles(self):
        # テスト用のRSSフィード（実際にはテスト専用フィードを使うのが望ましい）
        test_feeds = ["https://techcrunch.com/feed/"]
        articles = get_latest_articles(test_feeds)
        
        # 記事がちゃんと取得されているか
        self.assertTrue(len(articles) > 0)
        # 記事のフォーマットが正しいか
        for article in articles:
            self.assertIn('title', article)
            self.assertIn('link', article)
            self.assertIn('published', article)

if __name__ == "__main__":
    unittest.main()
