## 階層

```
rss_project/
│
├── rss_collector.py        # RSSフィードを収集するメインのコード
├── test_rss_collector.py    # ユニットテストコード
├── requirements.txt         # 必要なPythonライブラリ
├── .github/
│   └── workflows/
│       └── rss_collection.yml  # GitHub Actionsの設定ファイル
└── README.md                # プロジェクトの説明
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
python rss_collector.py
```

### テスト実行

```bash
python -m unittest test_rss_collector.py
```

### 仮想環境の無効化

```bash
deactivate
```
