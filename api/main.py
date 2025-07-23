from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from database_dynamodb import init_dynamodb, get_all_users, create_user as db_create_user

app = FastAPI()

# アプリケーション起動時にデータベースを初期化
@app.on_event("startup")
async def startup_event():
    init_dynamodb()

# CORS設定（Reactアプリケーションとの通信用）
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # React Vite開発サーバー
        "http://127.0.0.1:5173",  # React Vite開発サーバー（IP版）
        "http://localhost:8000",  # FastAPI
        "http://127.0.0.1:8000"   # FastAPI（IP版）
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# データモデル定義
class User(BaseModel):
    name: str
    email: str
    age: Optional[int] = None

class UserResponse(BaseModel):
    id: str  # DynamoDBではIDは文字列型
    name: str
    email: str
    age: Optional[int] = None


@app.get("/")
def read_root():
    return {"Hello": "World", "message": "FastAPI is running!"}


@app.get("/api/health")
def health_check():
    return {"status": "healthy", "timestamp": "2025-07-22"}


@app.get("/api/users")
def get_users():
    users = get_all_users()
    return {"users": users}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.post("/api/users", response_model=UserResponse)
def create_user(user: User):
    # データベースに新しいユーザーを保存
    new_user_data = db_create_user(user.name, user.email, user.age)
    return UserResponse(**new_user_data)


@app.get("/api/message")
def get_message():
    return {
        "message": "ReactからのAPIリクエストが成功しました！",
        "timestamp": "2025-07-22",
        "data": {
            "server": "FastAPI",
            "version": "0.116.1",
            "cors_enabled": True
        }
    }
