import streamlit as st
import numpy as np
import base64
import time

st.set_page_config(
    page_title="Diabetes Risk Checker",
    layout="centered",
    initial_sidebar_state="collapsed"
)

BACKGROUND_IMAGE_PATH = "castorice-honkai-7680x4320-22114.jpg"

def set_background(img_path):
    try:
        with open(img_path, "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
    except:
        b64 = ""

    css = f"""
    <style>
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
        margin: auto;
    }}

    h1, h2, h3 {{
        color: #d7e3ff;
        text-shadow: 0 0 8px #75aaff;
        text-align: center;
    }}

    label {{
        color: white !important;
    }}

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

st.title("DỰ ĐOÁN NGUY CƠ MẮC ĐÁI THÁO ĐƯỜNG")

mode = st.selectbox("Chọn chế độ:", ["Tại nhà", "Chế độ máy"])
st.markdown("---")


# ========== TẠI NHÀ ==========
def home_mode():
    age = st.number_input("Tuổi:", 1, 120, 1)
    activity = st.selectbox("Bạn vận động bao lâu mỗi ngày?", [
        "Ít hoặc không vận động", "10–30 phút", "30–60 phút", "Trên 1 giờ"
    ])
    sweet = st.selectbox("Bạn uống nước ngọt/đồ uống có đường?", [
        "Hầu như không","1–2 lần/tuần","3–6 lần/tuần","Mỗi ngày"
    ])
    family = st.selectbox("Gia đình có người mắc đái tháo đường?", ["Không","Có"])
    symptoms = st.multiselect("Bạn có các triệu chứng sau không?", [
        "Khát nước nhiều","Đi tiểu nhiều","Giảm cân nhanh","Mệt mỏi","Nhìn mờ"
    ])
    belly = st.selectbox("Vòng bụng:", ["Bình thường","Hơi to","To rõ"])
    over = st.selectbox("Cảm giác dư cân:", ["Không","Có, hơi dư cân","Có, thừa cân rõ"])

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

        # ✅ Animation progress bar
        bar = st.progress(0)
        for i in range(0, int(risk)+1):
            bar.progress(i/100)
            time.sleep(0.010)

        st.write(f"Nguy cơ mắc đái tháo đường: **{risk:.1f}%**")

        # ✅ Cảnh báo giống chế độ máy
        if risk >= 70:
            st.error("Nguy cơ cao – nên đi khám và xét nghiệm HbA1c.")
        elif risk >= 40:
            st.warning("Nguy cơ trung bình – nên kiểm soát cân nặng, vận động, ăn uống.")
        else:
            st.info("Nguy cơ thấp – hãy giữ lối sống lành mạnh.")


# ========== CHẾ ĐỘ MÁY ==========
def hospital_mode():
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LogisticRegression

    pregnancies = st.number_input("Số lần mang thai (nếu không có để 0):", 0, 50, 0)
    glucose = st.number_input("Glucose (mg/dL):", 0.0, 500.0, 0.0)
    bp = st.number_input("Huyết áp tâm trương (mmHg):", 0.0, 200.0, 0.0)
    bmi = st.number_input("BMI (kg/m²):", 0.0, 80.0, 0.0)
    age = st.number_input("Tuổi:", 1, 120, 1)

    if st.button("Dự đoán"):
        url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
        cols = ["Pregnancies","Glucose","BloodPressure","SkinThickness","Insulin","BMI","DiabetesPedigree","Age","Outcome"]

        df = pd.read_csv(url, header=None, names=cols)
        df = df.drop(columns=["SkinThickness","Insulin","DiabetesPedigree"])

        for c in ["Glucose","BloodPressure","BMI"]:
            df[c] = df[c].replace(0, np.nan)
            df[c] = df[c].fillna(df[c].median())

        X = df.drop(columns=["Outcome"])
        y = df["Outcome"]

        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        from sklearn.linear_model import LogisticRegression
        model = LogisticRegression(max_iter=1000, solver='liblinear')
        model.fit(X_train, y_train)

        x_input = np.array([pregnancies, glucose, bp, bmi, age]).reshape(1, -1)
        proba = model.predict_proba(x_input)[0,1]
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


# ========== RUN UI ==========
if mode == "Tại nhà":
    home_mode()
else:
    hospital_mode()

st.markdown("---")
st.caption("Công cụ tham khảo — không thay thế chẩn đoán y khoa.")
