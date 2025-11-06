import streamlit as st
import numpy as np
import base64

st.set_page_config(
    page_title="Diabetes Home Risk Checker",
    layout="centered",
    initial_sidebar_state="collapsed"
)

BACKGROUND_IMAGE_PATH = "castorice-honkai-7680x4320-22114.jpg"

def set_background(img_path):
    with open(img_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    css = f"""
    <style>

    /* NỀN */
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpg;base64,{b64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        animation: fadeIn 1.2s ease-in-out;
    }}

    /* HỘP NỘI DUNG */
    div.block-container {{
        background: rgba(0, 0, 0, 0.55);
        border-radius: 18px;
        padding: 2rem;
        box-shadow: 0 0 20px rgba(170, 200, 255, 0.35);
        color: #ffffff;
        animation: slideUp 0.8s ease-out;
    }}

    /* CHỮ */
    h1, h2, h3 {{
        color: #d7e3ff;
        text-shadow: 0 0 8px #75aaff;
        text-align: center;
    }}

    /* NÚT */
    .stButton>button {{
        background: linear-gradient(90deg, #6fb5ff, #b88cff);
        border-radius: 10px;
        border: none;
        color: black;
        width: 100%;
        padding: 0.6rem;
        font-weight: bold;
        transition: 0.25s;
    }}

    .stButton>button:hover {{
        transform: scale(1.05);
        box-shadow: 0 0 12px #b88cff;
    }}

    /* ANIMATION */
    @keyframes fadeIn {{
        0% {{opacity: 0;}}
        100% {{opacity: 1;}}
    }}

    @keyframes slideUp {{
        0% {{transform: translateY(25px); opacity: 0;}}
        100% {{transform: translateY(0); opacity: 1;}}
    }}

    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ✅ GỌI HÀM BACKGROUND
set_background(BACKGROUND_IMAGE_PATH)

st.title("DỰ ĐOÁN NGUY CƠ MẮC TIỂU ĐƯỜNG")
st.markdown("Chỉ cần trả lời một số câu hỏi đơn giản")

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
