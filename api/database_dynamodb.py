import boto3
from botocore.exceptions import ClientError
import json
from decimal import Decimal
import os

# DynamoDB Local設定
DYNAMODB_ENDPOINT = "http://dynamodb-local:8001"
AWS_REGION = "us-east-1"

# ダミー認証情報（DynamoDB Localでは実際の認証は不要）
os.environ['AWS_ACCESS_KEY_ID'] = 'dummy'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'dummy'

def get_dynamodb():
    """DynamoDB クライアントを取得"""
    return boto3.resource(
        'dynamodb',
        endpoint_url=DYNAMODB_ENDPOINT,
        region_name=AWS_REGION
    )

def init_dynamodb():
    """DynamoDBテーブルの作成と初期データの挿入"""
    dynamodb = get_dynamodb()
    
    table_name = 'Users'
    
    try:
        # テーブルが存在するかチェック
        table = dynamodb.Table(table_name)
        table.load()
        print(f"Table {table_name} already exists")
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            # テーブルを作成
            table = dynamodb.create_table(
                TableName=table_name,
                KeySchema=[
                    {
                        'AttributeName': 'id',
                        'KeyType': 'HASH'
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'id',
                        'AttributeType': 'S'
                    }
                ],
                BillingMode='PAY_PER_REQUEST'
            )
            
            # テーブルが作成されるまで待機
            table.wait_until_exists()
            print(f"Table {table_name} created successfully")
            
            # サンプルデータを挿入
            sample_users = [
                {
                    'id': '1',
                    'name': '田中太郎',
                    'email': 'tanaka@example.com',
                    'age': 30
                },
                {
                    'id': '2',
                    'name': '佐藤花子',
                    'email': 'sato@example.com',
                    'age': 25
                },
                {
                    'id': '3',
                    'name': '山田次郎',
                    'email': 'yamada@example.com',
                    'age': 35
                }
            ]
            
            # バッチでデータを挿入
            with table.batch_writer() as batch:
                for user in sample_users:
                    batch.put_item(Item=user)
            
            print("Sample data inserted successfully")
        else:
            raise e
    
    return table

def get_all_users():
    """全ユーザーを取得"""
    dynamodb = get_dynamodb()
    table = dynamodb.Table('Users')
    
    try:
        response = table.scan()
        users = response['Items']
        
        # DynamoDB の Decimal 型を int に変換
        for user in users:
            if 'age' in user and isinstance(user['age'], Decimal):
                user['age'] = int(user['age'])
        
        return users
    except ClientError as e:
        print(f"Error fetching users: {e}")
        return []

def create_user(name: str, email: str, age: int = None):
    """新しいユーザーを作成"""
    dynamodb = get_dynamodb()
    table = dynamodb.Table('Users')
    
    # 新しいIDを生成（簡易実装）
    import uuid
    user_id = str(uuid.uuid4())
    
    user_data = {
        'id': user_id,
        'name': name,
        'email': email
    }
    
    if age is not None:
        user_data['age'] = age
    
    try:
        table.put_item(Item=user_data)
        return user_data
    except ClientError as e:
        print(f"Error creating user: {e}")
        raise e

def get_user_by_id(user_id: str):
    """IDでユーザーを取得"""
    dynamodb = get_dynamodb()
    table = dynamodb.Table('Users')
    
    try:
        response = table.get_item(Key={'id': user_id})
        if 'Item' in response:
            user = response['Item']
            # DynamoDB の Decimal 型を int に変換
            if 'age' in user and isinstance(user['age'], Decimal):
                user['age'] = int(user['age'])
            return user
        return None
    except ClientError as e:
        print(f"Error fetching user: {e}")
        return None

if __name__ == "__main__":
    init_dynamodb()
    print("DynamoDB initialized successfully!")
