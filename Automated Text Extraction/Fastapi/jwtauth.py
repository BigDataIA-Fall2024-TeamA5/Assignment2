from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta, timezone
import hmac, hashlib, jwt
from typing import Dict
import mysql.connector
from mysql.connector import Error

# Create the APIRouter instance
router = APIRouter()

# Define security for bearer tokens
security = HTTPBearer()

SECRET_KEY = "abc"

# Database connection configuration
DB_CONFIG = {
    'host': 'database-1.cb4iuicksa3s.us-east-2.rds.amazonaws.com',
    'user': 'admin',
    'password': 'damg7245bigdata',
    'database': 'textextraction'
}

# Function to create a database connection
def create_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

# JWT Token Functions
def hash_password(password: str) -> str:
    return hmac.new(SECRET_KEY.encode(), msg=password.encode(), digestmod=hashlib.sha256).hexdigest()

def create_jwt_token(data: dict):
    expiration = datetime.now(timezone.utc) + timedelta(minutes=50)
    token_payload = {"exp": expiration, **data}
    token = jwt.encode(token_payload, SECRET_KEY, algorithm="HS256")
    return token, expiration

def decode_jwt_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

# Function to get user from database
def get_user_from_db(username: str):
    connection = create_db_connection()
    if connection is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database connection failed")
    
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        return user
    except Error as e:
        print(f"Error fetching user from database: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Define a function to get the current user based on the JWT
def get_current_user(authorization: HTTPAuthorizationCredentials = Depends(security)):
    token = authorization.credentials
    payload = decode_jwt_token(token)
    username = payload.get("username")
    user = get_user_from_db(username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

# Define login endpoint
@router.post("/login")
def login(username: str, password: str):
    user = get_user_from_db(username)
    if user and user["hashed_password"] == hash_password(password):
        token, expiration = create_jwt_token({"username": username})
        return {"access_token": token, "token_type": "bearer", "expires": expiration.isoformat()}
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

# Define registration endpoint
@router.post("/register")
def register(username: str, email: str, password: str):
    connection = create_db_connection()
    if connection is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database connection failed")
    
    try:
        cursor = connection.cursor()
        hashed_password = hash_password(password)
        query = "INSERT INTO users (username, email, hashed_password) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, email, hashed_password))
        connection.commit()
        return {"message": "User registered successfully"}
    except Error as e:
        print(f"Error registering user: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to register user")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Define a protected endpoint
@router.get("/protected")
def protected_route(current_user: Dict = Depends(get_current_user)):
    return {"message": f"Hello, {current_user['username']}!"}