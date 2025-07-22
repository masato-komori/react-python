from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# CORS設定（Reactアプリケーションとの通信用）
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://127.0.0.1:3000",
        "http://localhost:5173",  # Vite開発サーバー
        "http://127.0.0.1:5173"   # Vite開発サーバー
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
    id: int
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
    return {
        "users": [
            {"id": 1, "name": "田中太郎", "email": "tanaka@example.com"},
            {"id": 2, "name": "佐藤花子", "email": "sato@example.com"},
            {"id": 3, "name": "山田次郎", "email": "yamada@example.com"}
        ]
    }


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.post("/api/users", response_model=UserResponse)
def create_user(user: User):
    # 実際のアプリケーションではデータベースに保存します
    new_user = UserResponse(
        id=999,  # 仮のID
        name=user.name,
        email=user.email,
        age=user.age
    )
    return new_user


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
