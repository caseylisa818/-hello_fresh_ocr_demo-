import streamlit as st
from PIL import Image, UnidentifiedImageError
import numpy as np
import re

st.set_page_config(page_title="HelloFresh Add-On Demo", layout="centered")

KNOWN_INGREDIENTS = [
    "chicken", "chicken breast", "parmesan", "parmesan cheese", "mozzarella",
    "cheese", "pasta", "spaghetti", "rice", "lettuce",
    "tomato", "onion", "garlic", "basil", "olive oil", "carrot",
    "potato", "pepper", "salt", "vinegar", "spinach", "mushroom",
    "cream", "milk", "egg", "bread", "lemon", "lime", "butter"
]

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

st.title("🍽️ HelloFresh Add-On Demo")
st.caption("Upload a recipe image to extract ingredients and match with HelloFresh inventory.")

# Try to import EasyOCR, skip if not available
try:
    import easyocr
    @st.cache_resource
    def get_reader():
        return easyocr.Reader(['en'], gpu=False)
    reader = get_reader()
    OCR_AVAILABLE = True
except Exception as e:
    st.warning("⚠️ EasyOCR failed to load. Using placeholder text extraction.")
    OCR_AVAILABLE = False

uploaded_file = st.file_uploader("Upload recipe photo...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    try:
        with Image.open(uploaded_file) as image:
            st.image(image, caption="Uploaded Recipe", use_column_width=True)

            if OCR_AVAILABLE:
                import numpy as np
                image_array = np.array(image)
                ocr_results = reader.readtext(image_array)
                raw_text = " ".join([res[1] for res in ocr_results]).lower()
            else:
                # Dummy placeholder text so app runs without OCR
                raw_text = "chicken parmesan garlic basil butter"

            text = re.sub(r'[^a-z\s]', ' ', raw_text)

            detected = [i for i in KNOWN_INGREDIENTS if i in text]

            st.subheader("🧾 Detected Ingredients:")
            st.write(", ".join(sorted(set(detected))) if detected else "None")

            # Inventory check
            st.subheader("📦 Inventory Check:")
            in_stock = [i for i in detected if INVENTORY.get(i, False)]
            out_stock = [i for i in detected if not INVENTORY.get(i, False)]

            col1, col2 = st.columns(2)
            with col1:
                st.success("✅ In Stock:")
                st.write(", ".join(in_stock) if in_stock else "None")
            with col2:
                st.error("❌ Out of Stock:")
                st.write(", ".join(out_stock) if out_stock else "None")

            # Add-ons
            st.subheader("💡 Suggested Add-Ons:")
            suggestions = [ADD_ONS[i] for i in in_stock if i in ADD_ONS]
            if suggestions:
                for s in suggestions:
                    st.write(f"• {s}")
            else:
                st.write("No add-ons available for current inventory.")

    except UnidentifiedImageError:
        st.error("Not a valid image file.")
    except Exception as e:
        st.error(f"Error: {e}")
