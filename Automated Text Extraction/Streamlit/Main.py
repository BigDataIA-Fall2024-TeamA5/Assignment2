# main.py in FastAPI

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from boto3 import client
from dotenv import load_dotenv
import os

# JWT Auth Setup
from Fastapi.jwtauth import router  
# Assuming this is for JWT-based authentication

# Load environment variables
load_dotenv()

# Initialize FastAPI application
app = FastAPI()

# Add CORS middleware to allow Streamlit to interact with FastAPI
origins = [
    "http://localhost:8501",  # Replace with your Streamlit app URL if needed
    "http://127.0.0.1:8501"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the JWT-based router for authentication
app.include_router(router, prefix="/auth")

# Fetch S3 configurations from environment variables
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
S3_PREFIX = os.getenv("S3_PREFIX")

# Create a boto3 S3 client
s3_client = client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI PDF Management Service!"}

# Endpoint to list PDF files in S3
@app.get("/list-pdfs")
async def list_pdfs():
    """Lists PDF files from the specified S3 bucket and folder."""
    try:
        # Use the S3 client to list the PDF files
        response = s3_client.list_objects_v2(Bucket=S3_BUCKET_NAME, Prefix=S3_PREFIX)
        pdf_files = [
            content["Key"].split("/")[-1]
            for content in response.get("Contents", [])
            if content["Key"].endswith(".pdf")
        ]
        return {"pdf_files": pdf_files} if pdf_files else {"message": "No PDF files found in S3 bucket."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")