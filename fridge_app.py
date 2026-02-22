import streamlit as st
import google.generativeai as genai
from PIL import Image
import random
import os

# 1. Setup API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 2. App UI Header & Bills Styling
st.set_page_config(page_title="ColdCase: Mafia Family Edition", page_icon="🦬")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    h1 { color: #00338D; border-bottom: 3px solid #C60C30; }
    .stButton>button { 
        background-color: #00338D; 
        color: white; 
        border-radius: 10px; 
        border: 2px solid #C60C30;
        font-weight: bold;
    }
    .stButton>button:hover { 
        background-color: #C60C30; 
        border: 2px solid #00338D;
        transform: scale(1.05);
    }
    .chef-text {
        text-align: center; 
        color: #00338D; 
        font-weight: bold;
        margin-bottom: 0px;
    }
    .buffalo-emoji {
        text-align: center;
        font-size: 45px;
        margin-top: -10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🦬 ColdCase: Mafia Kid-Chef")

# 3. Sidebar Settings
with st.sidebar:
    # --- BRANDING SECTION ---
    if os.path.exists("me.jpg"):
        st.image("me.jpg", use_container_width=True)
        st.markdown("<p class='chef-text'>Head Chef</p>", unsafe_allow_html=True)
    else:
        st.markdown("<h1 style='text-align: center;'>👨‍🍳</h1>", unsafe_allow_html=True)
        st.markdown("<p class='chef-text'>Head Chef</p>", unsafe_allow_html=True)
        st.caption("To see your face: Upload 'me.jpg' to GitHub")

    # Buffalo Emoji (Bulletproof on iPhone)
    st.markdown("<div class='buffalo-emoji'>🦬</div>", unsafe_allow_html=True)
    
    st.divider()
    
    st.header("Tailgate Settings")
    diet_goal = st.selectbox("The Play Call:", ["Healthy & Kid Friendly", "Quick Snacks", "
