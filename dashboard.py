import streamlit as st
from db import create_health_recommendation, get_health_recommendation_db, get_user_by_email
from utils import apply_custom_css, verify_user_session
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Select the Generative AI model
model = genai.GenerativeModel('gemini-pro')

# Apply custom styling
apply_custom_css()

# Ensure user is logged in
verify_user_session()

# Retrieve the user's email from session state
user_email = st.session_state['email']
user = get_user_by_email(user_email)

# Dashboard layout
st.markdown("<h1 class='title'>🏥 Health Dashboard</h1>", unsafe_allow_html=True)
st.image("./assets/dashboard.png", use_container_width=True, caption="Your Personalized Health Dashboard")
st.markdown(f"<h2 class='subtitle'>Welcome, {user['name']}!</h2>", unsafe_allow_html=True)

# Display user info
st.markdown(f"<p class='info-text'>Age: {user['age']} years</p>", unsafe_allow_html=True)
st.markdown(f"<p class='info-text'>Height: {user['height']} cm</p>", unsafe_allow_html=True)
st.markdown(f"<p class='info-text'>Weight: {user['weight']} kg</p>", unsafe_allow_html=True)

# BMI Calculation
if user['weight'] and user['height'] > 0:
    bmi = user['weight'] / ((user['height'] / 100) ** 2)
    st.markdown(f"<div class='box'>Your **BMI** is: {bmi:.2f}</div>", unsafe_allow_html=True)
else:
    st.markdown(f"<div class='box'>Add your Weight and Height to get your **BMI**</div>", unsafe_allow_html=True)

st.markdown("---")

# Get health recommendations from Google's Generative AI
def get_health_recommendations(user):
    # Construct the user health profile for the AI model
    user_profile = f"Name: {user['name']}, Age: {user['age']}, Gender: {user['gender']}, Weight: {user['weight']} kg, Height: {user['height']} cm, Medical Conditions: {user['medical_conditions']}, Health Goals: {user['health_goals']}"
    
    # Using `generate_text()` method for text generation
    response = model.generate_text(prompt=f"Based on the following user profile, provide personalized health recommendations:\n{user_profile}")

    # Return the generated text
    return response['text']

# Recommendations Button
if st.button("Get Health Recommendations"):
    recommendations = get_health_recommendations(user)
    st.markdown("<h3 class='subtitle'>Health Recommendations</h3>", unsafe_allow_html=True)
    st.markdown(f"<div class='recommendations'>{recommendations}</div>", unsafe_allow_html=True)
    
    # Save recommendations in the database
    create_health_recommendation(user['id'], recommendations)

# Display Previous Health Recommendations
health_recommendation = get_health_recommendation_db(user['id'])
if health_recommendation:
    st.markdown("<h3 class='subtitle'>Previous Health Recommendations</h3>", unsafe_allow_html=True)
    st.markdown(f"<div class='recommendations'>{health_recommendation['health_recommendation']}</div>", unsafe_allow_html=True)
