import streamlit as st

# Set up session state to track login status, signup, and other states
if 'is_logged_in' not in st.session_state:
    st.session_state['is_logged_in'] = False

if 'is_signing_up' not in st.session_state:
    st.session_state['is_signing_up'] = False


if 'selected_pdf' not in st.session_state:
    st.session_state['selected_pdf'] = None

if 'result' not in st.session_state:
    st.session_state['result'] = ""


if 'query' not in st.session_state:
    st.session_state['query'] = ""


# A list of PDFs (simulated) for the dropdown. In a real app, this would come from S3.
pdf_list = ["PDF1.pdf", "PDF2.pdf", "PDF3.pdf"]


# Unique Style for the app using Streamlit options
st.set_page_config(page_title="PDF Query App", page_icon="📄", layout="centered")


# Hardcoded credentials for login
HARDCODED_USERNAME = "user"
HARDCODED_PASSWORD = "password"


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



# Function to go back to the login page after registration
def return_to_login():
    st.session_state['is_signing_up'] = False
    st.experimental_rerun()


# Function to handle signup
def signup_user(username, fullname, password):
    # Simulate registration. In a real application, this would store the user details.
    st.success(f"Account created for {fullname} with username: {username}")
    st.session_state['is_signing_up'] = False


st.markdown("""
    <style>
       
    /* Align title to center and make it blue */
    .title {
        text-align: center;
        color: blue; /* Change title text color to blue */
        font-size: 10px; /* Adjust the size of the title text */
    }
   
    /* Reduce overall size of the button */
    .stButton > button {
        width: 100%; /* Make button fit the container */
        max-width: 100px; /* Set max width for smaller buttons */
        margin: 10px auto; /* Adjust margin for spacing */
        padding: 8px; /* Reduce padding for a smaller button */
        background-color: #4CAF50; /* Button background color */
        color: white; /* Button text color */
        border: none;
        border-radius: 8px; /* Rounded button corners */
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2); /* Shadow for the button */
    }




    /* Reduce input field size */
    input[type="text"], input[type="password"] {
        font-size: 14px; /* Adjust font size inside the text fields */
        padding: 8px; /* Adjust padding */
        width: 100%; /* Make input fields fill their container */
        max-width: 300px; /* Set a maximum width for the input fields */
        margin: 0 auto; /* Center the input fields */
        display: block; /* Ensure it behaves like a block element */
    }
           
       
           
    }


 </style>
    """, unsafe_allow_html=True)



# If the user is signing up, show the signup page
if st.session_state['is_signing_up']:
    st.markdown("<h3 style='text-align: center; color: blue;'>📝 Sign Up Page</h3>", unsafe_allow_html=True)


# Signup form design
    with st.form("signup_form", clear_on_submit=True):
        st.markdown('<div class="centered-box">', unsafe_allow_html=True)
        fullname = st.text_input("Full Name")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        st.markdown('</div>', unsafe_allow_html=True)
       
        if st.form_submit_button("Register"):
            if username and fullname and password:
                signup_user(username, fullname, password)
            else:
                st.error("Please fill all the fields.")
   
    # "Back to Login" button outside the form
    if st.button("Go Back"):
        return_to_login()




# Otherwise, show the login page
elif not st.session_state['is_logged_in']:
    st.markdown("<h3 style='text-align: center; color: blue;'>🔒 Login to PDF Query System</h3>", unsafe_allow_html=True)


# Login form design
    with st.form("login_form", clear_on_submit=True):
        st.markdown('<div class="centered-box">', unsafe_allow_html=True)
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        st.markdown('</div>', unsafe_allow_html=True)



# Login button
        if st.form_submit_button("Login"):
            if login_user(username, password):
                st.session_state['is_logged_in'] = True
                st.success("Login successful!")
                st.experimental_rerun()  # Reload to show the main interface
            else:
                st.error("Invalid username or password.")
       
    # Signup button at the bottom of the login page
    if st.button("Sign Up"):
        st.session_state['is_signing_up'] = True
        st.experimental_rerun()



# Main Interface (PDF Query Interface)
else:
    st.markdown("<h3 style='text-align: center; color: blue;'>📄 PDF Query Interface</h3>", unsafe_allow_html=True)
    st.markdown("Welcome! You can select a PDF or query across all PDFs.")


# Layout for Question Input and PDF selection
    with st.form(key="query_form"):
        st.subheader("Ask Your Question")
       
        # Input for user's question
        query = st.text_input("Enter your question here:", value=st.session_state['query'])
       
        # Dropdown to select preprocessed PDF
        selected_pdf = st.selectbox("Select a PDF (Optional)", ["All PDFs"] + pdf_list, index=pdf_list.index(st.session_state['selected_pdf']) if st.session_state['selected_pdf'] in pdf_list else 0)
       
        # Submit button to submit the query
        submit_button = st.form_submit_button(label="Submit")
       
        if submit_button:
            if query:
                st.session_state['query'] = query
                st.session_state['selected_pdf'] = selected_pdf
               
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


 # Logout button
    if st.button("Logout"):
        logout()







