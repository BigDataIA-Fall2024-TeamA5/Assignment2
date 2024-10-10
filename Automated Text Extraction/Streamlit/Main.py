# main.py

import streamlit as st
import requests

FASTAPI_URL = "http://localhost:8000"  # Replace with your FastAPI URL

def signup(username, email, password):
    response = requests.post(f"{FASTAPI_URL}/auth/register", json={
        "username": username,
        "email": email,
        "password": password
    })
    if response.status_code == 200:
        st.success("Account created successfully!")
    else:
        st.error(response.json().get("detail", "An error occurred during signup."))

def login(username, password):
    response = requests.post(f"{FASTAPI_URL}/auth/login", json={
        "username": username,
        "password": password
    })
    if response.status_code == 200:
        token_data = response.json()
        st.session_state['access_token'] = token_data['access_token']
        st.session_state['logged_in'] = True
        st.success("Logged in successfully!")
        st.session_state['page'] = 'application'
    else:
        st.error("Invalid username or password. Please try again.")

# Check if user is logged in and set page state
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if 'page' not in st.session_state:
    st.session_state['page'] = 'login'

# Main Login/Signup Interface
if st.session_state['logged_in']:
    if st.session_state['page'] == 'application':
        import application  # Redirect to `application.py`
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