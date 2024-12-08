import streamlit as st
from signup import signup_page, login_page
from db import get_user_by_email

def login():
    st.sidebar.title("Sign Up / Login")
    choice = st.sidebar.radio("Select an option", ["Login", "Sign Up"])
    if choice == "Login":
        login_page()
    else:
        signup_page()