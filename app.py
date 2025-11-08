import streamlit as st
import numpy as np
import base64

st.set_page_config(page_title="Diabetes Home Risk Checker", layout="centered")

# ---- BACKGROUND ----
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

    /* THANH MENU */
    .top-menu {{
        width: 100%;
        padding: 12px 35px;
        position: fixed;
        top: 0;
        left: 0;
        z-index: 50;
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(10px);
        border-bottom: 1px solid rgba(255,255,255,0.18);
    }}

    .menu-items a {{
        margin-right: 25px;
        font-weight: 700;
        color: white;
        text-decoration: none;
        cursor: pointer;
        transition: 0.25s;
        text-shadow: 0 0 9px #5bd8ff;
    }}

    .menu-items a:hover {{
        color: #b0d3ff;
        text-shadow: 0 0 14px #c7d9ff;
    }}

    .logo-text {{
        font-size: 26px;
        font-weight: 900;
        color: white;
        text-shadow: 0 0 12px #79c3ff;
    }}

    /* KHUNG FORM */
    .glass-box {{
        background: rgba(255, 255, 255, 0.14);
        border-radius: 20px;
        padding: 2rem;
        margin-top: 80px;
        border: 1px solid rgba(255,255,255,0.3);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        box-shadow: 0 0 25px rgba(120,150,255,0.35);
        color: white;
        animation: slideUp 0.8s ease-out;
    }}

    h1 {{
        text-align: center;
        color: white;
        font-weight: 800;
        text-shadow: 0 0 12px #7acbff;
    }}

    label, p {{
        color: white !important;
        font-weight: 600;
    }}

    .start-btn button {{
        background: linear-gradient(90deg,#00eaff,#7b5bff);
        width: 260px;
        padding: 0.7rem;
        border-radius: 10px;
        border: none;
        font-weight: bold;
        color: black;
        transition: 0.22s;
    }}

    .start-btn button:hover {{
        transform: scale(1.07);
        box-shadow: 0 0 15px #7b5bff;
    }}

    .stProgress > div > div {{
        transition: width 1.4s ease-in-out;
    }}

    @keyframes fadeIn {{
        0% {{opacity:0;}}
        100% {{opacity:1;}}
    }}
    @keyframes slideUp {{
        0% {{transform:translateY(25px); opacity:0;}}
        100% {{transform:translateY(0); opacity:1;}}
    }}

    </style>

    <div class="top-menu">
        <div class="logo-text">StellaSora Health</div>
        <div class="menu-items">
            <a onclick="document.location.href='/?page=home'">HOME</a>
            <a onclick="document.location.href='/?page=info'">INFO</a>
            <a onclick="document.location.href='/?page=contact'">CONTACT</a>
            <a onclick="document.location.href='/?page=survey'">BẮT ĐẦU DỰ ĐOÁN</a>
        </div>
    </div>
    """
    st.markdown(css, unsafe_allow_html=True)

set_background(BACKGROUND_IMAGE_PATH)


# ========== PHÂN TRANG ==========
page = st.experimental_get_query_params().get("page", ["home"])[0]


# ✅ HOME – Landing giống game
if page == "home":
    st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
    st.title("🩺 Dự đoán nguy cơ tiểu đường ngay tại nhà")
    st.write("Hệ thống đánh giá nhanh các yếu tố nguy cơ mà **không cần xét nghiệm**.")
    st.write("→ Nhấn **BẮT ĐẦU DỰ ĐOÁN** ở góc trên để thực hiện.")
    st.markdown("</div>", unsafe_allow_html=True)


# ✅ INFO PAGE
elif page == "info":
    st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
    st.title("ℹ Thông tin về đái tháo đường")
    st.write("""
    - Là bệnh rối loạn chuyển hóa đường huyết
    - Gây tổn thương tim, thận, mắt, thần kinh nếu kéo dài
    - Yếu tố nguy cơ: thừa cân, ăn ngọt, lười vận động, tuổi cao
    - Nên khám định kỳ và kiểm soát lối sống
    """)
    st.markdown("</div>", unsafe_allow_html=True)


# ✅ CONTACT PAGE
elif page == "contact":
    st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
    st.title("📩 Liên hệ hỗ trợ")
    st.write("• Hotline: 1900-xxxxxx")
    st.write("• Email: support@health.ai")
    st.write("• Đơn vị phát triển: StellaSora Health")
    st.markdown("</div>", unsafe_allow_html=True)


# ✅ SURVEY PAGE (form tính điểm)
elif page == "survey":
    st.markdown("<div class='glass-box'>", unsafe_allow_html=True)
    st.title("DỰ ĐOÁN NGUY CƠ MẮC TIỂU ĐƯỜNG")
    st.markdown("Trả lời vài câu hỏi đơn giản:")

    age = st.number_input("Tuổi của bạn:", min_value=1, max_value=120, step=1)
    activity = st.selectbox("Bạn vận động bao lâu mỗi ngày?", [
        "Ít hoặc không vận động","10–30 phút","30–60 phút","Trên 1 giờ"
    ])
    sweet_drink = st.selectbox("Bạn uống nước ngọt/đồ uống có đường?", [
        "Hầu như không","1–2 lần/tuần","3–6 lần/tuần","Mỗi ngày"
    ])
    family = st.selectbox("Gia đình có người mắc đái tháo đường?", ["Không","Có"])
    symptoms = st.multiselect("Triệu chứng:", [
        "Khát nước nhiều","Đi tiểu nhiều","Giảm cân nhanh","Mệt mỏi","Nhìn mờ"
    ])
    belly = st.selectbox("Vòng bụng:", ["Bình thường","Hơi to","To rõ"])
    over_weight = st.selectbox("Bạn có dư cân?", [
        "Không","Có, hơi dư cân","Có, thừa cân rõ"
    ])

    if st.button("✅ Tính kết quả"):
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
            st.error("🚨 Nguy cơ cao – bạn nên đi khám và xét nghiệm.")
        elif risk_pct >= 40:
            st.warning("⚠ Trung bình – cần kiểm soát lối sống.")
        else:
            st.info("✅ Nguy cơ thấp – tiếp tục duy trì thói quen tốt.")

    st.markdown("</div>", unsafe_allow_html=True)


# ✅ Footer
st.markdown("<br><center><small>© StellaSora Health — Tham khảo, không thay thế bác sĩ.</small></center>", unsafe_allow_html=True)
