import streamlit as st
from PIL import Image, UnidentifiedImageError
import easyocr
import numpy as np
import re

# Page config (must be first Streamlit call)
st.set_page_config(page_title="HelloFresh OCR Add-on Demo", layout="centered")

# Simple ingredient list (expandable)
KNOWN_INGREDIENTS = [
    "chicken", "chicken breast", "parmesan", "parmesan cheese", "mozzarella",
    "cheese", "pasta", "spaghetti", "rice", "lettuce",
    "tomato", "onion", "garlic", "basil", "olive oil", "carrot",
    "potato", "pepper", "salt", "vinegar", "spinach", "mushroom",
    "cream", "milk", "egg", "bread", "lemon", "lime", "butter"
]

st.title("HelloFresh Recipe Add-On Demo (Simple)")
st.write("Upload a recipe image to extract ingredients and suggest add-ons!")

# Initialize OCR reader once (cached)
@st.cache_resource
def get_reader():
    try:
        return easyocr.Reader(['en'], gpu=False)
    except Exception as e:
        st.error(f"Failed to initialize OCR reader: {e}")
        return None

reader = get_reader()
uploaded_file = st.file_uploader("Choose a recipe image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    if reader is None:
        st.error("OCR reader not available.")
    else:
        try:
            with Image.open(uploaded_file) as image:
                st.image(image, caption="Uploaded Recipe", use_column_width=True)

                # Convert to numpy array for EasyOCR
                image_array = np.array(image)

                # OCR
                try:
                    ocr_results = reader.readtext(image_array)
                except Exception as e:
                    st.error(f"OCR processing failed: {e}")
                    ocr_results = []

                if not ocr_results:
                    st.warning("No text detected. Try a clearer image.")
                    raw_text = ""
                else:
                    # Join OCR fragments into one cleaned string
                    raw_text = " ".join([res[1] for res in ocr_results])

                st.write("### Extracted Text (Raw OCR):")
                st.write(raw_text or "— no text extracted —")

                # Basic cleaning
                text = raw_text.lower()
                text = re.sub(r'[^a-z\s]', ' ', text)
                text = re.sub(r'\s+', ' ', text).strip()

                # Detect ingredients by simple presence check
                detected = []
                for ingr in KNOWN_INGREDIENTS:
                    if ingr in text:
                        detected.append(ingr)

                st.write("### Detected Ingredients:")
                if detected:
                    st.write(", ".join(sorted(set(detected))))
                else:
                    st.write("No ingredients detected with the simple matcher.")

                # Simple add-on suggestions
                add_ons = []
                if any(x in detected for x in ["parmesan", "parmesan cheese", "mozzarella", "cheese"]):
                    add_ons.append("Extra Parmesan Cheese")
                if any(x in detected for x in ["chicken", "chicken breast"]):
                    add_ons.append("Herb Marinade Pack")
                if any(x in detected for x in ["lettuce", "tomato", "spinach"]):
                    add_ons.append("Organic Dressing Pack")

                st.write("### Suggested Add-Ons:")
                if add_ons:
                    st.write(", ".join(add_ons))
                else:
                    st.write("No add-ons suggested.")
        except UnidentifiedImageError:
            st.error("Uploaded file is not a valid image. Please upload JPG or PNG.")
        except Exception as e:
            st.error(f"Unexpected error: {e}")
            with st.expander("Debug info"):
                import traceback
                st.text(traceback.format_exc())
