import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Setup API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 2. UI
st.title("📸 ColdCase: AI Fridge Chef")

img_file = st.camera_input("Take a fridge photo")
uploaded_file = st.file_uploader("Or upload", type=["jpg", "png", "jpeg"])

target = img_file or uploaded_file

if target:
    # Process image
    img = Image.open(target).convert("RGB")
    st.image(img, caption="Scanning...")

    with st.spinner("AI Chef is thinking..."):
        # Make sure this line has 8 spaces (or 2 tabs) before it
        model = genai.GenerativeModel('gemini-1.5-flash-8b')
        
        try:
            response = model.generate_content([
                "What ingredients are in this fridge? Suggest 3 easy recipes.", 
                img
            ])
            st.subheader("👨‍🍳 Chef's Recommendations:")
            st.write(response.text)
        except Exception as e:
            st.error(f"AI Error: {e}")
