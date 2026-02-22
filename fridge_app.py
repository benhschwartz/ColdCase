import streamlit as st
import google.generativeai as genai
from PIL import Image
import random
import base64

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
    /* Circular Profile Style */
    .profile-pic {
        width: 150px;
        height: 150px;
        border-radius: 50%;
        object-fit: cover;
        border: 4px solid #00338D;
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    .chef-title {
        text-align: center; 
        color: #00338D; 
        margin-top: 10px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🦬 ColdCase: Mafia Kid-Chef")

# 3. Sidebar Settings
with st.sidebar:
    # --- BRANDING SECTION ---
    try:
        # Function to convert image to base64 for reliable iPhone display
        def get_image_base64(path):
            with open(path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
        
        encoded_img = get_image_base64("me.jpg")
        st.markdown(f'<img src="data:image/png;base64,{encoded_img}" class="profile-pic">', unsafe_allow_html=True)
        st.markdown("<h3 class='chef-title'>Head Chef</h3>", unsafe_allow_html=True)
    except:
        # Fallback if me.jpg is missing
        st.markdown("### 👤 Head Chef")
        st.info("💡 Upload 'me.jpg' to GitHub to see your face here!")
    
    # Generic Buffalo Icon (Centered)
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        st.image("https://upload.wikimedia.org/wikipedia/commons/7/71/American_bison_silhouette.svg", width=60)
    
    st.divider()
    
    st.header("Tailgate Settings")
    diet_goal = st.selectbox("The Play Call:", ["Healthy & Kid Friendly", "Quick Snacks", "High Protein"])
    mafia_mode = st.toggle("Activate Mafia Mode? 📢", value=True)
    
    st.divider()
    
    if st.button("Hey-ey-ey-ey!"):
        st.balloons()
        st.snow()
        st.success("LET'S GO BUFFALO!")

    st.divider()
    input_method = st.radio("Choose Input Method:", ("Camera Roll / Upload", "Take Live Photo"))

# 4. Image Input Logic
target = None
if input_method == "Take Live Photo":
    target = st.camera_input("Take a picture of the spread!")
else:
    target = st.file
