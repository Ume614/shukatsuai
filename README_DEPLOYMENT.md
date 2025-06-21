# 🌐 就活AIコンパス - 外部公開ガイド

## 🔗 現在のアクセス方法

### ローカルネットワーク公開
アプリケーションは以下のURLで同一ネットワーク内からアクセス可能です：

```
http://192.168.0.206:8501
```

### 💻 対象ユーザー
- 同じWiFiネットワークに接続している人
- 同じルーター配下のデバイス
- 社内LAN/大学ネットワーク内の利用者

## 🌍 インターネット公開オプション

### 1. 🔧 Streamlit Cloud（推奨）
**無料でインターネット公開可能**

**手順:**
1. GitHubにコードをプッシュ
2. [share.streamlit.io](https://share.streamlit.io) でアカウント作成
3. リポジトリを接続してデプロイ
4. 自動的にhttps URLが生成される

**メリット:**
- ✅ 完全無料
- ✅ HTTPS対応
- ✅ 自動スケーリング
- ✅ 簡単デプロイ

### 2. 🎯 ngrok（一時的公開）
**開発・デモ用途向け**

```bash
# ngrokインストール後
ngrok http 8501
```

**提供されるURL例:**
```
https://abc123.ngrok.io
```

### 3. ☁️ Heroku
**本格運用向け**

```bash
# Heroku CLI使用
heroku create job-hunt-ai-app
git push heroku main
```

### 4. 🐳 Docker + AWS/GCP
**エンタープライズ向け**

## ⚙️ 設定が必要な項目

### 環境変数
以下をクラウド環境で設定：
```
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx
OPENAI_API_KEY=sk-xxxxx（オプション）
DEBUG=False
```

### セキュリティ考慮事項
- API KEYの適切な管理
- アクセス制限（必要に応じて）
- HTTPS通信の確保

## 📦 Streamlit Cloud デプロイ手順

### 1. GitHubにプッシュ
```bash
cd job_hunt_ai
git init
git add .
git commit -m "Initial commit: 就活AIコンパス"
git remote add origin https://github.com/yourusername/job-hunt-ai.git
git push -u origin main
```

### 2. Streamlit Cloudでデプロイ
1. [share.streamlit.io](https://share.streamlit.io) にアクセス
2. GitHubアカウントでログイン
3. "New app" → リポジトリ選択
4. Main file path: `main.py`
5. "Deploy!" をクリック

### 3. Secrets設定
Streamlit Cloud管理画面で環境変数を設定：
```
ANTHROPIC_API_KEY = "sk-ant-api03-xxxxx"
OPENAI_API_KEY = "sk-xxxxx"
DEBUG = "False"
```

## 🔗 想定アクセスURL

デプロイ後のURL例：
```
https://job-hunt-ai-compass.streamlit.app
```

## 📊 利用状況

### 現在の状況
- ✅ ローカルネットワーク公開済み
- 🔄 Claude API残高要チャージ
- 📱 全機能実装完了

### 推奨デプロイ方法
1. **Streamlit Cloud** - 最も簡単
2. **ngrok** - デモ・テスト用
3. **Heroku** - 本格運用

## 🎯 次のステップ

1. **API残高チャージ** → 全機能テスト
2. **GitHubリポジトリ作成** → Streamlit Cloudデプロイ
3. **URL共有** → 対象ユーザーに提供

簡単にインターネット公開可能です！