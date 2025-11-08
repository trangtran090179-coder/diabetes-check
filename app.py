import streamlit as st
import base64
import numpy as np

st.set_page_config(
    page_title="Diabetes Risk Checker",
    layout="wide",
    initial_sidebar_state="collapsed"
)

BACKGROUND_IMAGE_PATH = "castorice-honkai-7680x4320-22114.jpg"

def inject_css():
    with open(BACKGROUND_IMAGE_PATH, "rb") as f:
        img_data = f.read()
    b64 = base64.b64encode(img_data).decode()

    css = """
    <style>

    [data-testid="stAppViewContainer"] {
        background-image: url("data:image/png;base64,%s");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        animation: fadeIn 1.2s ease-in-out;
    }

    .top-nav {
        width: 100%;
        display: flex;
        justify-content: center;
        gap: 50px;
        padding: 18px;
        backdrop-filter: blur(6px);
    }

    .nav-btn {
        padding: 10px 20px;
        border-radius: 10px;
        cursor: pointer;
        font-weight: bold;
        text-transform: uppercase;
        background: rgba(255,255,255,0.15);
        color: white;
        transition: 0.3s;
        text-decoration:none;
    }

    .nav-btn:hover {
        background: rgba(255,255,255,0.35);
        transform: scale(1.05);
    }

    .main-title {
        margin-top: 130px;
        text-align: center;
        font-size: 45px;
        color: #ffffff;
        text-shadow: 0 0 12px #75aaff;
        animation: fadeUp 1.3s ease;
    }

    .sub-title {
        text-align: center;
        font-size: 20px;
        color: #d6e9ff;
        margin-top: -10px;
    }

    .center-btn {
        display: flex;
        justify-content: center;
        margin-top: 40px;
    }

    .cta-btn {
        background: linear-gradient(90deg, #6fb5ff, #b88cff);
        border: none;
        padding: 14px 28px;
        font-size: 20px;
        border-radius: 12px;
        font-weight: bold;
        transition: 0.28s;
        cursor: pointer;
        color: black;
    }

    .cta-btn:hover {
        transform: scale(1.08);
        box-shadow: 0 0 15px #b88cff;
    }

    .form-box {
        background: rgba(0,0,0,0.55);
        padding: 25px;
        border-radius: 18px;
        box-shadow: 0 0 22px rgba(170,200,255,0.38);
        animation: fadeUp 0.6s ease;
    }

    .form-title {
        text-align: center;
        font-size: 30px;
        color: #d7e3ff;
        text-shadow: 0 0 10px #75aaff;
        margin-bottom: 10px;
    }

    @keyframes fadeIn {
        0% {opacity:0;}
        100% {opacity:1;}
    }

    @keyframes fadeUp {
        0% {opacity:0; transform: translateY(25px);}
        100% {opacity:1; transform: translateY(0);}
    }

    </style>
    """ % (b64)

    st.markdown(css, unsafe_allow_html=True)

inject_css()

# ============================= UI =============================
st.markdown("""
<div class='top-nav'>
    <div class='nav-btn'>HOME</div>
    <div class='nav-btn'>INFO</div>
    <div class='nav-btn'>CONTACT</div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>Dự đoán nguy cơ tiểu đường ngay tại nhà</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Không cần xét nghiệm. Kết quả tham khảo theo nguy cơ sức khỏe.</div>", unsafe_allow_html=True)

start = st.button("🚀 BẮT ĐẦU DỰ ĐOÁN")

if not start:
    st.stop()

st.markdown("<div class='form-box'>", unsafe_allow_html=True)

mode = st.radio("Chọn chế độ:", ["Tại nhà", "Máy"], horizontal=True)

age = st.number_input("Tuổi:", min_value=1, max_value=120, step=1)

activity = st.selectbox("Bạn vận động bao lâu mỗi ngày?", [
    "Ít hoặc không vận động", "10–30 phút", "30–60 phút", "Trên 1 giờ"
])

sweet = st.selectbox("Bạn uống nước ngọt/đồ có đường?", [
    "Hầu như không", "1–2 lần/tuần", "3–6 lần/tuần", "Mỗi ngày"
])

symptoms = st.multiselect("Triệu chứng:", [
    "Khát nước", "Đi tiểu nhiều", "Giảm cân", "Mệt mỏi", "Nhìn mờ"
])

weight = st.selectbox("Thừa cân?", [
    "Không", "Có, hơi thừa", "Có, thừa nhiều"
])

waist = st.selectbox("Vòng bụng:", [
    "Bình thường", "Hơi to", "To rõ"
])

if mode == "Máy":
    bmi = st.number_input("BMI:", 10.0, 60.0, step=0.1)
    glucose = st.number_input("Đường huyết lúc đói (mg/dL):", 50, 300, step=1)

st.markdown("</div>", unsafe_allow_html=True)

if st.button("✅ TÍNH NGUY CƠ"):

    score = 0

    if age >= 45: score += 2
    if age >= 60: score += 3

    if activity == "Ít hoặc không vận động": score += 2
    elif activity == "10–30 phút": score += 1

    if sweet == "Mỗi ngày": score += 2
    elif sweet == "3–6 lần/tuần": score += 1

    score += len(symptoms)

    if weight == "Có, hơi thừa": score += 1
    elif weight == "Có, thừa nhiều": score += 2

    if waist == "Hơi to": score += 1
    elif waist == "To rõ": score += 2

    if mode == "Máy":
        if bmi > 25: score += 2
        if glucose > 126: score += 3
        elif glucose > 100: score += 1

    risk_pct = min(score * 6, 100)

    st.subheader("✅ Kết quả dự đoán")
    st.progress(risk_pct / 100)
    st.success(f"Nguy cơ mắc tiểu đường: **{risk_pct:.1f}%**")

    if risk_pct >= 70:
        st.error("🚨 Nguy cơ cao – nên đi khám.")
    elif risk_pct >= 40:
        st.warning("⚠ Nguy cơ trung bình – nên điều chỉnh lối sống.")
    else:
        st.info("✅ Nguy cơ thấp – tiếp tục duy trì sức khỏe.")

st.markdown("---")
st.caption("© Công cụ tham khảo, không thay thế bác sĩ.")
