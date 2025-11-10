import streamlit as st
from PIL import Image, UnidentifiedImageError
import easyocr
import numpy as np
import re

# Always put this first Streamlit call at the top
st.set_page_config(page_title="HelloFresh Add-On Demo", layout="centered")

# -------------------------
# KNOWN INGREDIENTS
# -------------------------
KNOWN_INGREDIENTS = [
    "chicken", "chicken breast", "parmesan", "parmesan cheese", "mozzarella",
    "cheese", "pasta", "spaghetti", "rice", "lettuce",
    "tomato", "onion", "garlic", "basil", "olive oil", "carrot",
    "potato", "pepper", "salt", "vinegar", "spinach", "mushroom",
    "cream", "milk", "egg", "bread", "lemon", "lime", "butter"
]

# -------------------------
# INVENTORY + ADD-ONS
# -------------------------
INVENTORY = {
    "chicken": True,
    "parmesan": False,
    "mozzarella": True,
    "tomato": True,
    "basil": True,
    "garlic": False,
    "lettuce": True,
    "spinach": True,
    "butter": True,
    "olive oil": True,
}

ADD_ONS = {
    "chicken": "Herb Marinade Pack",
    "parmesan": "Extra Parmesan Cheese",
    "mozzarella": "Cheese Upgrade Pack",
    "tomato": "Organic Tomato Sauce Pouch",
    "lettuce": "Dressing Variety Kit",
    "basil": "Fresh Herb Bundle",
    "garlic": "Garlic Butter Kit",
    "spinach": "Green Boost Pack",
}

# -------------------------
# UI + OCR
# -------------------------
st.title("🍽️ HelloFresh Add-On Demo")
st.caption("Upload a recipe image to extract ingredients and match with HelloFresh inventory.")

@st.cache_resource
def get_reader():
    return easyocr.Reader(['en'], gpu=False)

reader = get_reader()

uploaded_file = st.file_uploader("Upload recipe photo...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    try:
        with Image.open(uploaded_file) as image:
            st.image(image, caption="Uploaded Recipe", use_column_width=True)
            image_array = np.array(image)

            # OCR
            ocr_results = reader.re_
