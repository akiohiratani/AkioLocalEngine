from flask import Flask, jsonify
from flask_cors import CORS
from blueprints.horse_routes import horses_bp
from blueprints.races_routes import races_bp

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# エンドポイントの登録
app.register_blueprint(horses_bp)
app.register_blueprint(races_bp)

@app.route('/api/data')
def get_data():
    # http://127.0.0.1:5000/api/data
    return jsonify({"message": "Welcome to Akio Local Engine", "status": 200})

# flask-backend/app.py 追記
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
