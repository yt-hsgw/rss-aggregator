## 階層

```markdown
rss_project/
│
├── src/
│   ├── __init__.py
│   ├── rss_collector.py  # RSSフィードの収集ロジック
│   ├── notion_handler.py # Notion API関連の処理
│   └── utils.py          # ヘルパー関数（例: ファイル読み込み関数など）
│
├── data/
│   └── rss_feeds.txt     # RSSフィードのURLリストを管理
│
├── tests/
│   ├── test_rss_collector.py  # rss_collector.py のテスト
│   ├── test_notion_handler.py # notion_handler.py のテスト
│   └── test_utils.py          # utils.py のテスト
│
├── .github/
│   └── workflows/
│       └── rss_collection.yml  # GitHub Actionsの設定ファイル
|
├── .gitignore             # 無視するファイルやディレクトリ
├── requirements.txt       # 必要なパッケージ
├── README.md              # プロジェクトの概要
└── notion_publisher.py    # 実行スクリプト

```

## ローカルで動作を確認する

### プロジェクト

> ディレクトリに移動

```powershell
cd rss_project
```

### 仮想環境の作成 (venvを使用)

```bash
python3 -m venv venv
```

### 仮想環境の有効化

> macOS/Linuxの場合:

```bash
source venv/bin/activate
```

### 必要なライブラリをインストール

```bash
pip install -r requirements.txt
```

### 実行

```bash
python notion_publisher.py
```

### 仮想環境の無効化

```bash
deactivate
```
