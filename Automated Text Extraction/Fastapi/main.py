from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from Fastapi.jwtauth import router  # Ensure jwtauth.py has a `router` defined
import boto3
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch AWS and S3 configurations from environment variables
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
S3_BASE_PREFIX = os.getenv("S3_PREFIX", "GAIA-Dataset/")  # Base folder in S3, default to GAIA_DATASET

# Define S3 subfolders to search for PDFs
S3_SUBFOLDERS = ["test/", "validation/"]

# Create a boto3 client using environment variables
s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
)

# Create FastAPI app instance
app = FastAPI()

# Set up CORS configuration
origins = [
    "http://localhost:8501",  # For Streamlit frontend
    "http://localhost:8000",  # For FastAPI backend
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

# Root route
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI JWT Authentication Application!"}

# Route to list PDF files from both `test` and `validation` folders in S3 bucket
@app.get("/list-pdfs")
async def list_pdfs():
    """Lists PDF files from the specified S3 bucket and subfolders."""
    pdf_files = []  # Store all PDF file names

    try:
        # Iterate through each subfolder (test and validation)
        for subfolder in S3_SUBFOLDERS:
            # List objects in the specified subfolder
            response = s3_client.list_objects_v2(Bucket=S3_BUCKET_NAME, Prefix=f"{S3_BASE_PREFIX}{subfolder}")
            
            # Extract PDF file names from the response
            folder_pdfs = [
                content["Key"].split("/")[-1]
                for content in response.get("Contents", [])
                if content["Key"].endswith(".pdf")
            ]
            
            # Add the files found in the current subfolder to the main list
            pdf_files.extend(folder_pdfs)

        # Return the combined list of PDF files
        return {"pdf_files": pdf_files} if pdf_files else {"message": "No PDF files found in the specified S3 bucket."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")

# Additional routes can be defined as needed