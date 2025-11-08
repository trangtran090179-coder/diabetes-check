import streamlit as st
import numpy as np
import base64

st.set_page_config(
    page_title="Diabetes Home Risk Checker",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==== BACKGROUND ====
BACKGROUND_IMAGE_PATH = "castorice-honkai-7680x4320-22114.jpg"

def set_background(img_path):
    with open(img_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()

    css = f"""
    <style>

    /* ======= NỀN FULL ANIME ======= */
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpg;base64,{b64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        animation: fadeIn 1.2s ease-in-out;
    }}

    /* ======= THANH MENU STELLA SORA ======= */
    .top-menu {{
        width: 100%;
        padding: 12px 25px;
        position: fixed;
        top: 0;
        left: 0;
        z-index: 50;
        display: flex;
        justify-content: space-between;
        align-items: center;

        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-bottom: 1px solid rgba(255,255,255,0.25);
        animation: fadeIn 1s ease-in-out;
    }}

    .menu-items a {{
        margin-right: 25px;
        color: #ffffff;
        font-weight: bold;
        text-decoration: none;
        transition: 0.25s;
        text-shadow: 0 0 9px #5bd8ff;
    }}

    .menu-items a:hover {{
        color: #9ab8ff;
        text-shadow: 0 0 15px #d2d6ff;
    }}

    .logo-text {{
        font-size: 26px;
        font-weight: 900;
        color: #ffffff;
        text-shadow: 0 0 12px #7cc9ff;
    }}

    /* ======= GLASS FORM ======= */
    div.block-container {{
        background: rgba(255, 255, 255, 0.13);
        border-radius: 20px;
        padding: 2.3rem;
        border: 1px solid rgba(255,255,255,0.35);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        box-shadow: 0 0 25px rgba(120,150,255,0.35);
        color: #FFFFFF;
        animation: slideUp 0.9s ease-out;
        margin-top: 90px;
    }}

    h1, h2, h3 {{
        color: #ffffff;
        text-align: center;
        font-weight: 800;
        text-shadow: 0 0 12px #7acbff;
    }}

    label {{
        color: #ffffff !important;
        font-weight: 600;
    }}

    /* ======= BUTTON ======= */
    .stButton>button {{
        background: linear-gradient(90deg, #0defff, #6b5bff);
        border-radius: 12px;
        border: none;
        color: #000;
        width: 100%;
        padding: 0.65rem;
        font-weight: bold;
        transition: 0.25s;
    }}

    .stButton>button:hover {{
        transform: scale(1.05);
        box-shadow: 0 0 18px #6b5bff;
    }}

    /* ======= ANIMATION ======= */
    @keyframes fadeIn {{
        0% {{opacity: 0;}}
        100% {{opacity: 1;}}
    }}

    @keyframes slideUp {{
        0% {{transform: translateY(30px); opacity: 0;}}
        100% {{transform: translateY(0); opacity: 1;}}
    }}

    .stProgress > div > div {{
        transition: width 1.2s ease-in-out;
    }}

    </style>

    <div class="top-menu">
        <div class="logo-text">StellaSora Health</div>
        <div class="menu-items">
            <a>HOME</a>
            <a>SURVEY</a>
            <a>INFO</a>
            <a>CONTACT</a>
        </div>
    </div>

    """
    st.markdown(css, unsafe_allow_html=True)


set_background(BACKGROUND_IMAGE_PATH)

st.title("DỰ ĐOÁN NGUY CƠ MẮC TIỂU ĐƯỜNG")
st.markdown("Chỉ cần trả lời một số câu hỏi đơn giản")

# ====== INPUT ======
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

belly = st.selectbox("Vòng bụng của bạn như thế nào?", [
    "Bình thường",
    "Hơi to",
    "To rõ",
])

over_weight = st.selectbox("Bạn có cảm thấy cơ thể dư cân hay bụng mỡ không?", [
    "Không",
    "Có, hơi dư cân",
    "Có, thừa cân rõ"
])

# ====== KẾT QUẢ ======
if st.button("Dự đoán nguy cơ"):

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

    st.markdown("### ✅ Kết quả dự đoán:")
    st.progress(risk_pct / 100)
    st.success(f"Nguy cơ mắc đái tháo đường: **{risk_pct:.1f}%**")

    if risk_pct >= 70:
        st.error("🚨 Nguy cơ cao – bạn nên đi khám và xét nghiệm HbA1c.")
    elif risk_pct >= 40:
        st.warning("⚠ Nguy cơ trung bình – nên kiểm soát cân nặng, vận động, ăn uống.")
    else:
        st.info("✅ Nguy cơ thấp – hãy giữ lối sống lành mạnh.")

st.markdown("---")
st.caption("Công cụ chỉ mang tính tham khảo — không thay thế bác sĩ.")
