import streamlit as st
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Set up Streamlit page configuration and title
st.set_page_config(page_title="PDF Text Extraction Application", layout="centered")
st.title("PDF Text Extraction Application")

# Correct FastAPI URL for the PDF list endpoint
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://127.0.0.1:8000/files/list-pdfs")

# Check if the user is logged in and JWT token is present
if 'access_token' not in st.session_state:
    st.warning("You need to login first. Please return to the main page and login.")
    st.stop()

# Initialize session state variables only once to avoid re-initialization
if 'selected_pdf' not in st.session_state:
    st.session_state['selected_pdf'] = None
if 'selected_extractor' not in st.session_state:
    st.session_state['selected_extractor'] = None
if 'pdf_files' not in st.session_state:
    st.session_state['pdf_files'] = []
    st.session_state['files_loaded'] = False  # Track if files are loaded

# Fetch PDF files only if they haven't been loaded already
def get_pdf_list():
    """Fetch the list of PDF files from the FastAPI endpoint."""
    headers = {"Authorization": f"Bearer {st.session_state['access_token']}"}
    try:
        # Make the GET request with authentication headers
        response = requests.get(FASTAPI_URL, headers=headers)
        if response.status_code == 200:
            # Extract and return the list of PDF files from the response
            return response.json().get("pdf_files", [])
        else:
            st.error(f"Failed to fetch PDF list from FastAPI. Status code: {response.status_code}.")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to FastAPI: {e}")
        return []

# Populate the PDF file list if not already loaded
if not st.session_state['files_loaded']:
    st.session_state['pdf_files'] = get_pdf_list()
    st.session_state['files_loaded'] = True  # Mark as loaded to prevent re-fetching

# Check if PDF files were successfully retrieved
if not st.session_state['pdf_files']:
    st.warning("No PDF files found in the specified S3 bucket folders.")
    st.stop()

# Define callbacks to update session state
def on_pdf_select():
    st.session_state['selected_pdf'] = st.session_state['pdf_dropdown']

def on_extractor_select():
    st.session_state['selected_extractor'] = st.session_state['extractor_dropdown']

# Dropdown for selecting a PDF file
st.selectbox(
    "Select a PDF file:", 
    st.session_state['pdf_files'], 
    help="Choose the PDF file you want to process.",
    key="pdf_dropdown",  # Use the same key as session state to maintain consistency
    index=0 if st.session_state['selected_pdf'] is None else st.session_state['pdf_files'].index(st.session_state['selected_pdf']),
    on_change=on_pdf_select  # Call this function whenever the selection changes
)

# Dropdown for selecting an extractor method
extractor_options = ["OpenAI", "PyPDF"]
st.selectbox(
    "Select an Extractor:", 
    extractor_options, 
    help="Choose the extraction method to use.",
    key="extractor_dropdown",  # Use the same key as session state to maintain consistency
    index=0 if st.session_state['selected_extractor'] is None else extractor_options.index(st.session_state['selected_extractor']),
    on_change=on_extractor_select  # Call this function whenever the selection changes
)

# Display selected values for debugging
st.write(f"You selected PDF: {st.session_state['selected_pdf']}")
st.write(f"You selected Extractor: {st.session_state['selected_extractor']}")

# Text area for inputting a question
select_question = st.text_area("Enter your question here (Optional):")

# Buttons to trigger actions
summary_button = st.button("Generate Summary")
generate_response = st.button("Generate Response")

# Debugging output
st.write("Page rendered successfully.")