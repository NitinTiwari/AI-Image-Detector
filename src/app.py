import os
import streamlit as st
import requests.exceptions
import requests
from PIL import Image
from PIL.ExifTags import TAGS
from dotenv import load_dotenv

load_dotenv()

# Sightengine credentials – replace with your actual keys
SIGHTENGINE_USER = os.getenv("SIGHTENGINE_USER")
SIGHTENGINE_SECRET = os.getenv("SIGHTENGINE_SECRET")

import base64
import tempfile

def query_sightengine(image_path, api_user, api_secret):
    """Check image using Sightengine's genai model.
    Returns the JSON response from the API.
    """
    params = {
        'models': 'genai',
        'api_user': api_user,
        'api_secret': api_secret
    }
    with open(image_path, 'rb') as f:
        files = {'media': f}
        r = requests.post('https://api.sightengine.com/1.0/check.json', files=files, data=params)
    return r.json()

def extract_exif(image):
    exif_data = image.getexif()
    metadata = {}
    if exif_data:
        for tag_id, value in exif_data.items():
            tag_name = TAGS.get(tag_id, tag_id)
            metadata[tag_name] = value
    return metadata

# 2. UI Layout
st.title("AI vs Real Image Detector")
st.write("Upload an image to verify if it is authentic or AI-generated.")

uploaded_file = st.file_uploader("Choose an image (JPG, PNG)...", type=["jpg", "jpeg", "png"])   

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Image", width=200)
    
    if st.button("Analyze Image"):
        with st.spinner("Analyzing image..."):
            # API Prediction
            uploaded_file.seek(0)
            # Save uploaded file to a temporary file for Sightengine API
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
                temp_file.write(uploaded_file.read())
                temp_path = temp_file.name
            api_results = query_sightengine(temp_path, SIGHTENGINE_USER, SIGHTENGINE_SECRET)
            
            # Metadata Check
            metadata = extract_exif(img)

        # 3. Display Results
        st.subheader("Analysis Results")
        
        # Handle successful list response (old format)
        if isinstance(api_results, list) and len(api_results) > 0:
            for item in api_results:
                label = item.get("label", "Unknown")
                score = round(item.get("score", 0.0) * 100, 2)
                st.write(f"**{label}:** {score}%")
        # Handle Sightengine dict response
        elif isinstance(api_results, dict):
            if api_results.get("status") == "success":
                # Extract AI‑generated confidence
                ai_score = api_results.get("ai_generated")
                # New: check 'type' field for ai_generated
                if ai_score is None:
                    ai_score = api_results.get("type", {}).get("ai_generated")
                # Fallback for older response format with models.genai
                if ai_score is None and isinstance(api_results.get("models"), dict):
                    genai = api_results["models"].get("genai")
                    if isinstance(genai, dict):
                        ai_score = genai.get("score") or genai.get("ai_generated")
                if ai_score is not None:
                    confidence = ai_score * 100
                    # Determine user‑friendly label
                    if ai_score >= 0.5:
                        verdict = "Likely AI-generated"
                    else:
                        verdict = "Likely Real Image"
                    # Show verdict with confidence in a blue filled rectangle
                    st.markdown(
                        f"{verdict} <span style='background-color:#007BFF;color:white;padding:2px 6px;border-radius:4px;'>{confidence:.0f}%</span>",
                        unsafe_allow_html=True,
                    )
                else:
                    st.info("API succeeded but did not return an AI-generated confidence score.")
                # JSON output removed for cleaner UI
            else:
                st.error(f"API error: {api_results.get('error', 'Unknown error')}")
        else:
            st.warning("API is currently warming up or rate-limited. Please retry in a few seconds.")
