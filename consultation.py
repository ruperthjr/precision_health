import streamlit as st
import pandas as pd
import datetime
import requests
from bs4 import BeautifulSoup
import plotly.express as px
import plotly.graph_objects as go
import json
import time
import logging
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Import the user data fetching code
from dashboard import get_user_by_email, verify_user_session

# Configure logging for debugging purposes
logging.basicConfig(level=logging.DEBUG)

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Select the Generative AI model
model = genai.GenerativeModel('gemini-pro')

# Function to get Google Trends data via a simple request
def get_trending_data():
    url = "https://trends.google.com/trending?geo=US&category=7&hours=168"
    try:
        # Make a GET request to the trends URL
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            trending_items = []
            for trend_item in soup.find_all('div', class_='feed-item'):
                trend_name = trend_item.find('div', class_='feed-item-title').text.strip()
                search_volume = trend_item.find('div', class_='feed-item-stats').text.strip() if trend_item.find('div', class_='feed-item-stats') else "N/A"
                explore_link = trend_item.find('a', href=True)['href']
                trending_items.append({
                    'Trends': trend_name,
                    'Search volume': search_volume,
                    'Explore link': f"https://trends.google.com{explore_link}"
                })
            return pd.DataFrame(trending_items)
        else:
            st.error("Failed to retrieve Google Trends data.")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        logging.error(f"Error fetching data: {e}")
        return pd.DataFrame()

# Function to get medication recommendations based on health conditions
def get_medication_recommendations(health_conditions):
    medication_data = {
        "obesity": ["Wegovy", "Ozempic", "Mounjaro", "Phentermine"],  
        "diabetes": ["Metformin", "Insulin", "GLP-1 Agonists", "SGLT2 Inhibitors"],
        "high blood pressure": ["Atenolol", "Lisinopril", "Losartan", "Amlodipine"],
        "sunset anxiety": ["Xanax", "Zoloft", "Lexapro", "Ativan"],
        "arthritis": ["Methotrexate", "Sulfasalazine", "Humira", "Corticosteroids"],
        "depression": ["SSRIs", "SNRIs", "Citalopram", "Sertraline", "Fluoxetine"],
        "anxiety": ["Buspirone", "Xanax", "Ativan", "Valium"],
        "asthma": ["Albuterol", "Salbutamol", "Advair", "Fluticasone"],
        "COPD": ["Spiriva", "Symbicort", "Albuterol", "Fluticasone"],
        "cholesterol": ["Statins", "Lipitor", "Atorvastatin", "Zocor"],
        "sleep apnea": ["CPAP therapy", "BiPAP", "Oxygen therapy"],
        "eczema": ["Topical steroids", "Hydrocortisone", "Tacrolimus"],
        "insomnia": ["Ambien", "Melatonin", "Zolpidem"],
        "acne": ["Benzoyl Peroxide", "Tretinoin", "Accutane", "Doxycycline"],
        "allergies": ["Antihistamines", "Claritin", "Zyrtec", "Benadryl"],
        "migraine": ["Sumatriptan", "Zolmitriptan", "Amitriptyline", "Topiramate"],
        "heart disease": ["Beta-blockers", "Aspirin", "ACE inhibitors", "Statins"],
        "gout": ["Allopurinol", "Colchicine", "Indomethacin"],
        "cancer": ["Chemotherapy", "Immunotherapy", "Radiation therapy"],
        "stroke": ["Aspirin", "Clopidogrel", "Warfarin"],
        "thyroid problems": ["Levothyroxine", "Methimazole", "Liothyronine"],
        "kidney disease": ["ACE inhibitors", "Diuretics"],
        "liver disease": ["Antivirals", "Interferon", "Ribavirin"]
    }
    
    recommendations = {}
    for condition in health_conditions:
        if condition in medication_data:
            recommendations[condition] = medication_data[condition]
        else:
            recommendations[condition] = "No specific medications found"
    return recommendations

# Function to get PubMed links for medications
def get_pubmed_links(medications):
    pubmed_links = {}
    for medication in medications:
        search_url = f"https://pubmed.ncbi.nlm.nih.gov/?term={medication.replace(' ', '+')}"
        pubmed_links[medication] = search_url
    return pubmed_links

# Function to plot a health trend graph
def plot_health_trend(health_conditions, trending_data):
    trend_conditions = {
        "obesity": "Wegovy, Ozempic",
        "diabetes": "Metformin, Insulin",
        "high blood pressure": "Atenolol, Lisinopril",
        "sunset anxiety": "Xanax, Zoloft",
    }

    trend_counts = []
    for condition in health_conditions:
        if condition in trend_conditions:
            meds = trend_conditions[condition].split(", ")
            trend_counts.append(len(meds))

    fig = go.Figure()
    fig.add_trace(go.Bar(x=health_conditions, y=trend_counts, name="Trending Health Medications"))
    fig.update_layout(title="Trending Medications for Health Conditions", xaxis_title="Conditions", yaxis_title="Count of Medications")
    return fig

# Fetch user data from the dashboard
verify_user_session()  # Ensure user is logged in
user_email = st.session_state['email']
user = get_user_by_email(user_email)

# Streamlit app layout
st.title("Trending Medications Based on Your Health")

# Display user info
st.markdown(f"<h2>Welcome, {user['name']}!</h2>", unsafe_allow_html=True)
health_conditions = st.multiselect(
    "Select Your Health Conditions:",
    ["obesity", "diabetes", "high blood pressure", "sunset anxiety", "arthritis", "depression", "anxiety", "asthma", "COPD", "cholesterol", "sleep apnea", "eczema", "insomnia", "acne", "allergies", "migraine", "heart disease", "gout", "cancer", "stroke", "thyroid problems", "kidney disease", "liver disease"]
)

if health_conditions:
    recommendations = get_medication_recommendations(health_conditions)
    st.subheader("Recommended Medications:")
    for condition, meds in recommendations.items():
        st.write(f"**{condition.capitalize()}**: {', '.join(meds)}")

    # Display PubMed links for the medications
    pubmed_links = get_pubmed_links([med for meds in recommendations.values() for med in meds])
    st.subheader("PubMed Links for Medications:")
    for medication, link in pubmed_links.items():
        st.write(f"[{medication}]({link})")

else:
    st.write("Select your health conditions to get medication recommendations.")

# Load and display the trending data (if available)
df = get_trending_data()

if not df.empty:
    st.subheader("Trending Topics")
    st.write(f"Data loaded at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Filter data based on user selection or other criteria
    trending_filter = st.text_input("Search for a specific trend:")
    if trending_filter:
        df = df[df['Trends'].str.contains(trending_filter, case=False, na=False)]
    
    # Display the data
    st.dataframe(df[['Trends', 'Search volume', 'Explore link']])

    # Trend-related health medications visualization
    st.subheader("Health Condition and Medication Trends")
    health_trend_fig = plot_health_trend(health_conditions, df)
    st.plotly_chart(health_trend_fig)

else:
    st.warning("No trending data available.")

# Display additional information (e.g., about the trend, its breakdown)
if not df.empty:
    trend_selection = st.selectbox("Select a trending topic to view more details:", df['Trends'])
    if trend_selection:
        trend_info = df[df['Trends'] == trend_selection].iloc[0]
        st.write(f"**Explore More**: [Click here]({trend_info['Explore link']})")

# Log successful data fetch for debugging
logging.debug(f"Data loaded at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def verify_user_session():
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.error("You need to log in to access this page.")
        st.stop()