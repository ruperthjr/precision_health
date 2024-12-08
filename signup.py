import streamlit as st
from db import create_user, get_user_by_email, update_user_info


def signup_page():
    st.title("Sign Up")

    # Add a link to switch back to the login page
    if st.button("Already have an account? Log In"):
        st.session_state['page'] = 'login'

    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    age = st.number_input("Age", min_value=1, max_value=120)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    height = st.number_input("Height (cm)", min_value=1)
    weight = st.number_input("Weight (kg)", min_value=1)
    medical_conditions = st.text_input("Medical Conditions")
    health_goals = st.text_input("Health Goals")

    if st.button("Sign Up"):
        if name and email and password:
            # Create a new user
            create_user(name, email, password, age, gender, height, weight, medical_conditions, health_goals)
            st.success("Account created successfully!")
            st.session_state['logged_in'] = True
            st.session_state['email'] = email
            st.button("Go to Dashboard")
        else:
            st.error("Please fill all required fields.")


def login_page():
    st.title("Login")
    
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = get_user_by_email(email)
        if user and user['password'] == password:
            st.session_state['logged_in'] = True
            st.session_state['email'] = email
            st.success(f"Welcome back, {user['name']}!")
            st.button("Go to Dashboard")
            return 1
        else:
            st.error("Invalid email or password.")
    
    # Add a link to switch to the signup page
    if st.button("Don't have an account? Sign Up"):
        st.session_state['page'] = 'signup'
