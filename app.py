import streamlit as st
import numpy as np
import base64
import time

st.set_page_config(
    page_title="Diabetes Risk Checker",
    page_title="Diabetes Home Risk Checker",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==== BACKGROUND ====
BACKGROUND_IMAGE_PATH = "castorice-honkai-7680x4320-22114.jpg"

def set_background(img_path):
    try:
        with open(img_path, "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
    except:
        b64 = ""
    with open(img_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()

    css = f"""
    <style>

    /* ======= NỀN FULL ANIME ======= */
    [data-testid="stAppViewContainer"] {{
        {"background-image: url('data:image/jpg;base64,"+b64+"');" if b64 else ""}
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
        background-color: #000;
    }}

    div.block-container {{
        background: rgba(0, 0, 0, 0.55);
        border-radius: 18px;
        padding: 1.6rem;
        box-shadow: 0 0 20px rgba(170, 200, 255, 0.28);
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
        animation: slideUp 0.6s ease-out;
        max-width: 900px;
        margin: auto;
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
        color: #d7e3ff;
        text-shadow: 0 0 8px #75aaff;
        color: #ffffff;
        text-align: center;
        font-weight: 800;
        text-shadow: 0 0 12px #7acbff;
    }}

    label {{
        color: white !important;
        color: #ffffff !important;
        font-weight: 600;
    }}

    /* ======= BUTTON ======= */
    .stButton>button {{
        background: linear-gradient(90deg, #6fb5ff, #b88cff);
        border-radius: 10px;
        background: linear-gradient(90deg, #0defff, #6b5bff);
        border-radius: 12px;
        border: none;
        color: black;
        color: #000;
        width: 100%;
        padding: 0.6rem;
        padding: 0.65rem;
        font-weight: bold;
        transition: 0.18s;
        transition: 0.25s;
    }}

    .stButton>button:hover {{
        transform: scale(1.05);
        box-shadow: 0 0 12px #b88cff;
        box-shadow: 0 0 18px #6b5bff;
    }}

    /* ======= ANIMATION ======= */
    @keyframes fadeIn {{
        0% {{opacity: 0;}}
        100% {{opacity: 1;}}
    }}

    @keyframes slideUp {{
        0% {{transform: translateY(18px); opacity: 0;}}
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

st.title("DỰ ĐOÁN NGUY CƠ MẮC ĐÁI THÁO ĐƯỜNG")
st.title("DỰ ĐOÁN NGUY CƠ MẮC TIỂU ĐƯỜNG")
st.markdown("Chỉ cần trả lời một số câu hỏi đơn giản")

mode = st.selectbox("Chọn chế độ:", ["Tại nhà", "Chế độ máy"])
st.markdown("---")
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
st.caption("Công cụ tham khảo — không thay thế chẩn đoán y khoa.")
st.caption("Công cụ chỉ mang tính tham khảo — không thay thế bác sĩ.")
