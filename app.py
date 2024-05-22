from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import boto3
from botocore.exceptions import ClientError

app = FastAPI()

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('MyDynamoDBTable2')

class User(BaseModel):
    id: int
    name: str
    email: str
    address: str

@app.post("/users/")
def create_user(user: User):
    try:
        table.put_item(Item=user.dict())
        return {"message": "User created successfully", "user": user}
    except ClientError as e:
        raise HTTPException(status_code=500, detail=e.response['Error']['Message'])

@app.get("/users/{user_id}")
def get_user(user_id: int):
    try:
        response = table.get_item(Key={'id': user_id})
        if 'Item' in response:
            return response['Item']
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except ClientError as e:
        raise HTTPException(status_code=500, detail=e.response['Error']['Message'])

@app.put("/users/{user_id}")
def update_user(user_id: int, updated_user: User):
    try:
        response = table.get_item(Key={'id': user_id})
        if 'Item' in response:
            table.put_item(Item=updated_user.dict())
            return {"message": "User updated successfully", "user": updated_user}
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except ClientError as e:
        raise HTTPException(status_code=500, detail=e.response['Error']['Message'])

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    try:
        response = table.get_item(Key={'id': user_id})
        if 'Item' in response:
            table.delete_item(Key={'id': user_id})
            return {"message": "User deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except ClientError as e:
        raise HTTPException(status_code=500, detail=e.response['Error']['Message'])

@app.get("/users/")
def list_users():
    try:
        response = table.scan()
        return response.get('Items', [])
    except ClientError as e:
        raise HTTPException(status_code=500, detail=e.response['Error']['Message'])
