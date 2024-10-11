import boto3
import os
from dotenv import load_dotenv

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

def generate_summary(pdf_name, extractor):
    """Fetch the summary for the selected PDF from S3."""
    # Define the folder prefixes based on the extractor type
    if extractor == "OpenAI":
        folder_prefix = "openai_extracts/"
    elif extractor == "PyPDF":
        folder_prefix = "pypdf2_folder/"
    else:
        return "Unknown extractor method."

    # Construct the S3 key based on the PDF name and extractor
    file_types = ['.json', '.csv', '.txt']
    s3_keys = [f"{folder_prefix}{pdf_name.replace('.pdf', file_ext)}" for file_ext in file_types]

    # Attempt to fetch the summary from one of the file types
    for s3_key in s3_keys:
        try:
            response = s3_client.get_object(Bucket=S3_BUCKET, Key=s3_key)
            file_content = response['Body'].read().decode('utf-8')
            return file_content
        except s3_client.exceptions.NoSuchKey:
            continue  # If key not found, try the next file type

    return "Summary not found for the selected PDF."