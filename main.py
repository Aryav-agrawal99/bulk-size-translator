import streamlit as st
import easyocr
from deep_translator import GoogleTranslator
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import io

# Load EasyOCR reader (Chinese and English)
reader = easyocr.Reader(['ch_sim', 'en'])

translator = GoogleTranslator(source='chinese', target='english')

def translate_image(image):
    image_array = np.array(image.convert("RGB"))
    results = reader.readtext(image_array)

    draw = ImageDraw.Draw(image)

    for (bbox, text, prob) in results:
        translated_text = translator.translate(text)
        top_left = tuple(map(int, bbox[0]))
        bottom_right = tuple(map(int, bbox[2]))
        
        # Draw white box to cover old text
        draw.rectangle([top_left, bottom_right], fill="white")

        # Draw translated text
        draw.text(top_left, translated_text, fill="black")

    return image

st.title("🈺 Size Chart Translator (Chinese → English)")
uploaded_files = st.file_uploader("Upload size chart images (JPG/PNG)", accept_multiple_files=True, type=["jpg", "jpeg", "png"])

if uploaded_files:
    for uploaded_file in uploaded_files:
        image = Image.open(uploaded_file)
        translated_image = translate_image(image.copy())

        st.image(translated_image, caption="Translated Image", use_column_width=True)

        # Download option
        img_byte_arr = io.BytesIO()
        translated_image.save(img_byte_arr, format='JPEG')
        st.download_button(
            label="Download Translated Image",
            data=img_byte_arr.getvalue(),
            file_name=f"translated_{uploaded_file.name}",
            mime="image/jpeg"
        )
