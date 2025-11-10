import streamlit as st
from PIL import Image, UnidentifiedImageError
import easyocr
import numpy as np
import re
from rapidfuzz import fuzz

# -----------------------------
# CONFIG / INGREDIENTS
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

st.set_page_config(page_title="HelloFresh OCR Add-on Demo", layout="centered")
st.title("HelloFresh Recipe Add-On Demo (Robust OCR)")
st.write("Upload a recipe image to extract ingredients and suggest add-ons!")

# -----------------------------
# Cache the OCR reader so it's not reinitialized every interaction
# -----------------------------
@st.cache_resource
def get_ocr_reader(lang_list=["en"]):
    try:
        reader = easyocr.Reader(lang_list, gpu=False)  # gpu=False for Cloud compatibility
        return reader
    except Exception as e:
        st.error(f"Failed to initialize OCR reader: {e}")
        return None

reader = get_ocr_reader()

uploaded_file = st.file_uploader("Choose a recipe image...", type=["jpg", "jpeg", "png"])

# -----------------------------
# Sliding-window fuzzy matching function
# -----------------------------
def detect_ingredients_sliding(text, known_ingredients, threshold=75):
    detected = set()
    if not text:
        return []
    lines = text.split("\n")
    for line in lines:
        # Clean OCR line
        line_clean = re.sub(r'[^a-z\s]', ' ', line.lower())
        line_clean = re.sub(r'\s+', ' ', line_clean).strip()
        if not line_clean:
            continue
        words = line_clean.split()
        # Check all ingredients
        for ingredient in known_ingredients:
            ing_words = ingredient.split()
            if len(words) < len(ing_words):
                # still attempt partial matches by sliding smaller windows
                max_window = len(words)
            else:
                max_window = len(words) - len(ing_words) + 1
            for i in range(max(1, max_window)):
                # Build windows of size equal to ingredient words (or smaller when line shorter)
                win_size = min(len(ing_words), len(words) - i)
                window = " ".join(words[i:i+win_size])
                # Use partial_ratio on both normalized strings
                score = fuzz.partial_ratio(ingredient, window)
                if score >= threshold:
                    detected.add(ingredient)
                    break  # stop sliding for this ingredient on this line
    return sorted(detected)

# -----------------------------
# Main app logic
# -----------------------------
if uploaded_file is not None:
    if reader is None:
        st.error("OCR reader failed to initialize. Please check the logs or try redeploying.")
    else:
        try:
            # Safely open image using context manager (prevents 'file not closed' warnings)
            with Image.open(uploaded_file) as image:
                st.image(image, caption='Uploaded Recipe', use_column_width=True)

                # Convert to numpy array for OCR
                try:
                    image_array = np.array(image)
                except Exception as e:
                    st.error(f"Could not convert uploaded file to an image array: {e}")
                    image_array = None

                if image_array is not None:
                    # OCR
                    try:
                        ocr_results = reader.readtext(image_array)
                    except Exception as e:
                        st.error(f"OCR processing failed: {e}")
                        ocr_results = []

                    if not ocr_results:
                        st.warning("OCR did not detect readable text. Try a clearer photo or higher resolution image.")
                        raw_text = ""
                    else:
                        # Keep each detected piece as a line to improve line-by-line matching
                        raw_text = "\n".join([res[1] for res in ocr_results])

                    st.write("### Extracted Text (Raw OCR):")
                    st.write(raw_text if raw_text else "— no text extracted —
