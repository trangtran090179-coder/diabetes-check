import streamlit as st
import numpy as np
import base64
import requests
from streamlit_lottie import st_lottie

# --------------------------------
# Cấu hình trang
# --------------------------------
st.set_page_config(
    page_title="Diabetes Home Risk Checker",
    layout="centered",
    initial_sidebar_state="collapsed"
)

BACKGROUND_IMAGE_PATH = "castorice-honkai-7680x4320-22114.jpg"

# --------------------------------
# Hàm đặt background
# --------------------------------
def set_background(img_path):
    with open(img_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    css = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpg;base64,{b64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    div.block-container {{
        background: rgba(255, 255, 255, 0.83);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 4px 25px rgba(0,0,0,0.25);
        color: #222;
        animation: fadein 1s ease;
    }}
    h1 {{
        color: #ff4d6d;
        text-shadow: 0px 0px 6px rgba(255, 0, 93, 0.6);
        animation: glow 2s infinite alternate ease-in-out;
    }}

    @keyframes fadein {{
        from {{ opacity:0; transform: translateY(20px); }}
        to {{ opacity:1; transform: translateY(0px); }}
    }}

    @keyframes glow {{
        from {{ text-shadow:0px 0px 6px #ff4d6d; }}
        to   {{ text-shadow:0px 0px 16px #ff006e; }}
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# --------------------------------
# Hàm load Lottie animation
# --------------------------------
def load_lottie(url):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
    except:
        return None


# --------------------------------
# Bắt đầu giao diện
# --------------------------------
set_background(BACKGROUND_IMAGE_PATH)

lottie_health = load_lottie("https://assets10.lottiefiles.com/packages/lf20_jcikwtux.json")

st.title("DỰ ĐOÁN NGUY CƠ MẮC ĐÁI THÁO ĐƯỜNG")

if lottie_health:
    st_lottie(lottie_health, height=180)

st.markdown("Hãy trả lời các câu hỏi sau (không cần dụng cụ, tự đánh giá tại nhà):")

# CÂU HỎI
age = st.number_input("Tuổi của bạn:", min_value=1, max_value=120, step=1)

activity = st.selectbox("Bạn vận động bao lâu mỗi ngày?", [
    "Ít hoặc không vận động",
    "10–30 phút",
    "30–60 phút",
    "Trên 1 giờ"
])

sweet_drink = st.selectbox("Bạn uống nước ngọt/đồ uống có đường?", [
    "Hầu như không",
    "1–2 lần/tuần",
    "3–6 lần/tuần",
    "Mỗi ngày"
])

family = st.selectbox("Gia đình có người mắc đái tháo đường?", ["Không", "Có"])

symptoms = st.multiselect(
    "Bạn có các triệu chứng sau không?",
    ["Khát nước nhiều", "Đi tiểu nhiều", "Giảm cân nhanh", "Mệt mỏi", "Nhìn mờ"]
)

belly = st.selectbox("Vòng bụng của bạn:", [
    "Bình thường",
    "Hơi to",
    "To rõ",
])

over_weight = st.selectbox("Bạn có cảm giác dư cân, bụng mỡ không?", [
    "Không",
    "Có, hơi dư cân",
    "Có, thừa cân rõ"
])

# --------------------------------
# KHI NHẤN DỰ ĐOÁN
# --------------------------------
if st.button("🔍 DỰ ĐOÁN NGUY CƠ"):
    score = 0

    if age >= 45: score += 2
    if age >= 60: score += 3
    if activity == "Ít hoặc không vận động": score += 2
    elif activity == "10–30 phút": score += 1
    if sweet_drink == "Mỗi ngày": score += 2
    elif sweet_drink == "3–6 lần/tuần": score += 1
    if family == "Có": score += 3
    score += len(symptoms)
    if belly == "Hơi to": score += 1
    elif belly == "To rõ": score += 2
    if over_weight == "Có, hơi dư cân": score += 1
    elif over_weight == "Có, thừa cân rõ": score += 2

    risk_pct = min(score * 6, 100)

    st.markdown("### ✅ KẾT QUẢ DỰ ĐOÁN:")
    st.progress(risk_pct / 100)
    st.success(f"✨ Nguy cơ mắc đái tháo đường: **{risk_pct:.1f}%**")

    # Animation theo mức nguy cơ
    if risk_pct >= 70:
        ani = load_lottie("https://assets7.lottiefiles.com/packages/lf20_qp1q7mct.json")
        st.error("🚨 Nguy cơ cao — hãy kiểm tra y tế sớm.")
        if ani: st_lottie(ani, height=200)
    elif risk_pct >= 40:
        ani = load_lottie("https://assets1.lottiefiles.com/packages/lf20_6xfqzzab.json")
        st.warning("⚠ Nguy cơ trung bình — kiểm soát cân nặng, ăn uống, tập luyện.")
        if ani: st_lottie(ani, height=200)
    else:
        ani = load_lottie("https://assets8.lottiefiles.com/packages/lf20_H0MOPI.json")
        st.info("✅ Nguy cơ thấp — hãy giữ thói quen sống lành mạnh.")
        if ani: st_lottie(ani, height=200)

st.markdown("---")
st.caption("Công cụ dự đoán — chỉ mang tính tham khảo, không thay thế bác sĩ.")
