from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import boto3
import openai
import json
import pdfplumber
import pandas as pd
from io import BytesIO
import os

# AWS S3 Configuration
s3BucketName = 'textextractionfrompdf'
s3InputPrefix = 'GAIA-Dataset/'
outputPrefix = 'openai_extracts/'  # Output folder for extracted files in S3

# Set up AWS S3 client
s3Client = boto3.client('s3')

# Set OpenAI API key (ensure the key is stored securely)
openai.api_key = os.getenv("OPENAI_API_KEY")  # Or you can directly provide your API key here

# Default DAG arguments
defaultArgs = {
    'owner': 'airflow',
    'start_date': datetime(2024, 10, 1),
    'retries': 1,
}

# Define the DAG
dag = DAG(
    dag_id='s3_openai_extraction_pipeline',
    default_args=defaultArgs,
    description='A pipeline to extract data from PDF files using pdfplumber and OpenAI API',
    schedule='@daily',
    catchup=False,
)


# Task 1: List and Select PDF Files from S3
def list_pdf_files_from_s3(**kwargs):
    """List PDF files from both 'test' and 'validation' subfolders in the S3 bucket."""
    pdf_files = []
    for subfolder in ['test/', 'validation/']:
        response = s3Client.list_objects_v2(Bucket=s3BucketName, Prefix=f"{s3InputPrefix}{subfolder}")
        folder_files = [content['Key'] for content in response.get('Contents', []) if content['Key'].endswith('.pdf')]
        pdf_files.extend(folder_files)

    print(f"Found {len(pdf_files)} PDF files in S3.")
    kwargs['ti'].xcom_push(key='pdf_files', value=pdf_files)


# Task 2: Extract Text and Table Data using pdfplumber
def extract_data_with_pdfplumber(**kwargs):
    """Extract text and table data from the PDF using pdfplumber and send text to OpenAI for further extraction."""
    pdf_files = kwargs['ti'].xcom_pull(key='pdf_files', task_ids='list_pdf_files_from_s3')

    for s3_file in pdf_files:
        # Read PDF file directly from S3 into memory using BytesIO
        response = s3Client.get_object(Bucket=s3BucketName, Key=s3_file)
        pdf_content = response['Body'].read()

        # Open the PDF with pdfplumber
        with pdfplumber.open(BytesIO(pdf_content)) as pdf:
            for page_num, page in enumerate(pdf.pages):
                # Check if the page contains tables
                tables = page.extract_tables()
                if tables and len(tables) > 0:
                    # Extract tables and save as CSV
                    save_table_as_csv(tables, s3_file, page_num)
                else:
                    # Extract text and send it to OpenAI for structured extraction
                    text = page.extract_text()
                    if text:
                        process_text_with_openai(text, s3_file, page_num)


# Task 3: Process Text Using OpenAI API
def process_text_with_openai(text, s3_file, page_num):
    """Use OpenAI API to extract structured information from the text."""
    # Define a structured prompt for OpenAI API
    prompt = f"""
    You are a powerful document data extraction tool. Extract the relevant information from the following text:
    
    {text}
    
    Return the result as a structured JSON object, preserving the format and context of the original document.
    """

    # Call OpenAI API
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Use your preferred OpenAI model
            prompt=prompt,
            max_tokens=500,
            temperature=0.0,
        )
        structured_data = response.choices[0].text.strip()

        # Save the structured data as JSON
        save_text_as_json(structured_data, s3_file, page_num)

    except Exception as e:
        print(f"OpenAI API Error for file {s3_file}, page {page_num}: {e}")


# Function to save table data as a CSV in S3
def save_table_as_csv(tables, s3_file, page_num):
    """Save extracted table data as a CSV file in S3."""
    for i, table in enumerate(tables):
        df = pd.DataFrame(table[1:], columns=table[0])
        csv_data = df.to_csv(index=False, header=True)
        csvFileName = s3_file.split('/')[-1].replace('.pdf', f'_page{page_num}_table{i}.csv')
        s3Client.put_object(Bucket=s3BucketName, Key=f"{outputPrefix}{csvFileName}", Body=csv_data)
        print(f"Table {i} on Page {page_num} saved as CSV for file {s3_file}.")


# Function to save extracted text as JSON in S3
def save_text_as_json(text, s3_file, page_num):
    """Store extracted text or structured OpenAI response in JSON format in S3."""
    json_data = json.dumps({'page_num': page_num, 'content': text}, indent=4)
    jsonFileName = s3_file.split('/')[-1].replace('.pdf', f'_page{page_num}.json')
    s3Client.put_object(Bucket=s3BucketName, Key=f"{outputPrefix}{jsonFileName}", Body=json_data)
    print(f"Text on Page {page_num} saved as JSON for file {s3_file}.")


# Define Airflow Tasks
listFilesTask = PythonOperator(task_id='list_pdf_files_from_s3', python_callable=list_pdf_files_from_s3, dag=dag)
extractDataTask = PythonOperator(task_id='extract_data_with_pdfplumber', python_callable=extract_data_with_pdfplumber, dag=dag)

# Set Task Dependencies
listFilesTask >> extractDataTask