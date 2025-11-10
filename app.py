import streamlit as st
from PIL import Image
import easyocr
import numpy as np
import re

# -----------------------------
# Multi-word ingredient dictionary
# -----------------------------
KNOWN_INGREDIENTS = [
    "chicken breast", "chicken thighs", "ground beef", "pork chops",
    "salmon fillet", "shrimp", "mozzarella cheese", "parmesan cheese",
    "cheddar cheese", "pasta", "spaghetti", "rice", "lettuce",
    "tomato", "onion", "garlic", "basil", "olive oil", "carrot",
    "potato", "black pepper", "salt", "vinegar", "spinach", "mushroom",
    "cream", "milk", "egg", "bread", "lemon", "lime", "honey",
    "cinnamon", "nutmeg", "oregano", "thyme", "red bell pepper",
    "green bell pepper", "yellow bell pepper", "butter", "yogurt"
]

st.title("HelloFresh Recipe Add-On Demo (Robust Multi-Ingredient OCR)")
st.write("Upload a recipe image to extract ingredients and suggest add-ons!")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg","jpeg","png"])

if uploaded_file is not None:
    # Open image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Recipe', use_column_width=True)

    # Convert to numpy array
    image_array = np.array(image)

    # OCR
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image_array)
    raw_text = " ".join([res[1] for res in result])
    st.write("### Extracted Text (Raw OCR):")
    st.write(raw_text)

    # Clean OCR text
    text = raw_text.lower()
    text = re.sub(r'[^a-z\s]', ' ', text)  # remove non-letter characters
    text = re.sub(r'\s+', ' ', text)       # collapse multiple spaces

    # -----------------------------
    # Robust ingredient detection
    # -----------------------------
    detected_ingredients = []
    for ingredient in KNOWN_INGREDIENTS:
        words = ingredient.split()
        if all(word in text for word in words):
            detected_ingredients.append(ingredient)

    st.write("### Detected Ingredients (Cleaned):")
    if detected_ingredients:
        st.write(", ".join(sorted(set(detected_ingredients))))
    else:
        st.write("No ingredients detected from image.")

    # -----------------------------
    # Suggest Add-Ons
    # -----------------------------
    add_ons = []
    if any(x in detected_ingredients for x in ["mozzarella cheese", "parmesan cheese", "cheddar cheese", "pasta", "spaghetti"]):
        add_ons.append("Extra Parmesan Cheese")
    if any(x in detected_ingredients for x in ["chicken breast", "chicken thighs", "ground beef", "pork chops", "shrimp", "salmon fillet"]):
        add_ons.append("Herb Marinade Pack")
    if any(x in detected_ingredients for x in ["lettuce", "tomato", "spinach", "carrot", "red bell pepper", "green bell pepper", "yellow bell pepper"]):
        add_ons.append("Organic Dressing Pack")

    st.write("### Suggested Add-Ons:")
    if add_ons:
        st.write(", ".join(add_ons))
    else:
        st.write("No add-ons detected for these ingredient
