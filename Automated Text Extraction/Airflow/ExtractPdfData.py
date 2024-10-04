from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import boto3
import json
import requests
from PyPDF2 import PdfReader
from io import BytesIO
import openai

# Set up AWS S3 client
s3Client = boto3.client('s3')

# Define constants
s3BucketName = 'textextractionfrompdf'  # Update with your actual S3 bucket name
s3InputPrefix = 'gaia-dataset/'  # Folder in the S3 bucket where PDF files are stored
fastApiEndpoint = "http://fastapi_container:8000/process-json"  # Update with your FastAPI endpoint

# Set up OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Default DAG arguments
defaultArgs = {
    'owner': 'airflow',
    'start_date': datetime(2024, 10, 1),
    'retries': 1
}

# Define the DAG
dag = DAG(
    dag_id='extractPdfDataPipeline',
    default_args=defaultArgs,
    description='A pipeline to extract data from PDF files in S3 and send directly to API',
    schedule_interval='@daily',
)

# Task 1: List PDF files in the S3 bucket
def listPdfFiles(**kwargs):
    response = s3Client.list_objects_v2(Bucket=s3BucketName, Prefix=s3InputPrefix)
    pdfFiles = [content['Key'] for content in response.get('Contents', []) if content['Key'].endswith('.pdf')]
    return pdfFiles

# Task 2: Extract text and metadata directly from S3 PDFs using selected extractor
def extractPdfData(pdfFiles, extractorType='PyPDF2', **kwargs):
    extractedData = []

    # Process each PDF file in the S3 bucket
    for pdfFile in pdfFiles:
        try:
            # Read PDF file directly from S3 into memory using BytesIO
            response = s3Client.get_object(Bucket=s3BucketName, Key=pdfFile)
            pdfContent = response['Body'].read()
            metadata = {}
            text = ''

            if extractorType == 'PyPDF2':
                # Extract using PyPDF2
                reader = PdfReader(BytesIO(pdfContent))
                for page in reader.pages:
                    text += page.extract_text()
                metadata = reader.metadata

            elif extractorType == 'OpenAI':
                # Extract using OpenAI's Document Extractor API
                openaiResponse = openai.File.create(file=BytesIO(pdfContent), purpose='answers')
                text = openaiResponse['data']
                metadata = {'OpenAI': 'Extracted using OpenAI'}

            # Append extracted data to the list
            extractedData.append({
                'fileName': pdfFile,
                'metadata': metadata,
                'text': text
            })

        except Exception as e:
            print(f"Error processing {pdfFile}: {e}")

    return extractedData  # Return the extracted data directly

# Task 3: Send extracted data to FastAPI for further processing
def sendToApi(extractedData, **kwargs):
    response = requests.post(fastApiEndpoint, json=extractedData)
    if response.status_code == 200:
        print(f"Successfully sent extracted data to {fastApiEndpoint}")
    else:
        print(f"Failed to send data to API. Status code: {response.status_code}, Error: {response.text}")

# Define Airflow tasks
listFilesTask = PythonOperator(
    task_id='listPdfFiles',
    python_callable=listPdfFiles,
    provide_context=True,
    dag=dag
)

extractDataTask = PythonOperator(
    task_id='extractPdfData',
    python_callable=extractPdfData,
    provide_context=True,
    op_kwargs={
        'pdfFiles': "{{ task_instance.xcom_pull(task_ids='listPdfFiles') }}",
        'extractorType': 'OpenAI'  # Choose 'PyPDF2' or 'OpenAI' dynamically
    },
    dag=dag
)

sendToApiTask = PythonOperator(
    task_id='sendToApi',
    python_callable=sendToApi,
    provide_context=True,
    op_kwargs={'extractedData': "{{ task_instance.xcom_pull(task_ids='extractPdfData') }}"},
    dag=dag
)

# Set up task dependencies
listFilesTask >> extractDataTask >> sendToApiTask