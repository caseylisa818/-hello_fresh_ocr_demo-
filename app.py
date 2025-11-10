import streamlit as st
from PIL import Image
import easyocr
import numpy as np
import re

st.title("HelloFresh Recipe Add-On Demo (OCR)")
st.write("Upload a recipe image to extract ingredients and suggest add-ons!")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg","jpeg","png"])

if uploaded_file is not None:
    # Open the uploaded image with PIL
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Recipe', use_column_width=True)

    # Convert PIL image to numpy array for EasyOCR
    image_array = np.array(image)

    # Initialize EasyOCR reader
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image_array)

    # Extract text from OCR results
    text = " ".join([res[1] for res in result])
    st.write("### Extracted Text:")
    st.write(text)

    # Simple ingredient extraction
    ingredients = re.split(r'[\n,]+', text)
    ingredients = [i.strip() for i in ingredients if i.strip() != ""]

    st.write("### Detected Ingredients:")
    st.write(", ".join(ingredients))

    # Example add-ons based on ingredients
    add_ons = []
    for item in ingredients:
        item_lower = item.lower()
        if "cheese" in item_lower or "pasta" in item_lower:
            add_ons.append("Extra Parmesan Cheese")
        if "chicken" in item_lower or "beef" in item_lower:
            add_ons.append("Herb Marinade Pack")
        if "lettuce" in item_lower or "salad" in item_lower:
            add_ons.append("Organic Dressing Pack")

    st.write("### Suggested Add-Ons:")
    if add_ons:
        st.write(", ".join(add_ons))
    else:
        st.write("No add-ons detected for these ingredients.")
