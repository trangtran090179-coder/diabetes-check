import streamlit as st
import numpy as np
import base64
import time
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# --- Cấu hình trang ---
st.set_page_config(
    page_title="Diabetes Risk Checker",
    layout="centered",
    initial_sidebar_state="collapsed"
)

BACKGROUND_IMAGE_PATH = "castorice-honkai-7680x4320-22114.jpg"

# --- Cài đặt ảnh nền + CSS animation + thanh menu + nút nổi ---
def set_background(img_path):
    try:
        with open(img_path, "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
    except:
        b64 = ""

    css = f"""
    <style>
    /* === Background & Layout === */
    [data-testid="stAppViewContainer"] {{
        {"background-image: url('data:image/jpg;base64,"+b64+"');" if b64 else ""}
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        animation: fadeIn 1s ease-in-out;
        background-color: #000;
    }}
    div.block-container {{
        background: rgba(0, 0, 0, 0.55);
        border-radius: 18px;
        padding: 1.6rem;
        box-shadow: 0 0 20px rgba(170, 200, 255, 0.28);
        color: #ffffff;
        animation: slideUp 0.6s ease-out;
        max-width: 900px;
        margin: 5rem auto;
    }}

    /* === Text & Title === */
    h1, h2, h3 {{
        color: #d7e3ff;
        text-shadow: 0 0 8px #75aaff;
        text-align: center;
    }}
    label {{ color: white !important; }}

    /* === Button style === */
    .stButton>button {{
        background: linear-gradient(90deg, #6fb5ff, #b88cff);
        border-radius: 10px;
        border: none;
        color: black;
        width: 100%;
        padding: 0.6rem;
        font-weight: bold;
        transition: 0.18s;
    }}
    .stButton>button:hover {{
        transform: scale(1.05);
        box-shadow: 0 0 12px #b88cff;
    }}

    /* === Top navigation === */
    .topnav {{
        background-color: rgba(0, 0, 0, 0.65);
        overflow: hidden;
        position: fixed;
        top: 0;
        width: 100%;
        z-index: 9999;
        backdrop-filter: blur(8px);
        display: flex;
        justify-content: center;
        align-items: center;
        animation: fadeIn 1s ease-in-out;
    }}
    .topnav a {{
        color: #fff;
        text-align: center;
        padding: 14px 20px;
        text-decoration: none;
        font-weight: bold;
        font-size: 18px;
        transition: 0.3s;
    }}
    .topnav a:hover {{
        color: #75aaff;
        text-shadow: 0 0 8px #75aaff;
    }}

    /* === Floating button (bottom-right) === */
    .floating-button {{
        position: fixed;
        bottom: 25px;
        right: 25px;
        background: linear-gradient(90deg, #6fb5ff, #b88cff);
        color: black;
        border: none;
        border-radius: 50px;
        padding: 16px 26px;
        font-weight: bold;
        font-size: 16px;
        cursor: pointer;
        box-shadow: 0 0 18px rgba(120, 180, 255, 0.5);
        transition: all 0.25s;
        z-index: 9999;
    }}
    .floating-button:hover {{
        transform: scale(1.08);
        box-shadow: 0 0 28px rgba(180, 140, 255, 0.8);
    }}

    @keyframes fadeIn {{
        0% {{opacity: 0;}}
        100% {{opacity: 1;}}
    }}
    @keyframes slideUp {{
        0% {{transform: translateY(18px); opacity: 0;}}
        100% {{transform: translateY(0); opacity: 1;}}
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

set_background(BACKGROUND_IMAGE_PATH)

# --- Thanh menu cố định trên cùng ---
st.markdown("""
<div class="topnav">
  <a href="?page=Home">Home</a>
  <a href="?page=Info">Info</a>
  <a href="?page=Contact">Contact</a>
</div>
""", unsafe_allow_html=True)

# --- Xử lý tham số URL ---
query_params = st.query_params
page = query_params.get("page", ["Home"])[0]

# --- Nội dung từng trang ---
if page == "Home":
    st.title("🩺 Diabetes Risk Checker")
    st.markdown("""
    ### 💡 Chào mừng bạn!
    Đây là công cụ giúp **ước tính nguy cơ mắc bệnh đái tháo đường** qua hai chế độ:
    - 🏡 *Tại nhà*: Dựa trên thói quen sinh hoạt, triệu chứng.
    - 🏥 *Chế độ máy*: Dựa trên dữ liệu y học (Pima Indians Dataset).
    
    👉 Nhấn nút **Bắt đầu dự đoán** ở góc phải để bắt đầu.
    """)

elif page == "Info":
    st.title("ℹ️ Thông tin")
    st.markdown("""
    **Ứng dụng:** Diabetes Risk Checker  
    **Ngôn ngữ:** Python + Streamlit  
    **Dữ liệu huấn luyện:** [Pima Indians Diabetes Dataset (UCI)](https://archive.ics.uci.edu/ml/datasets/Pima+Indians+Diabetes)  

    ⚠️ Đây là công cụ hỗ trợ — **không thay thế chẩn đoán y khoa**.
    """)

elif page == "Contact":
    st.title("📞 Liên hệ")
    st.markdown("""
    - **Tác giả:** Nhóm AI Y tế  
    - **Email:** healthai.project@gmail.com  
    - **GitHub:** [https://github.com/healthai-project](https://github.com/healthai-project)
    """)

elif page == "Predict":
    # --- Form chọn chế độ ---
    st.title("DỰ ĐOÁN NGUY CƠ MẮC ĐÁI THÁO ĐƯỜNG")
    mode = st.selectbox("Chọn chế độ:", ["Tại nhà", "Chế độ máy"])
    st.markdown("---")

    # ========== TẠI NHÀ ==========
    if mode == "Tại nhà":
        age = st.number_input("Tuổi:", 1, 120, 1)
        activity = st.selectbox("Bạn vận động bao lâu mỗi ngày?", [
            "Ít hoặc không vận động", "10–30 phút", "30–60 phút", "Trên 1 giờ"
        ])
        sweet = st.selectbox("Bạn uống nước ngọt/đồ uống có đường?", [
            "Hầu như không", "1–2 lần/tuần", "3–6 lần/tuần", "Mỗi ngày"
        ])
        family = st.selectbox("Gia đình có người mắc đái tháo đường?", ["Không", "Có"])
        symptoms = st.multiselect("Bạn có các triệu chứng sau không?", [
            "Khát nước nhiều", "Đi tiểu nhiều", "Giảm cân nhanh", "Mệt mỏi", "Nhìn mờ"
        ])
        belly = st.selectbox("Vòng bụng:", ["Bình thường", "Hơi to", "To rõ"])
        over = st.selectbox("Cảm giác dư cân:", ["Không", "Có, hơi dư cân", "Có, thừa cân rõ"])

        if st.button("Dự đoán"):
            score = 0
            if age >= 45: score += 2
            if age >= 60: score += 3
            if activity == "Ít hoặc không vận động": score += 2
            elif activity == "10–30 phút": score += 1
            if sweet == "Mỗi ngày": score += 2
            elif sweet == "3–6 lần/tuần": score += 1
            if family == "Có": score += 3
            score += len(symptoms)
            if belly == "Hơi to": score += 1
            elif belly == "To rõ": score += 2
            if over == "Có, hơi dư cân": score += 1
            elif over == "Có, thừa cân rõ": score += 2

            risk = min(score * 6, 100)
            st.markdown("### Kết quả:")
            bar = st.progress(0)
            for i in range(0, int(risk)+1):
                bar.progress(i/100)
                time.sleep(0.010)
            st.write(f"Nguy cơ mắc đái tháo đường: **{risk:.1f}%**")
            if risk >= 70:
                st.error("Nguy cơ cao – nên đi khám và xét nghiệm HbA1c.")
            elif risk >= 40:
                st.warning("Nguy cơ trung bình – nên kiểm soát cân nặng, vận động, ăn uống.")
            else:
                st.info("Nguy cơ thấp – hãy giữ lối sống lành mạnh.")

    # ========== CHẾ ĐỘ MÁY ==========
    else:
        pregnancies = st.number_input("Số lần mang thai (nếu không có để 0):", 0, 50, 0)
        glucose = st.number_input("Glucose (mg/dL):", 0.0, 500.0, 0.0)
        bp = st.number_input("Huyết áp tâm trương (mmHg):", 0.0, 200.0, 0.0)
        bmi = st.number_input("BMI (kg/m²):", 0.0, 80.0, 0.0)
        age = st.number_input("Tuổi:", 1, 120, 1)

        if st.button("Dự đoán"):
            url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
            cols = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI", "DiabetesPedigree", "Age", "Outcome"]
            df = pd.read_csv(url, header=None, names=cols)
            df = df.drop(columns=["SkinThickness", "Insulin", "DiabetesPedigree"])
            for c in ["Glucose", "BloodPressure", "BMI"]:
                df[c] = df[c].replace(0, np.nan)
                df[c] = df[c].fillna(df[c].median())

            X = df.drop(columns=["Outcome"])
            y = df["Outcome"]
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            model = LogisticRegression(max_iter=1000, solver='liblinear')
            model.fit(X_train, y_train)

            x_input = np.array([pregnancies, glucose, bp, bmi, age]).reshape(1, -1)
            proba = model.predict_proba(x_input)[0, 1]
            risk_percent = proba * 100

            st.markdown("### Kết quả:")
            bar = st.progress(0)
            for i in range(0, int(risk_percent)+1):
                bar.progress(i/100)
                time.sleep(0.010)
            st.write(f"Xác suất mắc bệnh: **{risk_percent:.1f}%**")
            if risk_percent >= 70:
                st.error("Nguy cơ cao – nên đi khám và xét nghiệm HbA1c.")
            elif risk_percent >= 40:
                st.warning("Nguy cơ trung bình – nên kiểm soát cân nặng, vận động, ăn uống.")
            else:
                st.info("Nguy cơ thấp – hãy giữ lối sống lành mạnh.")

# --- Nút nổi dưới góc phải ---
st.markdown("""
<button class="floating-button" onclick="window.location.href='?page=Predict'">
🔮 Bắt đầu dự đoán
</button>
""", unsafe_allow_html=True)

st.markdown("---")
st.caption("Công cụ tham khảo — không thay thế chẩn đoán y khoa.")
