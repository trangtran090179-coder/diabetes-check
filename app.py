import streamlit as st
import numpy as np
import base64
from streamlit_lottie import st_lottie
import requests

# ========================
# CONFIG
# ========================
st.set_page_config(
    page_title="Diabetes Risk System",
    page_icon="",
    layout="centered"
)

# ========================
# BACKGROUND + CSS
# ========================
def set_background(img_url):
    bg = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("{img_url}");
        background-size: cover;
        background-position: center;
    }}

    div.block-container {{
        background: rgba(10, 10, 25, 0.78);
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 0 25px rgba(120, 180, 255, 0.3);
        color: #e6f2ff;
        border: 1px solid rgba(180, 220, 255, 0.25);
    }}

    h1, h2, h3 {{
        text-align: center;
        font-weight: bold;
        color: #9cc9ff;
        text-shadow: 0px 0px 8px #7bbaff;
    }}

    .stButton>button {{
        background: linear-gradient(135deg, #4a9fff, #7a47ff);
        border: none;
        border-radius: 12px;
        color: white;
        font-size: 18px;
        padding: 10px 25px;
        cursor: pointer;
        box-shadow: 0px 0px 10px #7bc4ff;
    }}

    .stButton>button:hover {{
        background: linear-gradient(135deg, #3478ff, #5527ff);
        box-shadow: 0px 0px 15px #b6e0ff;
    }}
    </style>
    """
    st.markdown(bg, unsafe_allow_html=True)

set_background("https://wallpapersden.com/star-rail-4k-firefly-honkai-2024-art-wallpaper/")

# ========================
# LOTTIE ANIMATION
# ========================
def load_lottie(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    return None

lottie = load_lottie("https://assets8.lottiefiles.com/packages/lf20_gljxf5vs.json")

# ========================
# PAGE HEADER
# ========================
st.markdown("<h1>Hệ thống dự đoán nguy cơ đái tháo đường</h1>", unsafe_allow_html=True)

if lottie:
    st_lottie(lottie, height=180, key="anim")

st.markdown(
    """
    <div style='text-align:center; font-size:18px'>
    <br>
    Trả lời vài câu hỏi, hệ thống sẽ tính nguy cơ sức khỏe của bạn.
    </div>
    """,
    unsafe_allow_html=True
)

# ========================
# INPUT QUESTIONS
# ========================
st.subheader("Bắt đầu kiểm tra:")

age = st.slider("➤ Tuổi của bạn:", 1, 80, 20)
activity = st.selectbox("➤ Mức hoạt động hàng ngày:", [
    "Hầu như không vận động",
    "Dưới 30 phút",
    "30–60 phút",
    "Trên 1 giờ"
])
sweet = st.selectbox("➤ Mức độ ăn/uống đồ ngọt:", [
    "Hiếm khi",
    "1–2 lần/tuần",
    "3–6 lần/tuần",
    "Mỗi ngày"
])
family = st.selectbox("➤ Gia đình có người mắc tiểu đường?", ["Không", "Có"])
symptoms = st.multiselect(
    "➤ Bạn có dấu hiệu nào sau đây?",
    ["Khát nhiều", "Đi tiểu nhiều", "Ủ rũ/mệt mỏi", "Giảm cân nhanh", "Hay đói nhanh"]
)
belly = st.selectbox("➤ Tình trạng vòng bụng:", [
    "Bình thường",
    "Hơi to",
    "To rõ"
])

# ========================
# LOGIC – TÍNH RỦI RO
# ========================
if st.button("Dự đoán"):
    score = 0

    # tuổi
    if age >= 45: score += 2
    if age >= 60: score += 3

    # vận động
    if activity == "Hầu như không vận động": score += 2
    elif activity == "Dưới 30 phút": score += 1

    # đồ ngọt
    if sweet == "Mỗi ngày": score += 2
    elif sweet == "3–6 lần/tuần": score += 1

    # gia đình
    if family == "Có": score += 3

    # vòng bụng
    if belly == "Hơi to": score += 1
    elif belly == "To rõ": score += 2

    score += len(symptoms)

    risk = min(score * 7, 100)

    st.markdown("## ⭐ Kết quả phân tích:")
    st.progress(risk / 100)
    st.write(f"### Nguy cơ ước tính: **{risk:.1f}%**")

    if risk >= 70:
        st.error("Nguy cơ cao — hãy đến bệnh viện để xét nghiệm chính xác.")
    elif risk >= 40:
        st.warning("Nguy cơ trung bình — nên tập thể dục và hạn chế đồ ngọt.")
    else:
        st.success("Nguy cơ thấp — giữ lối sống hiện tại!")

st.markdown("<hr>", unsafe_allow_html=True)
st.caption("Công cụ mô phỏng — không thay thế chẩn đoán y tế. Hãy khám bác sĩ nếu có triệu chứng bất thường.")
