FROM python:3.12-slim

WORKDIR /app

# システムの依存関係をインストール
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Poetryをインストール（バージョン2系を指定）
RUN pip install poetry==2.*

# Poetry設定: 仮想環境を作成しない（コンテナ内では不要）
RUN poetry config virtualenvs.create false

# pyproject.tomlとpoetry.lockをコピー
COPY pyproject.toml poetry.lock* ./

# 依存関係をインストール（開発依存関係は除く）
RUN poetry install --without dev --no-root

# アプリケーションコードをコピー
COPY . .

# ポート8000を公開
EXPOSE 8000

# アプリケーションを起動
CMD ["python", "main.py"]
