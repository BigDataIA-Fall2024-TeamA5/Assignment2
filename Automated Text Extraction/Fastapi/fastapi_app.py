# fastapi_app.py
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from jwtauth import auth_router, get_current_user  # Ensure `jwtauth` is correctly imported
import boto3
from typing import List
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# AWS S3 Configuration
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
REGION_NAME = os.getenv("AWS_DEFAULT_REGION")
S3_BUCKET = os.getenv("S3_BUCKET_NAME")

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=REGION_NAME
)

# Create FastAPI app
app = FastAPI()

# CORS Configuration
origins = [
    "http://localhost:8501",
    "http://127.0.0.1:8501"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include auth-related routes from jwtauth.py
app.include_router(auth_router, prefix="/auth")

# Debugging: Root endpoint to verify the application is running correctly
@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI JWT Authentication Application!"}

# Endpoint to get the list of PDFs from S3
@app.get("/auth/pdf-list", response_model=List[str], dependencies=[Depends(get_current_user)])
async def get_pdf_list():
    """Fetch and return the list of PDF files from the S3 bucket."""
    try:
        response = s3_client.list_objects_v2(Bucket=S3_BUCKET)
        pdf_files = [file['Key'] for file in response.get('Contents', []) if file['Key'].endswith('.pdf')]
        return pdf_files
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to fetch PDFs: {e}")
