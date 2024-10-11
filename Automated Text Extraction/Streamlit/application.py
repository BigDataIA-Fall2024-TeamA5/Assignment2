import streamlit as st

# Set Streamlit page configuration first
st.set_page_config(page_title="PDF Text Extraction Application", layout="centered")

# Other imports after setting page config
import boto3
import mysql.connector
import pandas as pd
from dotenv import load_dotenv
import os
import sys

st.write("Python Executable Path:", sys.executable)

# Load environment variables from .env file
load_dotenv()

# Set up Streamlit page configuration and title (set_page_config should not be here)
st.title("PDF Text Extraction Application")

# Database Configuration from .env file
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Function to establish a connection to the database
def create_connection():
    """Establish a database connection to the Amazon RDS."""
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# Function to fetch all unique file names from merged_pdf table
def get_file_names():
    """Fetch unique file names from the merged_pdf table."""
    try:
        conn = create_connection()
        query = "SELECT DISTINCT file_name FROM merged_pdf"
        file_names_df = pd.read_sql(query, conn)
        conn.close()
        return file_names_df['file_name'].tolist()
    except Exception as e:
        st.error(f"Error fetching file names: {e}")
        return []

# Function to fetch questions based on the selected file name
def get_questions_for_file(file_name):
    """Fetch questions for the selected file from merged_pdf table."""
    try:
        conn = create_connection()
        query = "SELECT Question FROM merged_pdf WHERE file_name = %s"
        questions_df = pd.read_sql(query, conn, params=[file_name])
        conn.close()
        return questions_df['Question'].tolist()
    except Exception as e:
        st.error(f"Error fetching questions: {e}")
        return []

# Fetch all unique file names from the merged_pdf table
file_names = get_file_names()

# Display a dropdown menu for selecting a file name
if file_names:
    selected_file = st.selectbox("Select a PDF file:", file_names, help="Choose the PDF file you want to view questions for.")
else:
    st.warning("No files found in the merged_pdf table.")
    st.stop()

# Fetch questions for the selected file name
questions_list = get_questions_for_file(selected_file)

# Display the questions in a dropdown menu if available
if questions_list:
    selected_question = st.selectbox("Select a Question:", questions_list, help="Choose a question to view.")
else:
    st.warning(f"No questions found for the selected file: {selected_file}")
    st.stop()

# Display the selected question
st.subheader("Selected Question")
st.write(selected_question)
