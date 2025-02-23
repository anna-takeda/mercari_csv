# Pythonイメージをベースにする（バージョンは適宜変更）
FROM python:3.9-slim

# 作業ディレクトリを設定
WORKDIR /app

# requirements.txt をコピーし、ライブラリをインストール
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

# アプリのソースコードをコピー
COPY . /app

# Cloud Run はポート番号を $PORT で渡すので、それを使って streamlit を起動する
CMD streamlit run app.py --server.port $PORT --server.headless true
