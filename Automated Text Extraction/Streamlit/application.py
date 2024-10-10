import streamlit as st
import requests

# Set up page configuration and title
st.set_page_config(page_title="PDF Text Extraction Application", layout="centered")
st.title("PDF Text Extraction Application")

# FastAPI URL to fetch the list of PDF files
FASTAPI_URL = "http://localhost:8000/list-pdfs"

# Function to fetch the list of PDFs from the FastAPI endpoint
def get_pdf_files():
    try:
        response = requests.get(FASTAPI_URL)
        if response.status_code == 200:
            return response.json().get("pdf_files", [])
        else:
            st.error(f"Failed to fetch PDF files: {response.json().get('detail', 'Unknown error')}")
            return []
    except Exception as e:
        st.error(f"Error: {e}")
        return []

# Fetch PDF files from FastAPI
pdf_files = get_pdf_files()

# Dropdown for PDF selection
selected_pdf = st.selectbox("Select a PDF file:", pdf_files, help="Choose the PDF file you want to process.")

# Dropdown for text extraction method selection
methods = ["PyPDF", "OpenAI Text Extraction"]
selected_method = st.selectbox("Select text extraction method:", methods, help="Select the method for extracting text.")

# Define placeholder extraction functions for each method
def extract_text_pypdf(pdf_file):
    # Placeholder logic for PyPDF text extraction
    return f"Extracted text from {pdf_file} using PyPDF."

def extract_text_openai(pdf_file):
    # Placeholder logic for OpenAI-based text extraction
    return f"Extracted text from {pdf_file} using OpenAI Text Extraction."

# Button to trigger text extraction and summarization
if st.button("Get Summary"):
    # Implement the logic to extract text and summarize based on the selected method
    if selected_method == "PyPDF":
        summary = extract_text_pypdf(selected_pdf)
    elif selected_method == "OpenAI Text Extraction":
        summary = extract_text_openai(selected_pdf)
    
    # Display the extracted summary
    st.subheader("Extracted Summary")
    st.write(summary)