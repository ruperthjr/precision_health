import streamlit as st

def apply_custom_css():
    st.markdown("""
        <style>
        .title {
            font-size: 40px;
            font-weight: bold;
            color: #34495E;
            text-align: center;
        }
        .subtitle {
            font-size: 22px;
            font-weight: bold;
            color: #2E86C1;
        }
        .info-text {
            font-size: 18px;
            color: #566573;
        }
        .highlight {
            font-size: 18px;
            font-weight: bold;
            color: #CB4335;
        }
        .box {
            background-color: #87CEEB;
            padding: 15px;
            border-radius: 10px;
            font-size: 18px;
            color: #2C3E50;
            border: 1px solid #BDC3C7;
        }
        .recommendations {
            background-color: #abc0d4;
            padding: 15px;
            border-radius: 10px;
            font-size: 18px;
            color: #1C2833;
            border: 1px solid #AAB7B8;
        }
        </style>
    """, unsafe_allow_html=True)

def verify_user_session():
    if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
        st.error("You need to log in to access this page.")
        st.stop()
