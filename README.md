## 構成

```

├── flask-backend/         # Flaskバックエンド
│   ├── app.py             # Flaskアプリケーション
│   ├── blueprints         # ルーティング設定
│   ├── domain             # ビジネス層、型など
│   ├── services           # スクレイピング、エクセル出力
│   ├── requirements.txt   # Python依存関係
│   └── venv/              # Python仮想環境


```

## コマンド
```
cd flask-backend 
python -m venv venv
py -3.12 -m venv venv312

venv\Scripts\activate
venv312\Scripts\activate

pip install -r requirements.txt
pip freeze > requirements.txt
python app.py


taskkill /IM flask-app.exe /F
rmdir /s /q dist
pyinstaller --onefile app.py --name akio-local-engine


```