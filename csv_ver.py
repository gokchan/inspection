import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ========== CONFIG ==========

# Where to save the CSV file (in a hidden folder)
DATA_DIR = ".data2"
CSV_PATH = os.path.join(DATA_DIR, "inspection_data.csv")

# Create the folder if it doesn't exist
os.makedirs(DATA_DIR, exist_ok=True)

# ========== FORM SETUP ==========

areas = [
    "Yorunge Dinlenme Alani (PVC Yani)",
    "Dolunay Sealer Dinlenme Alani (Yeni Sealer)",
    "Sealer Buck (Eski Sealer)",
    "Gokkusagi SVO",
    "Gun Isigi",
    "Cayland Kabin (Yeni Boya Kabini)",
    "Kabin Dunyasi (Eski Kabin)",
    "Yildiz Zimpara"
]

questions = [
    "Duvarlari temiz mi?",
    "Yerler temiz mi?",
    "Koltuklar temiz mi?",
    "Masa ustleri temiz mi?",
    "Aydinlatma yeterli mi?",
    "Boyasi iyi mi?",
    "Koltuklar yeterli mi?",
    "Sehbalar yeterli mi?"
]

# ========== SAVE FUNCTION ==========

def save_to_csv(name, shift, area, responses, comment):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data = {
        "Ad": name,
        "Vardiya": shift,
        "Alan": area,
        "Tarih & Saat": now,
        **responses,
        "Aciklama": comment
    }

    df_new = pd.DataFrame([data])

    # Append or create CSV
    if os.path.exists(CSV_PATH):
        df_new.to_csv(CSV_PATH, mode='a', index=False, header=False)
    else:
        df_new.to_csv(CSV_PATH, index=False)

# ========== STREAMLIT UI ==========

st.set_page_config(page_title="Mobil Denetleme Formu", layout="centered")
st.title("📋 Mobil Denetleme Formu")

# Step control
if "step" not in st.session_state:
    st.session_state.step = 1
if "name" not in st.session_state:
    st.session_state.name = ""
if "shift" not in st.session_state:
    st.session_state.shift = ""
if "area" not in st.session_state:
    st.session_state.area = ""

# Step 1: Name and Shift
if st.session_state.step == 1:
    st.subheader("1. Adim: Ad ve Vardiya")

    name = st.text_input("Adiniz Soyadiniz *")
    shift = st.selectbox("Vardiyaniz *", ["", "A", "B", "C"])

    if st.button("Ileri"):
        if not name or not shift:
            st.error("Lutfen tum alanlari doldurun.")
        else:
            st.session_state.name = name
            st.session_state.shift = shift
            st.session_state.step = 2

# Step 2: Area Selection
elif st.session_state.step == 2:
    st.subheader("2. Adim: Denetlenecek Alan")

    area = st.selectbox("Denetlenecek Alan *", [""] + areas)

    col1, col2 = st.columns(2)
    if col1.button("Geri"):
        st.session_state.step = 1
    if col2.button("Ileri"):
        if not area:
            st.error("Lutfen bir alan secin.")
        else:
            st.session_state.area = area
            st.session_state.step = 3

# Step 3: Questions + Comment + Submit
elif st.session_state.step == 3:
    st.subheader("3. Adim: Denetim Sorulari")

    responses = {}
    for q in questions:
        response = st.selectbox(q, ["Evet", "Hayir"], key=q)
        responses[q] = response

    comment = st.text_area("Aciklama / Yorum")

    col1, col2 = st.columns(2)
    if col1.button("Geri"):
        st.session_state.step = 2

    if col2.button("Gonder"):
        save_to_csv(
            st.session_state.name,
            st.session_state.shift,
            st.session_state.area,
            responses,
            comment
        )
        st.success("✅ Form basariyla kaydedildi.")
        st.session_state.step = 1
