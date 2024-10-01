import boto3
import os
from datasets import load_dataset

# Load the GAIA dataset from Hugging Face
ds = load_dataset("gaia-benchmark/GAIA", "2023_all")

# Print the dataset structure to confirm the correct keys
print("Dataset Structure:", ds)

# Use the correct keys based on the dataset structure
target_directories = ["test", "validation"]

# Define S3 bucket and base path
s3_bucket_name = 'textextractionfrompdf'
s3_base_path = 'GAIA-Dataset/'

# Initialize S3 client
s3_client = boto3.client('s3')

# Function to upload PDF files to S3
def upload_pdf_files_to_s3(dataset, directories, bucket_name, base_path):
    for directory in directories:
        print(f"Processing directory: {directory}")
        
        # Ensure the directory exists in the dataset
        if directory not in dataset:
            print(f"Directory {directory} not found in the dataset. Skipping...")
            continue

        # Access files in the directory
        for file in dataset[directory]:
            file_name = file['file_name']
            file_path = file['file_path']  # Use the file path to locate the file

            # Check if the file is a PDF
            if file_name.lower().endswith(".pdf"):
                # Upload the file to S3 using its file path
                s3_file_path = os.path.join(base_path, directory, file_name)

                try:
                    # Upload the PDF file directly from the local path or dataset path
                    s3_client.upload_file(file_path, bucket_name, s3_file_path)
                    print(f"Uploaded {file_name} to s3://{bucket_name}/{s3_file_path}")
                except FileNotFoundError:
                    print(f"File {file_path} not found. Skipping...")
            else:
                print(f"Skipping non-PDF file: {file_name}")

# Execute the PDF upload process
upload_pdf_files_to_s3(ds, target_directories, s3_bucket_name, s3_base_path)