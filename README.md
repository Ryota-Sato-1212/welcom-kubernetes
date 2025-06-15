# Welcome Kubernetes - Kubernetes学習環境

このプロジェクトは、Kubernetesの学習を支援するためのWebアプリケーションです。タスク管理機能とKubernetes演習環境を提供します。
<img width="756" alt="スクリーンショット 2025-06-15 17 19 53" src="https://github.com/user-attachments/assets/936e7519-f30f-423a-a5a9-6b893852bcc9" />

## 機能

1. **タスク管理**
   - 学習タスクの作成、編集、削除
   - ドラッグ＆ドロップによるタスクステータスの変更
<img width="1482" alt="スクリーンショット 2025-06-15 17 21 13" src="https://github.com/user-attachments/assets/4dacd88f-686c-4357-b95d-208a05e76ab0" />

2. **Kubernetes演習環境**
   - Minikubeを使用したローカルKubernetes環境
   - 基本的なKubernetesコマンドの実行
   - チュートリアル  
![スクリーンショット 2025-06-15 17 21 30](https://github.com/user-attachments/assets/1a3b342f-b7d8-4c05-a788-6b93751defd1)

3. **技術ブログ投稿機能**
   - Markdown形式での記事作成
   - コードブロックのシンタックスハイライト
   - 画像のアップロードと埋め込み
   - 記事の編集・削除機能
   - カテゴリー分けとタグ付け
   - コメント機能
   - 記事の検索機能
<img width="1508" alt="スクリーンショット 2025-06-15 17 20 12" src="https://github.com/user-attachments/assets/a240fe91-557e-4590-a2b4-32cdf650dde1" />

4. **AI検索機能**
   - OpenAI APIを使用した自然言語検索
   - Kubernetes関連の質問へのAIアシスタント回答
   - コードスニペットの生成と説明
   - エラーメッセージの解析と解決策の提案
   - 学習コンテンツのレコメンデーション
   - 検索履歴の保存と管理
<img width="1434" alt="スクリーンショット 2025-06-15 17 20 37" src="https://github.com/user-attachments/assets/90ef8d0c-5c80-4c43-a45f-6e7fff360476" />

## 必要条件

- Python 3.8以上
- Docker Desktop
- Minikube
- kubectl

## セットアップ手順

### 1. リポジトリのクローン

```bash
git clone https://github.com/yourusername/welcom-kubernetes.git
cd welcom-kubernetes
```

### 2. 仮想環境の作成と依存関係のインストール

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Minikubeのセットアップ

```bash
# Minikubeの起動
minikube start --driver=docker

# ステータスの確認
minikube status
```

![Minikube Status](static/images/minikube-status.png)

### 4. アプリケーションの起動

```bash
python app.py
```

アプリケーションは http://127.0.0.1:5051 で起動します。

## 使用方法

### タスク管理

1. ブラウザで http://127.0.0.1:5051/tasks にアクセス
2. 「New Task」フォームでタスクを作成
3. タスクをドラッグ＆ドロップでステータスを変更

![Task Management](static/images/task-management.png)

### Kubernetes演習

1. ブラウザで http://127.0.0.1:5051/k8s_exercise にアクセス
2. 「Start Minikube」ボタンをクリック
3. コマンド入力欄にKubernetesコマンドを入力して実行

![K8s Exercise](static/images/k8s-exercise.png)

## トラブルシューティング

### Minikubeが起動しない場合

```bash
# Minikubeを完全に削除
minikube delete

# 再起動
minikube start --driver=docker
```

### kubectlコマンドが動作しない場合

```bash
# kubectlの設定を確認
kubectl config view

# Minikubeのステータスを確認
minikube status
```

## 開発者向け情報

### プロジェクト構造

```
welcom-kubernetes/
├── app.py              # メインアプリケーション
├── requirements.txt    # 依存関係
├── static/            # 静的ファイル
│   ├── css/
│   ├── js/
│   └── images/
└── templates/         # HTMLテンプレート
    ├── tasks.html
    └── k8s_exercise.html
```

### データベース

SQLiteデータベースを使用してタスク情報を保存します。データベースは自動的に初期化されます。

## ライセンス

MIT License

## 貢献

1. このリポジトリをフォーク
2. 新しいブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add some amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成 
