import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Setup API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 2. App UI Header
st.set_page_config(page_title="ColdCase: AI Fridge Chef", page_icon="🥗")
st.title("🥗 ColdCase: AI Fridge Chef")

# 3. Sidebar Settings
with st.sidebar:
    st.header("Chef Settings")
    
    # Dropdown for Diet Goal
    diet_goal = st.selectbox(
        "What is your goal?",
        ["Standard", "Healthy", "Quick (Under 15 mins)", "High Protein", "Kid Friendly", "Vegetarian"]
    )
    
    # Dropdown for Chef Tone
    chef_tone = st.selectbox(
        "Chef Personality",
        ["Friendly Assistant", "Professional Chef", "Sassy Aunt", "Gordon Ramsay Mode"]
    )
    
    # Toggle for Macros
    show_macros = st.toggle("Include Calories & Macros?")
    
    # Toggle for Input Method
    input_method = st.radio("Choose Input Method:", ("Camera Roll / Upload", "Take Live Photo"))

st.divider()

# 4. Image Input Logic
target = None
if input_method == "Take Live Photo":
    target = st.camera_input("Take a picture of your ingredients!")
else:
    target = st.file_uploader("Upload a clear photo from your gallery", type=["jpg", "jpeg", "png"])

# 5. Processing the Image
if target:
    img = Image.open(target).convert("RGB")
    st.image(img, caption="Image Loaded Successfully!", use_container_width=True)

    with st.spinner(f"AI Chef is thinking..."):
        # Using the newest stable model for 2026
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Crafting the dynamic prompt
        macro_text = " Please also include estimated calories and macros for each recipe." if show_macros else ""
        
        prompt = (
            f"Act as a {chef_tone}. Identify the food items in this image. "
            f"Suggest 3 {diet_goal} recipes based on these ingredients. "
            f"Format the output with bold titles and numbered steps.{macro_text}"
        )
        
        try:
            response = model.generate_content([prompt, img])
            st.success("Here is what I found!")
            st.markdown(response.text)
            
        except Exception as e:
            if "429" in str(e):
                st.error("Quota reached. Please wait 60 seconds and try again.")
            else:
                st.error(f"AI Error: {e}")

# Footer
st.caption(f"Model: Gemini 2.5 Flash | Mode: {diet_goal}")
