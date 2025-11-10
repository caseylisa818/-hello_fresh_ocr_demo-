import streamlit as st
from PIL import Image
import easyocr
import numpy as np
import re
from rapidfuzz import fuzz

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

st.title("HelloFresh Recipe Add-On Demo (Sliding-Window Fuzzy OCR)")
st.write("Upload a recipe image to extract ingredients and suggest add-ons!")

uploaded_file = st.file_uploader("Choose a recipe image...", type=["jpg","jpeg","png"])

# -----------------------------
# Sliding-window fuzzy matching function
# -----------------------------
def detect_ingredients_sliding(text, known_ingredients, threshold=75):
    detected = set()
    lines = text.split("\n")
    for line in lines:
        # Clean OCR line
        line_clean = re.sub(r'[^a-z\s]', ' ', line.lower())
        line_clean = re.sub(r'\s+', ' ', line_clean).strip()
        words = line_clean.split()
        # Check all ingredients
        for ingredient in known_ingredients:
            ing_words = ingredient.split()
            if len(words) < len(ing_words):
                continue
            # Sliding window over OCR words
            for i in range(len(words) - len(ing_words) + 1):
                window = " ".join(words[i:i+len(ing_words)])
                score = fuzz.partial_ratio(ingredient, window)
                if score >= threshold:
                    detected.add(ingredient)
    return list(detected)

# -----------------------------
# Main app
# -----------------------------
if uploaded_file is not None:
    # Open image safely
    with Image.open(uploaded_file) as image:
        st.image(image, caption='Uploaded Recipe', use_column_width=True)

        # Convert to numpy array for OCR
        image_array = np.array(image)

        # OCR
        reader = easyocr.Reader(['en'])
        result = reader.readtext(image_array)
        raw_text = "\n".join([res[1] for res in result])  # keep lines
        st.write("### Extracted Text (Raw OCR):")
        st.write(raw_text)

        # Detect ingredients
        detected_ingredients = detect_ingredients_sliding(raw_text, KNOWN_INGREDIENTS, threshold=75)
        st.write("### Detected Ingredients (Cleaned & Fuzzy):")
        if detected_ingredients:
            st.write(", ".join(sorted(detected_ingredients)))
        else:
            st.write("No ingredients detected from image.")

        # Suggest Add-Ons
        add_ons = []
        if any(x in detected_ingredients for x in ["mozzarella]()_
