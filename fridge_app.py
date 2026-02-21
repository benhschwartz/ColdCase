import os
from google import genai
from PIL import Image
from pillow_heif import register_heif_opener

register_heif_opener()

# 1. YOUR API KEY
client = genai.Client(api_key="AIzaSyDlhTrqoisZHuL1di9KQ1GuHqhIQK0EZ2A")

image_path = "my_fridge.jpg"

print("🔍 Checking for image...")

if not os.path.exists(image_path):
    print(f"❌ Error: I can't find {image_path}")
else:
    try:
        # OPEN AND SHRINK IMAGE AUTOMATICALLY
        img = Image.open(image_path)
        img.thumbnail((800, 800)) # This makes it "Free Tier" friendly!
        
        print("📸 Image resized and ready! Asking AI Chef...")
        
        prompt = "Identify the food in this photo. Suggest 2 easy, kid-friendly recipes."
        
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=[prompt, img]
        )

        print("-" * 30)
        print("👨‍🍳 AI CHEF SUGGESTIONS:")
        print(response.text)
        
    except Exception as e:
        print(f"❌ Error: {e}")