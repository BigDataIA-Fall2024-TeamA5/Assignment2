import boto3
import pandas as pd
from sqlalchemy import create_engine
from datasets import load_dataset
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# AWS S3 Configuration
s3BucketName = os.getenv("S3_BUCKET_NAME")  
s3TestPrefix = os.getenv("S3_TEST_PREFIX")  
s3ValidationPrefix = os.getenv("S3_VALIDATION_PREFIX")

# RDS Configuration
rdsHost = os.getenv("RDS_HOST")
rdsPort = os.getenv("RDS_PORT")
rdsDatabase = os.getenv("RDS_DATABASE")
rdsUser = os.getenv("RDS_USER")
rdsPassword = os.getenv("RDS_PASSWORD")

# Initialize the AWS S3 client
s3Client = boto3.client('s3')

# Step 1: Load Hugging Face Dataset CSVs
def load_huggingface_csv(dataset_name, subset_name):
    # Load the dataset using the `datasets` library
    ds = load_dataset(dataset_name, subset_name)
    # Convert the Hugging Face dataset to a Pandas DataFrame
    df = ds['train'].to_pandas()
    return df

# Step 2: Get list of PDF files from S3 (both test and validation folders)
def get_pdf_files_from_s3(bucket_name, prefixes):
    pdf_files = []
    for prefix in prefixes:
        response = s3Client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        pdf_files.extend([content['Key'].split('/')[-1] for content in response.get('Contents', []) if content['Key'].endswith('.pdf')])
    return pdf_files

# Step 3: Filter Hugging Face dataset based on matching PDF names from S3
def filter_dataset_by_s3_files(hf_df, s3_pdf_files):
    # Filter the DataFrame based on the 'file_name' column matching the PDF files in S3
    filtered_df = hf_df[hf_df['file_name'].isin(s3_pdf_files)]
    return filtered_df

# Step 4: Insert filtered data into Amazon RDS SQL table
def insert_into_rds(filtered_df, table_name='pdf_metadata'):
    # Create an SQLAlchemy engine to connect to Amazon RDS
    engine = create_engine(f'postgresql://{rdsUser}:{rdsPassword}@{rdsHost}:{rdsPort}/{rdsDatabase}')
    
    # Insert data into the RDS table
    filtered_df.to_sql(table_name, engine, if_exists='append', index=False)
    print(f"Inserted {len(filtered_df)} rows into the RDS table '{table_name}'.")

# Step 5: Define the main workflow
def main():
    # 1. Load the Hugging Face dataset
    print("Loading Hugging Face dataset...")
    huggingface_df = load_huggingface_csv("gaia-benchmark/GAIA", "2023_all")
    print(f"Hugging Face dataset loaded with {len(huggingface_df)} rows.")

    # 2. Get the list of PDF files from both test and validation folders in S3
    print("Fetching PDF files from S3...")
    pdf_files_in_s3 = get_pdf_files_from_s3(s3BucketName, [s3TestPrefix, s3ValidationPrefix])
    print(f"PDF files found in S3: {pdf_files_in_s3}")

    # 3. Filter the Hugging Face dataset to include only matching files
    print("Filtering Hugging Face dataset based on S3 files...")
    filtered_data = filter_dataset_by_s3_files(huggingface_df, pdf_files_in_s3)
    print(f"Filtered Data:\n{filtered_data}")

    # 4. Insert the filtered data into Amazon RDS
    if not filtered_data.empty:
        print("Inserting filtered data into Amazon RDS...")
        insert_into_rds(filtered_data)
    else:
        print("No matching rows found for the PDF files in S3.")

# Run the main workflow
if __name__ == "__main__":
    main()