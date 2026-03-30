import streamlit as st
from dotenv import load_dotenv
import os
from PIL import Image
from google import genai

# Load environment variables
load_dotenv()
key = os.getenv("GOOGLE_API_KEY")

# Initialize Gemini client
client = genai.Client(api_key=key)

# Streamlit UI
st.set_page_config(
    page_title="Structural Defect Detection App",
    page_icon="📷",
    layout="wide"
)

st.title("Structural Defect Detection App")
st.header("Project Overview")
st.subheader("Objective")

with st.expander("Click to expand the project objective"):
    st.markdown("""
    The project aims to develop a structural defect detection application using Google Gemini API.
    It allows users to upload images and receive feedback on structural defects.
    """)

st.subheader("Upload the image here")

input_image = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png"]
)

img = None

if input_image:
    img = Image.open(input_image).convert("RGB")
    st.image(img, caption="Uploaded successfully ✅")

# Prompt
prompt = """
Act as a structural and civil engineer. Give maximum 3 bullet points per answer.

1. Detect defects (cracks, bends, damages)
2. Probability of defect
3. Severity level
4. Causes
5. Repair or replace?
6. Remedies
7. Safety hazards
8. Monitoring needed?
9. Cost estimate (INR)
10. Summary (max 3 lines)
"""

# Gemini response function
def generate_response(prompt, img):
    response = client.models.generate_content(
        model="gemini-1.0-pro-vision",
        contents=[prompt, img]
    )
    return response.text


# Button
if st.button("Detect Defects"):
    if img:
        with st.spinner("Analyzing image..."):
            result = generate_response(prompt, img)
            st.subheader("Detection Results")
            st.markdown(result)
    else:
        st.warning("Please upload an image first")