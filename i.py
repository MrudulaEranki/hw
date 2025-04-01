import streamlit as st
from streamlit_drawable_canvas import st_canvas
import numpy as np
from PIL import Image, ImageOps
import os

# Title
st.title("Custom Handwriting Generator")

# save handwriting samples
SAVE_DIR = "handwriting_samples"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

#  save drawn letters
def save_image(image_data, letter):
    if image_data is not None:
        image = Image.fromarray((image_data[:, :, :3]).astype("uint8"))  #   PIL image
        image = image.resize((64, 64))  # Resize  
        image = ImageOps.invert(image)  #  handwriting black on white
        image.save(os.path.join(SAVE_DIR, f"{letter}.png"))
        st.success(f"✅ {letter} saved successfully!")

# generate handwritten text
def generate_handwritten_text(text):
    images = []
    
    for char in text:
        char = char.upper()  # Convert to uppercase for consistency
        img_path = os.path.join(SAVE_DIR, f"{char}.png")

        if os.path.exists(img_path):
            img = Image.open(img_path)
            images.append(img)
        else:
           
            blank_img = Image.new("RGB", (64, 64), (255, 255, 255))
            images.append(blank_img)

    if images:
        final_image = concat_images(images)
        return final_image
    return None

# combine letter images into a full handwritten output
def concat_images(images):
    widths, heights = zip(*(img.size for img in images))
    total_width = sum(widths)  # Width of the full image
    max_height = max(heights)  # Keep max height

    new_image = Image.new("RGB", (total_width, max_height), (255, 255, 255))

    x_offset = 0
    for img in images:
        new_image.paste(img, (x_offset, 0))
        x_offset += img.width

    return new_image

# UI: Select a letter to draw
letter = st.selectbox("Select a letter to draw:", list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"))

# Create a drawing canvas
st.write(f"Draw the letter: {letter}")
canvas_result = st_canvas(
    fill_color="black",
    stroke_width=5,
    stroke_color="black",
    background_color="white",
    height=200,
    width=200,
    key="canvas",
)

# Save drawn letter when button is clicked
if st.button("Save Handwriting Sample"):
    if canvas_result.image_data is not None:
        save_image(canvas_result.image_data, letter)

# Show saved handwriting samples
if st.button("Show Saved Letters"):
    saved_files = os.listdir(SAVE_DIR)
    if saved_files:
        st.write("Your saved handwriting samples:")
        for file in saved_files:
            st.image(os.path.join(SAVE_DIR, file), caption=file.split(".")[0], width=100)
    else:
        st.warning("No handwriting samples saved yet!")

# Input text to convert to handwriting
typed_text = st.text_area("Enter text to convert to handwriting:", "Hello World")

# Convert and display handwritten text
if st.button("Convert to Handwriting"):
    if len(os.listdir(SAVE_DIR)) < 26:
        st.warning("You need to save all letters (A-Z, a-z) first!")
    else:
        handwritten_text_img = generate_handwritten_text(typed_text)
        if handwritten_text_img:
            st.image(handwritten_text_img, caption="Your Handwritten Text")

st.write("Draw all letters to create a fully customized handwriting font.")
