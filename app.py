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

st.title("HelloFresh Recipe Add-On Demo (Reliable Multi-Ingredient OCR)")
st.write("Upload a recipe image to extract ingredients and suggest add-ons!")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg","jpeg","png"])

def detect_ingredients_fuzzy(text, known_ingredients, thres_
