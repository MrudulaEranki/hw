#under construction

import streamlit as st
from streamlit_drawable_canvas import st_canvas
import cv2
import numpy as np
import pytesseract
from PIL import Image
import io

st.title(" Handwriting to Font Generator")


uploaded_file = st.file_uploader("Upload a handwritten document (JPG, PNG, PDF)", type=["png", "jpg", "pdf"])

# Streamlit Drawable Canvas 
st.subheader("Or draw letters on the canvas:")
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)", 
    stroke_width=3,
    stroke_color="#000000",
    background_color="#FFFFFF",
    height=300,
    width=600,
    drawing_mode="freedraw",
    key="canvas"
)

# Save drawn letters as images
if canvas_result.image_data is not None:
    img_data = canvas_result.image_data
    img = Image.fromarray((img_data[:, :, :3] * 255).astype(np.uint8))  # Convert to PIL Image
    img.save("drawn_letter.png")  # Save the drawn image
    st.image(img, caption="Your Drawn Letter", use_column_width=True)

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Handwritten Document", use_column_width=True)



#under construction
