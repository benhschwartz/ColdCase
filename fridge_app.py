import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Setup API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 2. App UI Header
st.set_page_config(page_title="ColdCase: AI Fridge Chef", page_icon="🥗")
st.title("🥗 ColdCase: AI Fridge Chef")
st.write("Take a photo of your fridge, and I'll tell you what to cook!")

# 3. Sidebar Settings (Line 15 area)
st.sidebar.header("Chef Settings")
diet_goal = st.sidebar.selectbox(
    "What is your goal?",
    ["Standard", "Healthy", "Quick (Under 15 mins)", "High Protein", "Kid Friendly"]
)
show_macros = st.sidebar.toggle("Include Calories & Macros?")

# 4. Camera Input
target = st.camera_input("Take a picture of your ingredients!")

if target:
    img = Image.open(target).convert("RGB")
    st.image(img, caption="Scanning your fridge...", use_container_width=True)

    with st.spinner(f"AI Chef is thinking ({diet_goal})..."):
        # Use the most stable model name for 2026
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Build the dynamic prompt based on sidebar settings
        nutrition_info = " Please also include estimated calories and macros (Protein, Carbs, Fat) for each recipe." if show_macros else ""
        prompt = f"Identify the food items in this image. Suggest 3 {diet_goal} recipes based on these ingredients.{nutrition_info}"
        
        try:
            # Generate response
            response = model.generate_content([prompt, img])
            
            st.divider()
            st.subheader(f"👨‍🍳 {diet_goal} Recommendations:")
            st.write(response.text)
            
        except Exception as e:
            # Check for the common 429 Quota error
            if "429" in str(e):
                st.error("AI Error: Daily limit reached. Please wait a minute or check your Google AI Studio quota.")
            else:
                st.error(f"AI Error: {e}")

# Footer
st.caption("Powered by Gemini 2.0 Flash")
