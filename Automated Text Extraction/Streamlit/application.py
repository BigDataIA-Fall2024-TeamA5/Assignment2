# application.py
import streamlit as st
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Set up Streamlit page configuration and title
st.set_page_config(page_title="PDF Text Extraction Application", layout="centered")
st.title("PDF Text Extraction Application")

# FastAPI URL for the PDF list endpoint
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://127.0.0.1:8000/auth/pdf-list")

# Check if the user is logged in and JWT token is present
if 'access_token' not in st.session_state:
    st.warning("You need to login first. Please return to the main page and login.")
    st.stop()

# Use JWT token to make an authenticated request to the FastAPI endpoint
headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}
response = requests.get(FASTAPI_URL, headers=headers)

# Check response status and display the actual content of the response for debugging
st.write("FastAPI Response Status Code:", response.status_code)
st.write("FastAPI Response Content:", response.content)  # Display the raw response content

# Check response status and populate the PDF dropdown
if response.status_code == 200:
    pdf_files = response.json()  # Get the list of PDF files from response
    st.write("Parsed PDF Files List:", pdf_files)  # Display the parsed list for verification
    if not pdf_files:
        st.warning("No PDF files found in the S3 bucket.")
        st.stop()
else:
    st.error("Failed to retrieve PDF files. Please check your login status or backend configuration.")
    st.stop()

# Dropdown for selecting a PDF file
selected_pdf = st.selectbox("Select a PDF file:", pdf_files, help="Choose the PDF file you want to process.")
