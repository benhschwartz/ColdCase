import streamlit as st
import google.generativeai as genai
from PIL import Image
import random

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
    </style>
    """, unsafe_allow_html=True)

st.title("🦬 ColdCase: Mafia Kid-Chef")

# 3. Sidebar Settings
with st.sidebar:
    # --- 1. YOUR PHOTO ---
    try:
        st.image("me.jpg", use_container_width=True)
        st.markdown("<h3 style='text-align: center; color: #00338D; margin-bottom: 0;'>Head Chef</h3>", unsafe_allow_html=True)
    except:
        st.info("💡 Pro Tip: Upload 'me.jpg' to GitHub to see your face here!")
    
    # --- 2. BILLS LOGO ---
    # Keeping the logo right under your photo
    st.image("https://static.www.nfl.com/image/private/f_auto/bills/vsc6u7j3v4f66t7f8gqh", width=80)
    
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
    target = st.file_uploader("Upload a clear photo", type=["jpg", "jpeg", "png"])

# 5. Processing Logic
if target:
    img = Image.open(target).convert("RGB")
    st.image(img, caption="Scanning the roster...", use_container_width=True)

    # Mafia + Parent + Kid Task Logic
    personality = "You are a die-hard Buffalo Bills fan and a health-conscious parent. " if mafia_mode else ""
    mafia_slang = "Use family-friendly Buffalo slang like 'Bills Mafia'. " if mafia_mode else ""
    
    kid_task_logic = (
        "For EACH recipe, add a section called '👶 Little Sous Chef Task'. "
        "In this section, suggest 1 or 2 safe, fun tasks for a child to help with. "
        "Ensure all recipes are healthy, low-sugar, and kid-approved."
    )
    
    ranch_ban = "Note: Blue cheese only for the wings! No ranch in this house. "
    
    prompt = f"{personality}{mafia_slang}{kid_task_logic}{ranch_ban}Identify the food in this image and suggest 3 {diet_goal} recipes. Format with bold titles."

    if st.button("🚀 SMASH TABLES & START COOKING"):
        with st.spinner("Circling the wagons..."):
            model = genai.GenerativeModel('gemini-2.0-flash')
            try:
                response = model.generate_content([prompt, img])
                
                # Victory Effects
                st.balloons()
                st.toast("TABLE SMASHED! 🪑💥", icon="🦬")
                
                st.divider()
                st.subheader(f"👨‍🍳 Mafia Parent's {diet_goal} Menu:")
                st.markdown(response.text)
                
                # Random Bills Quote
                quotes = ["Go Bills!", "Josh Allen eats his spinach!", "Circle the wagons!", "Bills by a Billion!"]
                st.info(random.choice(quotes))
                
            except Exception as e:
                st.error(f"Error: {e}")

st.caption("Built for the Mafia | Powered by Gemini")
