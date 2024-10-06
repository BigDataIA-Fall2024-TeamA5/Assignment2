import streamlit as st

# Set up session state to track login status and other states
if 'is_logged_in' not in st.session_state:
    st.session_state['is_logged_in'] = False

if 'selected_pdf' not in st.session_state:
    st.session_state['selected_pdf'] = None

if 'result' not in st.session_state:
    st.session_state['result'] = ""

# A list of PDFs (simulated) for the dropdown. In a real app, this would come from S3.
pdf_list = ["PDF1.pdf", "PDF2.pdf", "PDF3.pdf"]

# Unique Style for the app using Streamlit options
st.set_page_config(page_title="PDF Query App", page_icon="📄", layout="wide")

# Hardcoded credentials for login
HARDCODED_USERNAME = "user"
HARDCODED_PASSWORD = "password"

# Login function (with hardcoded credentials)
def login_user(username, password):
    if username == HARDCODED_USERNAME and password == HARDCODED_PASSWORD:
        return True
    else:
        return False

# Function to clear the output
def clear_output():
    st.session_state['result'] = ""

# Function to log out
def logout():
    st.session_state['is_logged_in'] = False
    st.session_state['selected_pdf'] = None
    st.experimental_rerun()

# Main Application

# --- Login Page ---
if not st.session_state['is_logged_in']:
    st.title("🔒 Login to PDF Query System")
    
    # User input for login
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    # Login button
    if st.button("Login"):
        if login_user(username, password):
            st.session_state['is_logged_in'] = True
            st.success("Login successful!")
            st.experimental_rerun()  # Reload to show the main interface
        else:
            st.error("Invalid username or password.")

# --- Main Interface (After Login) ---
else:
    # Welcome Header
    st.title("📄 PDF Query Interface")
    st.markdown("Welcome! You can select a PDF or query across all PDFs.")

    # Layout for Question Input and PDF selection
    with st.form(key="query_form"):
        st.subheader("Ask Your Question")
        
        # Input for user's question
        query = st.text_input("Enter your question here:")
        
        # Dropdown to select preprocessed PDF (simulated)
        selected_pdf = st.selectbox("Select a PDF (Optional)", ["All PDFs"] + pdf_list)
        
        # Submit button to submit the query
        submit_button = st.form_submit_button(label="Submit Question")
        
        # Handle form submission (without backend functionality for now)
        if submit_button:
            if query:
                if selected_pdf == "All PDFs":
                    st.session_state['result'] = f"Searching in all PDFs for: {query}"
                else:
                    st.session_state['result'] = f"Searching in {selected_pdf} for: {query}"
            else:
                st.warning("Please enter a question.")

    # Display the result of the query
    if st.session_state['result']:
        st.write("**Query Result:**")
        st.text(st.session_state['result'])

    # Buttons for clearing output and logging out
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Clear"):
            clear_output()
    with col2:
        if st.button("Logout"):
            logout()