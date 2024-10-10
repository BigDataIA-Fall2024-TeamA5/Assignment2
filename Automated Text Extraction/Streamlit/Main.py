# streamlit_app.py
import streamlit as st
import requests

# Define FastAPI base URL
FASTAPI_URL = "http://127.0.0.1:8000/auth"  # Make sure this matches your FastAPI server URL and path

# Function to handle signup
def signup(username, email, password):
    response = requests.post(f"{FASTAPI_URL}/register", json={
        "username": username,
        "email": email,
        "password": password
    })
    if response.status_code == 200:
        st.success("Account created successfully!")
    else:
        st.error(response.json().get("detail", "An error occurred during signup."))

# Function to handle login
def login(username, password):
    response = requests.post(f"{FASTAPI_URL}/login", json={
        "username": username,
        "password": password
    })
    if response.status_code == 200:
        token_data = response.json()
        st.session_state['access_token'] = token_data['access_token']
        st.session_state['logged_in'] = True
        st.success("Logged in successfully!")
    else:
        st.error("Invalid username or password. Please try again.")

# Session state to manage login state
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if 'page' not in st.session_state:
    st.session_state['page'] = 'login'

# Render different pages based on login state
if st.session_state['logged_in']:
    st.write("Welcome to the application!")
else:
    option = st.selectbox("Select Login or Signup", ("Login", "Signup"))

    if option == "Login":
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            login(username, password)

    elif option == "Signup":
        st.subheader("Signup")
        username = st.text_input("Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        if st.button("Signup"):
            signup(username, email, password)
