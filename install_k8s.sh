#!/bin/bash

echo "🚀 Kubernetes環境のセットアップを開始します..."

# Homebrewがインストールされているか確認
if ! command -v brew &> /dev/null; then
    echo "📦 Homebrewをインストールします..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Dockerがインストールされているか確認
if ! command -v docker &> /dev/null; then
    echo "🐳 Dockerをインストールします..."
    brew install --cask docker
    echo "⚠️ Docker Desktopを起動してください。"
    open -a Docker
    read -p "Docker Desktopが起動したらEnterキーを押してください..."
fi

# kubectlがインストールされているか確認
if ! command -v kubectl &> /dev/null; then
    echo "🔧 kubectlをインストールします..."
    brew install kubectl
fi

# Minikubeがインストールされているか確認
if ! command -v minikube &> /dev/null; then
    echo "🚢 Minikubeをインストールします..."
    brew install minikube
fi

# Minikubeの起動
echo "🚀 Minikubeを起動します..."
minikube start

# インストールの確認
echo "✅ インストール完了！"
echo "📊 バージョン情報:"
echo "kubectl version:"
kubectl version --client
echo "minikube version:"
minikube version 