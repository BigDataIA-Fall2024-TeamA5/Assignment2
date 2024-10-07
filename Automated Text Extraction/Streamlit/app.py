import streamlit as st

# Set up session state to track login status and other states
if 'is_logged_in' not in st.session_state:
    st.session_state['is_logged_in'] = False

if 'selected_pdf' not in st.session_state:
    st.session_state['selected_pdf'] = None

if 'result' not in st.session_state:
    st.session_state['result'] = ""

if 'query' not in st.session_state:
    st.session_state['query'] = ""

# A list of PDFs (simulated) for the dropdown. In a real app, this would come from S3.
pdf_list = ["PDF1.pdf", "PDF2.pdf", "PDF3.pdf"]

# Unique Style for the app using Streamlit options
st.set_page_config(page_title="PDF Query App", page_icon="📄", layout="wide")

# Hardcoded credentials for login
HARDCODED_USERNAME = "user"
HARDCODED_PASSWORD = "password"

# FastAPI URL endpoints 
# BASE_URL = "http://your_fastapi_backend_url"
# LOGIN_URL = f"{BASE_URL}/login"
# QUERY_URL = f"{BASE_URL}/submit_query"
# PDF_LIST_URL = f"{BASE_URL}/get_preprocessed_pdfs"

# Login function with FastAPI integration 
# def login_user(username, password):
#     # Call FastAPI to verify credentials
#     response = requests.post(LOGIN_URL, json={"username": username, "password": password})
#     if response.status_code == 200:
#         return response.json()["access_token"]  # You can also store this in session state
#     else:
#         return None

# Login function 
def login_user(username, password):
    if username == HARDCODED_USERNAME and password == HARDCODED_PASSWORD:
        return True
    else:
        return False

# Function to log out
def logout():
    st.session_state['is_logged_in'] = False
    st.session_state['selected_pdf'] = None
    st.session_state['query'] = ""
    st.session_state['result'] = ""
    st.experimental_rerun()

# Main Application

# Login Page
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

# Main Interface 
else:
    # Welcome Header
    st.title("📄 PDF Query Interface")
    st.markdown("Welcome! You can select a PDF or query across all PDFs.")

    # Fetch PDF List from FastAPI 
    # pdf_list = requests.get(PDF_LIST_URL).json()

    # Layout for Question Input and PDF selection
    with st.form(key="query_form"):
        st.subheader("Ask Your Question")
        
        # Input for user's question
        query = st.text_input("Enter your question here:", value=st.session_state['query'])
        
        # Dropdown to select preprocessed PDF 
        selected_pdf = st.selectbox("Select a PDF (Optional)", ["All PDFs"] + pdf_list, index=pdf_list.index(st.session_state['selected_pdf']) if st.session_state['selected_pdf'] in pdf_list else 0)
        
        # Submit button to submit the query
        submit_button = st.form_submit_button(label="Submit Question")
        
        # Handle form submission
        if submit_button:
            if query:
                st.session_state['query'] = query  # Save query in session state
                st.session_state['selected_pdf'] = selected_pdf  # Save selected PDF in session state
                
                if selected_pdf == "All PDFs":
                    # FastAPI Query submission (commented out)
                    # headers = {"Authorization": f"Bearer {st.session_state['jwt_token']}"}
                    # response = requests.post(QUERY_URL, json={"query": query, "pdf": selected_pdf}, headers=headers)
                    # st.session_state['result'] = response.json()["result"]

                    st.session_state['result'] = f"Searching in all PDFs for: {query}"
                else:
                    # FastAPI Query submission (commented out)
                    # headers = {"Authorization": f"Bearer {st.session_state['jwt_token']}"}
                    # response = requests.post(QUERY_URL, json={"query": query, "pdf": selected_pdf}, headers=headers)
                    # st.session_state['result'] = response.json()["result"]

                    st.session_state['result'] = f"Searching in {selected_pdf} for: {query}"
            else:
                st.warning("Please enter a question.")

    # Display the result of the query
    if st.session_state['result']:
        st.write("**Query Result:**")
        st.text(st.session_state['result'])

    # Logout button
    if st.button("Logout"):
        logout()

