from flask import Flask, request, jsonify
from flask_cors import CORS
from database_dynamodb import init_dynamodb, get_all_users, create_user as db_create_user, get_user_by_id
import os

app = Flask(__name__)

# CORS設定（Reactアプリケーションとの通信用）
CORS(app, origins=[
    "http://localhost:5173",  # React Vite開発サーバー
    "http://127.0.0.1:5173",  # React Vite開発サーバー（IP版）
    "http://localhost:8000",  # Flask
    "http://127.0.0.1:8000"   # Flask（IP版）
])

# アプリケーション起動時にデータベースを初期化
@app.before_request
def before_first_request():
    if not hasattr(app, 'db_initialized'):
        init_dynamodb()
        app.db_initialized = True

@app.route('/')
def read_root():
    return jsonify({"Hello": "World", "message": "Flask is running!"})

@app.route('/api/health')
def health_check():
    return jsonify({"status": "healthy", "timestamp": "2025-07-23"})

@app.route('/api/users', methods=['GET'])
def get_users():
    try:
        users = get_all_users()
        return jsonify({"users": users})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = get_user_by_id(user_id)
        if user:
            return jsonify(user)
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        
        # バリデーション
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        if 'name' not in data or 'email' not in data:
            return jsonify({"error": "Name and email are required"}), 400
        
        # ユーザー作成
        new_user = db_create_user(
            name=data['name'],
            email=data['email'],
            age=data.get('age')
        )
        
        return jsonify(new_user), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/items/<int:item_id>')
def read_item(item_id):
    q = request.args.get('q')
    return jsonify({"item_id": item_id, "q": q})

@app.route('/api/message')
def get_message():
    return jsonify({
        "message": "ReactからのAPIリクエストが成功しました！",
        "timestamp": "2025-07-23",
        "data": {
            "server": "Flask",
            "version": "3.0.0",
            "cors_enabled": True
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
