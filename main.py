import streamlit as st
import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import pytesseract
from deep_translator import GoogleTranslator

def translate_text(text):
    return GoogleTranslator(source='auto', target='en').translate(text)

def process_image(image):
    img = np.array(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    data = pytesseract.image_to_data(gray, lang='chi_sim', output_type=pytesseract.Output.DICT)

    for i in range(len(data['text'])):
        if int(data['conf'][i]) > 60:
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            original = data['text'][i]
            translated = translate_text(original)
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), -1)
            font_scale = 0.5
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, translated, (x, y + h - 5), font, font_scale, (0, 0, 0), 1, cv2.LINE_AA)
    
    return img

st.title("🈶 Bulk Size Chart Translator")
uploaded_files = st.file_uploader("Upload Chinese Size Chart Images", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        image = Image.open(file).convert('RGB')
        st.image(image, caption="Original", use_column_width=True)
        translated_img = process_image(image)
        st.image(translated_img, caption="Translated", use_column_width=True)
