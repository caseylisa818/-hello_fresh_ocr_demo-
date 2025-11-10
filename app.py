import streamlit as st
from PIL import Image
import easyocr
import numpy as np
import re

# -----------------------------
# Mini ingredient dictionary
# -----------------------------
KNOWN_INGREDIENTS = [
    "chicken", "beef", "pork", "salmon", "shrimp",
    "cheese", "parmesan", "mozzarella", "butter",
    "pasta", "rice", "lettuce", "tomato", "onion",
    "garlic", "basil", "olive oil", "carrot", "potato",
    "pepper", "salt", "vinegar", "spinach", "mushroom",
    "cream", "milk", "egg", "bread", "lemon", "lime",
    "honey", "cinnamon", "nutmeg", "oregano", "thyme",
]

# -----------------------------
# Streamlit App
# -----------------------------
st.title("HelloFresh Recipe Add-On Demo (Clean OCR)")
st.write("Upload a recipe image to extract ingredients and suggest add-ons!")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg","jpeg","png"])

if uploaded_file is not None:
    # Open the uploaded image with PIL
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Recipe', use_column_width=True)

    # Convert PIL image to numpy array for EasyOCR
    image_array = np.array(image)

    # OCR with EasyOCR
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image_array)
    raw_text = " ".join([res[1] for res in result])
    st.write("### Extracted Text (Raw OCR):")
    st.write(raw_text)

    # -----------------------------
    # Clean OCR Text
    # -----------------------------
    text = raw_text.lower()
    text = re.sub(r'[^a-z\s]', ' ', text)  # remove non-letter chars
    words = text.split()

    # Keep only known ingredients
    ingredients = [w for w in words if w in KNOWN_INGREDIENTS]
    st.write("### Detected Ingredients (Cleaned):")
    st.write(", ".join(sorted(set(ingredients))))  # remove duplicates

    # -----------------------------
    # Suggest Add-Ons
    # -----------------------------
    add_ons = []
    if any(x in ingredients for x in ["cheese", "parmesan", "mozzarella", "pasta"]):
        add_ons.append("Extra Parmesan Cheese")
    if any(x in ingredients for x in ["chicken", "beef", "pork", "shrimp", "salmon"]):
        add_ons.append("Herb Marinade Pack")
    if any(x in ingredients for x in ["lettuce", "tomato", "spinach", "carrot"]):
        add_ons.append("Organic Dressing Pack")
    
    st.write("### Suggested Add-Ons:")
    if add_ons:
        st.write(", ".join(add_ons))
    else:
        st.write("No add-ons detected for these ingredients.")
