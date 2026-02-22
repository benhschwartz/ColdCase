import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Setup API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 2. App UI Header & Custom Bills Styling
st.set_page_config(page_title="ColdCase: Bills Mafia Edition", page_icon="🦬")

# Custom CSS for Bills colors
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    h1 { color: #00338D; border-bottom: 3px solid #C60C30; }
    .stButton>button { background-color: #00338D; color: white; border-radius: 10px; border: 2px solid #C60C30; }
    .stButton>button:hover { background-color: #C60C30; border: 2px solid #00338D; }
    </style>
    """, unsafe_allow_html=True)

st.title("🦬 ColdCase: Bills Mafia Fridge Chef")
st.write("Let's go Buffalo! Scan your fridge for game day eats.")

# 3. Sidebar Settings
with st.sidebar:
    st.image("https://static.www.nfl.com/image/private/f_auto/bills/vsc6u7j3v4f66t7f8gqh", width=100) # Small Bills Logo
    st.header("Tailgate Settings")
    
    diet_goal = st.selectbox("What's the play?", ["Standard", "Healthy", "Game Day Snacks", "High Protein"])
    
    # NEW: Mafia Mode Toggle
    mafia_mode = st.toggle("Activate Mafia Mode? 📢")
    
    st.divider()
    analyze_freshness = st.button("🍎 Analyze Freshness")
    
    # Easter Egg Button
    if st.button("Hey-ey-ey-ey!"):
        st.balloons()
        st.audio("https://www.myinstants.com/media/sounds/buffalo-bills-shout-song-excerpt.mp3") # Note: Audio might be blocked by some browsers
        st.success("LET'S GO BUFFALO!")

    st.divider()
    input_method = st.radio("Choose Input Method:", ("Camera Roll / Upload", "Take Live Photo"))

# 4. Image Input Logic
target = None
if input_method == "Take Live Photo":
    target = st.camera_input("Take a picture of the spread!")
else:
    target = st.file_uploader("Upload a photo from the camera roll", type=["jpg", "jpeg", "png"])

# 5. Processing Logic
if target:
    img = Image.open(target).convert("RGB")
    st.image(img, caption="Scanning the huddle...", use_container_width=True)

    if analyze_freshness:
        prompt = "Analyze the freshness of these items. Tell me what's about to spoil so we don't waste food before the big game."
        loading_msg = "Checking the roster..."
        header_msg = "⏳ Freshness Forecast"
    else:
        # Mafia Mode changes the AI's personality
        personality = "You are a die-hard Buffalo Bills fan and expert tailgate chef. " if mafia_mode else ""
        mafia_slang = "Use Buffalo slang like 'Bills Mafia', 'Circle the Wagons', and 'Go Bills'. " if mafia_mode else ""
        
        prompt = f"{personality}{mafia_slang}Identify the food in this image. Suggest 3 {diet_goal} recipes. If there are wings, mention Blue Cheese (never ranch)."
        loading_msg = "Circling the wagons..."
        header_msg = "👨‍🍳 Mafia Chef Recommendations"

    with st.spinner(loading_msg):
        model = genai.GenerativeModel('gemini-2.5-flash')
        try:
            response = model.generate_content([prompt, img])
            st.divider()
            st.subheader(header_msg)
            st.markdown(response.text)
            
            if mafia_mode:
                st.info("📢 BUFFALO ALL THE WAY!")
                
        except Exception as e:
            st.error(f"Error: {e}")

# Footer
st.caption("Powered by Gemini 2.5 Flash | Go Bills!")
