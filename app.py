import streamlit as st
import numpy as np
import pandas as pd
import base64
import time
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# ========== Page config ==========
st.set_page_config(page_title="Dự đoán nguy cơ mắc đái tháo đường", layout="centered")
BACKGROUND_IMAGE_PATH = "castorice-honkai-7680x4320-22114.jpg"

# ========== CSS + background ==========
def set_background(img_path):
    try:
        with open(img_path, "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
    except Exception:
        b64 = ""

    css = f"""
    <style>
    /* Hide Streamlit chrome */
    #MainMenu, header, footer, [data-testid="stDecoration"],
    [data-testid="stStatusWidget"], section[data-testid="stSidebar"],
    div[data-testid="stToolbar"], div[data-testid="stHeader"] {{
        display: none !important;
    }}

    /* Remove default container padding so background is full-bleed */
    .block-container {{
        padding: 0 !important;
        margin: 0 auto !important;
    }}

    /* Background */
    [data-testid="stAppViewContainer"] {{
        {"background-image: url('data:image/jpg;base64,"+b64+"');" if b64 else ""}
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: white;
    }}

    /* central box style (we will insert as a div.mainbox) */
    .mainbox {{
        background: rgba(0, 0, 0, 0.56);
        border-radius: 18px;
        padding: 2.0rem;
        box-shadow: 0 0 30px rgba(120, 170, 255, 0.22);
        color: #ffffff;
        max-width: 900px;
        margin: 160px auto;
        backdrop-filter: blur(6px);
        overflow: hidden;
    }}

    /* Heading and labels color */
    h1, h2, h3, label, p, span {{
        color: #fff !important;
        text-shadow: 0 0 8px #95c7ff;
    }}

    /* Buttons look */
    .stButton>button {{
        background: linear-gradient(90deg, #6fb5ff, #b88cff);
        border-radius: 10px;
        border: none;
        color: black;
        width: 100%;
        padding: 0.6rem;
        font-weight: 600;
    }}
    .stButton>button:hover {{
        transform: scale(1.03);
        box-shadow: 0 0 12px #b88cff;
    }}

    /* Start button special style */
    .startButton>button {{
        font-size: 1.05rem;
        width: 260px;
        height: 56px;
        background: linear-gradient(90deg, #9ecbff, #d5a6ff);
        border-radius: 12px;
        color: black;
        font-weight: 700;
        box-shadow: 0 0 18px rgba(160,200,255,0.25);
    }}
    .startButton>button:hover {{
        transform: scale(1.06);
        box-shadow: 0 0 26px rgba(200,160,255,0.45);
    }}

    /* Animation keyframes (slide up + fade) */
    @keyframes slideFadeUp {{
      0%   {{ opacity: 0; transform: translateY(40px) scale(0.98); }}
      60%  {{ opacity: 0.8; transform: translateY(8px) scale(1.01); }}
      100% {{ opacity: 1; transform: translateY(0) scale(1); }}
    }}

    /* Add a class that triggers animation */
    .mainbox.animate {{
        animation: slideFadeUp 0.9s cubic-bezier(.2,.9,.3,1) both;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

set_background(BACKGROUND_IMAGE_PATH)

# ========== App state ==========
if "show_form" not in st.session_state:
    st.session_state.show_form = False

# ========== Intro screen (with Start button) ==========
if not st.session_state.show_form:
    # show a centered mainbox with a start button
    st.markdown("<div class='mainbox'>", unsafe_allow_html=True)
    st.title("DỰ ĐOÁN NGUY CƠ MẮC ĐÁI THÁO ĐƯỜNG")
    st.write("Ứng dụng giúp bạn ước lượng nhanh nguy cơ mắc bệnh dựa trên lối sống hoặc chỉ số y tế cơ bản.")
    st.markdown("<br>", unsafe_allow_html=True)

    # special container for styled start button; we don't animate here
    st.markdown("<div class='startButton' style='text-align:center; margin-top:18px; margin-bottom:4px;'>", unsafe_allow_html=True)
    if st.button("Bắt đầu dự đoán", key="start"):
        st.session_state.show_form = True
        # rerun to show the form (we will insert it with placeholder for animation)
        st.experimental_rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ========== Show form with animation (use placeholder insertion) ==========
# We will write the animated wrapper after a tiny delay so animation triggers.
placeholder = st.empty()

# small delay then render the animated box to force DOM insertion and animation
time.sleep(0.06)  # short delay (60 ms) — adjust if you want slower/faster

# produce the wrapper div with class "mainbox animate"
placeholder.markdown("<div class='mainbox animate'>", unsafe_allow_html=True)

# Now display the Streamlit form controls inside that wrapper
mode = st.selectbox("Chọn chế độ:", ["Tại nhà", "Chế độ máy"])
st.markdown("---")

def home_mode():
    age = st.number_input("Tuổi:", 1, 120, 25)
    activity = st.selectbox("Mức vận động mỗi ngày:", [
        "Ít hoặc không vận động", "10–30 phút", "30–60 phút", "Trên 1 giờ"
    ])
    sweet = st.selectbox("Uống đồ ngọt:", [
        "Hầu như không","1–2 lần/tuần","3–6 lần/tuần","Mỗi ngày"
    ])
    family = st.selectbox("Gia đình có người mắc bệnh:", ["Không","Có"])
    symptoms = st.multiselect("Triệu chứng:", [
        "Khát nước nhiều","Đi tiểu nhiều","Giảm cân nhanh","Mệt mỏi","Nhìn mờ"
    ])
    belly = st.selectbox("Vòng bụng:", ["Bình thường","Hơi to","To rõ"])
    over = st.selectbox("Cảm giác dư cân:", ["Không","Có, hơi dư cân","Có, thừa cân rõ"])

    if st.button("Dự đoán", key="home_predict"):
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
            time.sleep(0.01)
        st.write(f"Nguy cơ mắc đái tháo đường: **{risk:.1f}%**")
        if risk >= 70:
            st.error("Nguy cơ cao – nên đi khám và xét nghiệm HbA1c.")
        elif risk >= 40:
            st.warning("Nguy cơ trung bình – nên kiểm soát cân nặng, vận động, ăn uống.")
        else:
            st.info("Nguy cơ thấp – hãy giữ lối sống lành mạnh.")

def hospital_mode():
    pregnancies = st.number_input("Số lần mang thai (nếu không có để 0):", 0, 50, 0)
    glucose = st.number_input("Glucose (mg/dL):", 0.0, 500.0, 0.0)
    bp = st.number_input("Huyết áp tâm trương (mmHg):", 0.0, 200.0, 0.0)
    bmi = st.number_input("BMI (kg/m²):", 0.0, 80.0, 0.0)
    age = st.number_input("Tuổi:", 1, 120, 1)

    if st.button("Dự đoán", key="hospital_predict"):
        url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
        cols = ["Pregnancies","Glucose","BloodPressure","SkinThickness","Insulin","BMI","DiabetesPedigree","Age","Outcome"]
        df = pd.read_csv(url, header=None, names=cols)
        df = df.drop(columns=["SkinThickness","Insulin","DiabetesPedigree"])
        for c in ["Glucose","BloodPressure","BMI"]:
            df[c] = df[c].replace(0, np.nan)
            df[c] = df[c].fillna(df[c].median())

        X = df.drop(columns=["Outcome"])
        y = df["Outcome"]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = LogisticRegression(max_iter=1000, solver='liblinear')
        model.fit(X_train, y_train)

        x_input = np.array([pregnancies, glucose, bp, bmi, age]).reshape(1, -1)
        proba = model.predict_proba(x_input)[0,1]
        risk_percent = proba * 100

        st.markdown("### Kết quả:")
        bar = st.progress(0)
        for i in range(0, int(risk_percent)+1):
            bar.progress(i/100)
            time.sleep(0.01)
        st.write(f"Xác suất mắc bệnh: **{risk_percent:.1f}%**")
        if risk_percent >= 70:
            st.error("Nguy cơ cao – nên đi khám và xét nghiệm HbA1c.")
        elif risk_percent >= 40:
            st.warning("Nguy cơ trung bình – nên kiểm soát cân nặng, vận động, ăn uống.")
        else:
            st.info("Nguy cơ thấp – hãy giữ lối sống lành mạnh.")

# display the chosen mode
if mode == "Tại nhà":
    home_mode()
else:
    hospital_mode()

# close wrapper div (we inserted with placeholder)
st.markdown("</div>", unsafe_allow_html=True)
