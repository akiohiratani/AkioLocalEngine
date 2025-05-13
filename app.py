from flask import Flask, jsonify
from flask_cors import CORS
from blueprints.horse_routes import horses_bp
from blueprints.races_routes import races_bp
from services.usecase import Usecase

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# エンドポイントの登録
app.register_blueprint(horses_bp)
app.register_blueprint(races_bp)

@app.route('/')
def get_data():
    # http://127.0.0.1:5000/
    return jsonify({"message": "Welcome to Akio Local Engine Ver 1.0", "status": 200})

@app.route('/api/activate')
def get_status():
    # http://127.0.0.1:5000/api/activate
    try:
        if Usecase().get_activate():
            return jsonify({"activate": "ok", "status": 200})
        else:
            return jsonify({
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "Expired"
                }
            }), 500
    except Exception as e:
        return jsonify({
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": str(e)
            }
        }), 500
# flask-backend/app.py 追記
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
