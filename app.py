import streamlit as st
from PIL import Image, UnidentifiedImageError
import easyocr
import numpy as np
import re

st.set_page_config(page_title="HelloFresh Add-On Demo", layout="centered")

# Known ingredients
KNOWN_INGREDIENTS = [
    "chicken", "chicken breast", "parmesan", "parmesan cheese", "mozzarella",
    "cheese", "pasta", "spaghetti", "rice", "lettuce",
    "tomato", "onion", "garlic", "basil", "olive oil", "carrot",
    "potato", "pepper", "salt", "vinegar", "spinach", "mushroom",
    "cream", "milk", "egg", "bread", "lemon", "lime", "butter"
]

# Mock inventory (pretend backend)
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

# Add-on logic mapping
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
            ocr_results = reader.readtext(image_array)
            raw_text = " ".join([res[1] for res in ocr_results]).lower()
            raw_text = re.sub(r'[^a-z\s]', ' ', raw_text)

            detected = [i for i in KNOWN_INGREDIENTS if i in raw_text]

            st.subheader("🧾 Detected Ingredients:")
            if detected:
                st.write(", ".join(sorted(set(detected))))
            else:
                st.warning("No ingredients detected.")

            # Inventory and add-ons display
            st.subheader("📦 Inventory Check:")
            in_stock, out_stock = [], []
            for i in detected:
                if INVENTORY.get(i, False):
                    in_stock.append(i)
                else:
                    out_stock.append(i)

            col1, col2 = st.columns(2)
            with col1:
                st.success("✅ In Stock:")
                if in_stock:
                    st.write(", ".join(in_stock))
                else:
                    st.write("None")
            with col2:
                st.error("❌ Out of Stock:")
                if out_stock:
                    st.write(", ".join(out_stock))
                else:
                    st.write("None")

            # Suggested add-ons for available ingredients
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
