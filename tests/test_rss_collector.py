from src.rss_collector import get_latest_articles, load_rss_feeds

def test_load_rss_feeds(tmpdir):
    """
    RSSフィードURLリストが正しく読み込まれるかをテスト
    """
    rss_file = tmpdir.join('rss_feeds.txt')
    rss_file.write('https://example.com/feed\nhttps://another.com/feed')
    urls = load_rss_feeds(rss_file)
    
    assert len(urls) == 2
    assert urls[0] == 'https://example.com/feed'

def test_get_latest_articles(mock_feedparser):
    """
    RSSフィードから最新の記事を正しく取得できるかをテスト
    """
    mock_feedparser.entries = [
        {'title': 'Test Article', 'link': 'https://example.com', 'published': '2024-09-01'}
    ]
    articles = get_latest_articles(['https://example.com/feed'])
    
    assert len(articles) == 1
    assert articles[0]['title'] == 'Test Article'
    assert articles[0]['link'] == 'https://example.com'