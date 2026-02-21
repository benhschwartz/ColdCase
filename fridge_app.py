import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Security: Look for the hidden API Key
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# 2. App Interface
st.title("📸 ColdCase: AI Fridge Chef")
st.write("Take a photo of your fridge to see what you can cook!")

# 3. Camera/Upload Widget
img_file = st.camera_input("Take a picture of your fridge") 
# Or allow manual upload
uploaded_file = st.file_uploader("...or upload a photo", type=["jpg", "png", "jpeg"])

# Use whichever one the user provided
target_image = img_file or uploaded_file

if target_image:
    img = Image.open(target_image)
    
    # --- ADD THIS LINE TO FIX THE ERROR ---
    img = img.convert("RGB") 
    # ---------------------------------------

    st.image(img, caption="Scanning your ingredients...", use_container_width=True)
    
    with st.spinner("AI Chef is thinking..."):
        model = genai.GenerativeModel('gemini-1.5-flash')
        # We pass the converted 'img' here
        response = model.generate_content([
            "List the ingredients you see and suggest 3 easy recipes.", 
            img
        ])
        
        st.subheader("👨‍🍳 Chef's Recommendations:")
        st.write(response.text)
