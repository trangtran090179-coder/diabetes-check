import streamlit as st
import numpy as np
import pandas as pd
import base64
import time
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# --- Cấu hình trang ---
st.set_page_config(page_title="Diabetes Risk Checker", layout="wide")

BACKGROUND_IMAGE_PATH = "castorice-honkai-7680x4320-22114.jpg"

# --- Đặt ảnh nền ---
def set_background(img_path):
    with open(img_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    css = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/png;base64,{b64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
        animation: fadeIn 1.2s ease-in-out;
    }}
    div.block-container {{
        background: rgba(0, 0, 0, 0.5);
        border-radius: 18px;
        padding: 2rem;
        color: white;
        box-shadow: 0 0 20px rgba(170, 200, 255, 0.25);
        max-width: 900px;
        margin: 5rem auto;
        animation: slideUp 0.6s ease-out;
    }}
    h1, h2, h3 {{
        color: #d7e3ff;
        text-shadow: 0 0 8px #75aaff;
        text-align: center;
    }}
    .topnav {{
        background-color: rgba(0, 0, 0, 0.7);
        overflow: hidden;
        position: fixed;
        top: 0;
        width: 100%;
        z-index: 9999;
        backdrop-filter: blur(6px);
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 0.5rem 0;
    }}
    .topnav a {{
        color: white;
        text-align: center;
        padding: 12px 20px;
        text-decoration: none;
        font-size: 18px;
        font-weight: bold;
        transition: 0.3s;
    }}
    .topnav a:hover {{
        color: #75aaff;
        text-shadow: 0 0 8px #75aaff;
    }}
    .floating-button {{
        position: fixed;
        bottom: 30px;
        right: 30px;
        background: linear-gradient(90deg, #6fb5ff, #b88cff);
        color: black;
        border: none;
        border-radius: 50px;
        padding: 18px 26px;
        font-weight: bold;
        font-size: 16px;
        cursor: pointer;
        box-shadow: 0 0 20px rgba(100, 150, 255, 0.5);
        transition: all 0.25s;
    }}
    .floating-button:hover {{
        transform: scale(1.08);
        box-shadow: 0 0 25px rgba(180, 140, 255, 0.8);
    }}
    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}
    @keyframes slideUp {{
        from {{ transform: translateY(20px); opacity: 0; }}
        to {{ transform: translateY(0); opacity: 1; }}
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

set_background(BACKGROUND_IMAGE_PATH)

# --- Thanh menu trên đầu ---
st.markdown("""
<div class="topnav">
    <a href="?page=Home">Home</a>
    <a href="?page=Info">Info</a>
    <a href="?page=Contact">Contact</a>
</div>
""", unsafe_allow_html=True)

# --- Đọc URL params để xác định trang ---
query_params = st.query_params
page = query_params.get("page", ["Home"])[0]

# --- Hiển thị nội dung ---
if page == "Home":
    st.title("🩺 Diabetes Risk Checker")
    st.markdown("""
    ### 💡 Chào mừng bạn!
    Công cụ này giúp bạn **ước tính nguy cơ mắc bệnh đái tháo đường** qua hai chế độ:
    - 🏡 *Tại nhà*: dựa trên thói quen sinh hoạt, triệu chứng.  
    - 🏥 *Chế độ máy*: dựa trên dữ liệu y học (Pima Indians Diabetes Dataset).  

    👉 Nhấn nút **Bắt đầu dự đoán** ở góc phải để bắt đầu nhé!
    """)
elif page == "Info":
    st.title("ℹ️ Thông tin")
    st.markdown("""
    **Ứng dụng**: Diabetes Risk Checker  
    **Ngôn ngữ**: Python + Streamlit  
    **Dữ liệu huấn luyện**: [Pima Indians Diabetes Dataset (UCI)](https://archive.ics.uci.edu/ml/datasets/Pima+Indians+Diabetes)  
    ⚠️ Đây là công cụ hỗ trợ — **không thay thế chẩn đoán y khoa**.
    """)
elif page == "Contact":
    st.title("📞 Liên hệ")
    st.markdown("""
    - **Tác giả:** Nhóm AI Y tế  
    - **Email:** healthai.project@gmail.com  
    - **GitHub:** [https://github.com/healthai-project](https://github.com/healthai-project)  
    """)

# --- Nếu người dùng nhấn nút “Bắt đầu dự đoán” ---
if st.button("🔮 Bắt đầu dự đoán", key="floating", help="Nhấn để mở trình dự đoán"):
    st.session_state["show_predict"] = True

# --- Hiển thị nút nổi ---
st.markdown("""
<button class="floating-button" onclick="window.location.href='?page=Predict'">
    🔮 Bắt đầu dự đoán
</button>
""", unsafe_allow_html=True)

# --- Trang dự đoán ---
if page == "Predict":
    st.title("DỰ ĐOÁN NGUY CƠ MẮC ĐÁI THÁO ĐƯỜNG")
    mode = st.selectbox("Chọn chế độ:", ["Tại nhà", "Chế độ máy"])
    st.markdown("---")

    # ====== TẠI NHÀ ======
    if mode == "Tại nhà":
        age = st.number_input("Tuổi:", 1, 120, 25)
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
            bar = st.progress(0)
            for i in range(int(risk)+1):
                bar.progress(i/100)
                time.sleep(0.01)

            st.write(f"Nguy cơ mắc đái tháo đường: **{risk:.1f}%**")
            if risk >= 70:
                st.error("Nguy cơ cao – nên đi khám và xét nghiệm HbA1c.")
            elif risk >= 40:
                st.warning("Nguy cơ trung bình – nên kiểm soát cân nặng, vận động, ăn uống.")
            else:
                st.info("Nguy cơ thấp – hãy giữ lối sống lành mạnh.")

    # ====== CHẾ ĐỘ MÁY ======
    else:
        pregnancies = st.number_input("Số lần mang thai:", 0, 50, 0)
        glucose = st.number_input("Glucose (mg/dL):", 0.0, 500.0, 120.0)
        bp = st.number_input("Huyết áp tâm trương (mmHg):", 0.0, 200.0, 70.0)
        bmi = st.number_input("BMI (kg/m²):", 0.0, 80.0, 25.0)
        age = st.number_input("Tuổi:", 1, 120, 30)

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

            bar = st.progress(0)
            for i in range(int(risk_percent)+1):
                bar.progress(i/100)
                time.sleep(0.01)

            st.write(f"Xác suất mắc bệnh: **{risk_percent:.1f}%**")
            if risk_percent >= 70:
                st.error("Nguy cơ cao – nên đi khám và xét nghiệm HbA1c.")
            elif risk_percent >= 40:
                st.warning("Nguy cơ trung bình – nên kiểm soát cân nặng, vận động, ăn uống.")
            else:
                st.info("Nguy cơ thấp – hãy giữ lối sống lành mạnh.")

st.markdown("<br><br>", unsafe_allow_html=True)
st.caption("Công cụ tham khảo — không thay thế chẩn đoán y khoa.")
