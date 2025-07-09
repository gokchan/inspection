import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ========== CONFIG ==========

# Where to save the Excel file (hidden folder)
EXCEL_DIR = ".data"
EXCEL_PATH = os.path.join(EXCEL_DIR, "inspection_data.xlsx")

# Create the folder if it doesn't exist
os.makedirs(EXCEL_DIR, exist_ok=True)

# ========== FORM SETUP ==========

areas = [
    "Yörünge Dinlenme Alanı (PVC Yanı)",
    "Dolunay Sealer Dinlenme Alanı (Yeni Sealer)",
    "Sealer Buck (Eski Sealer)",
    "Gökkuşağı SVO",
    "Gün Işığı",
    "Çayland Kabin (Yeni Boya Kabini)",
    "Kabin Dünyası (Eski Kabin)",
    "Yıldız Zımpara"
]

questions = [
    "Duvarları temiz mi?",
    "Yerler temiz mi?",
    "Koltuklar temiz mi?",
    "Masa üstleri temiz mi?",
    "Aydınlatma yeterli mi?",
    "Boyası iyi mi?",
    "Koltuklar yeterli mi?",
    "Sehbalar yeterli mi?"
]

# ========== SAVE FUNCTION ==========

def save_to_excel(name, shift, area, responses, comment):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    data = {
        "Ad": name,
        "Vardiya": shift,
        "Alan": area,
        "Tarih & Saat": now,
        **responses,
        "Açıklama": comment
    }

    df_new = pd.DataFrame([data])

    if os.path.exists(EXCEL_PATH):
        df_existing = pd.read_excel(EXCEL_PATH)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_combined = df_new

    df_combined.to_excel(EXCEL_PATH, index=False)

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
    st.subheader("1. Adım: Ad ve Vardiya")

    name = st.text_input("Adınız Soyadınız *")
    shift = st.selectbox("Vardiyanız *", ["", "A", "B", "C"])

    if st.button("İleri"):
        if not name or not shift:
            st.error("Lütfen tüm alanları doldurun.")
        else:
            st.session_state.name = name
            st.session_state.shift = shift
            st.session_state.step = 2

# Step 2: Area Selection
elif st.session_state.step == 2:
    st.subheader("2. Adım: Denetlenecek Alan")

    area = st.selectbox("Denetlenecek Alan *", [""] + areas)

    col1, col2 = st.columns(2)
    if col1.button("Geri"):
        st.session_state.step = 1
    if col2.button("İleri"):
        if not area:
            st.error("Lütfen bir alan seçin.")
        else:
            st.session_state.area = area
            st.session_state.step = 3

# Step 3: Questions + Comment + Submit
elif st.session_state.step == 3:
    st.subheader("3. Adım: Denetim Soruları")

    responses = {}
    for q in questions:
        response = st.selectbox(q, ["Evet", "Hayır"], key=q)
        responses[q] = response

    comment = st.text_area("Açıklama / Yorum")

    col1, col2 = st.columns(2)
    if col1.button("Geri"):
        st.session_state.step = 2

    if col2.button("Gönder"):
        save_to_excel(
            st.session_state.name,
            st.session_state.shift,
            st.session_state.area,
            responses,
            comment
        )
        st.success("✅ Form başarıyla kaydedildi.")
        st.balloons()
        st.session_state.step = 1
