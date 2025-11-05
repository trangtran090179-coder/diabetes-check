import streamlit as st
import pandas as pd
import numpy as np
import base64
from io import BytesIO
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import joblib
import requests
from streamlit_lottie import st_lottie

# ========================
# CONFIGURATION
# ========================
st.set_page_config(
    page_title="Diabetes Home Risk Checker",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Path to background image
BACKGROUND_IMAGE_PATH = "cells-at-work-background-k6fmdp1u2fyd0uyq.jpg"

# ========================
# HELPER: Set background via base64 CSS
# ========================
def set_background(img_path):
    with open(img_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    page_bg = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpg;base64,{b64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    [data-testid="stSidebar"], [data-testid="stHeader"], [data-testid="stToolbar"] {{
        background-color: rgba(255,255,255,0);
    }}

    div.block-container {{
        background: rgba(255, 255, 255, 0.85);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 4px 25px rgba(0,0,0,0.15);
        color: #222222;
    }}

    h1, h2, h3, h4, h5, h6 {{
        color: #e63946;
        text-align: center;
    }}

    button[kind="primary"] {{
        background-color: #e63946;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
    }}

    .stButton>button {{
        display: block;
        margin: 0 auto;
    }}
    </style>
    """
    st.markdown(page_bg, unsafe_allow_html=True)


# ========================
# APP CONTENT
# ========================
set_background(BACKGROUND_IMAGE_PATH)
st.title("DỰ ĐOÁN NGUY CƠ MẮC TIỂU ĐƯỜNG")

st.markdown(
    """
    Ứng dụng này giúp bạn **ước lượng nguy cơ mắc tiểu đường** dựa trên các yếu tố sức khỏe có thể tự đo tại nhà.  
    *Kết quả chỉ mang tính tham khảo — không thay thế chẩn đoán y khoa.*
    """
)

# Input fields (chỉ giữ các chỉ số có thể tự đo tại nhà)
age = st.number_input("Tuổi", min_value=1, max_value=120, step=1)
bmi = st.number_input("BMI (kg/m²)", min_value=10.0, max_value=60.0, step=0.1)
waist = st.number_input("Vòng eo (cm)", min_value=40.0, max_value=150.0, step=0.5)
bp = st.number_input("Huyết áp tâm thu (mmHg)", min_value=60.0, max_value=200.0, step=1.0)
glucose = st.number_input("Đường huyết đói (mg/dL)", min_value=50.0, max_value=400.0, step=0.1)
family_history = st.selectbox("Tiền sử gia đình mắc tiểu đường", ["Không", "Có"])

# Convert categorical
family_history = 1 if family_history == "Có" else 0

# Prediction simulation (demo model logic)
if st.button("🔍 Dự đoán nguy cơ"):
    risk_score = (
        0.04 * age
        + 0.12 * bmi
        + 0.08 * (bp / 100)
        + 0.25 * (glucose / 100)
        + 0.15 * family_history
        + 0.05 * (waist / 100)
    )
    risk_pct = np.clip(risk_score * 8, 0, 100)

    st.markdown("### 🔎 Kết quả dự đoán:")
    st.progress(risk_pct / 100)
    st.success(f"Nguy cơ ước tính: **{risk_pct:.1f}%**")

    if risk_pct >= 70:
        st.error("🚨 Nguy cơ cao: Nên đi khám và làm xét nghiệm HbA1c sớm.")
    elif risk_pct >= 40:
        st.warning("⚠️ Nguy cơ trung bình: Hãy kiểm tra sức khỏe định kỳ và duy trì thói quen tốt.")
    else:
        st.info("✅ Nguy cơ thấp: Tiếp tục lối sống lành mạnh nhé!")

# Footer
st.markdown("---")
