import streamlit as st
import numpy as np
import base64

st.set_page_config(
    page_title="Diabetes Risk — Home / Hospital",
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
        animation: fadeIn 1.0s ease-in-out;
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

    label, .stSelectbox, .stNumberInput, .stMultiSelect {{
        color: #ffffff !important;
        font-weight: 500;
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
        animation: btnFade 0.6s ease-out;
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
    @keyframes btnFade {{
        0% {{opacity: 0; transform: scale(0.94);}}
        100% {{opacity: 1; transform: scale(1);}}
    }}

    @keyframes resultPop {{
        0% {{transform: scale(0.75); opacity: 0;}}
        100% {{transform: scale(1); opacity: 1;}}
    }}

    .result-box {{
        animation: resultPop 0.5s ease-out;
    }}

    @media (max-width: 600px) {{
        div.block-container {{
            width: 94%;
            padding: 1rem;
        }}
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

set_background(BACKGROUND_IMAGE_PATH)

st.title("DỰ ĐOÁN NGUY CƠ MẮC ĐÁI THÁO ĐƯỜNG")
st.markdown("Chọn chế độ và nhập thông tin. *'Tại nhà'* không cần thiết bị; *'Bệnh viện'* dùng chỉ số xét nghiệm để mô hình ML dự đoán.")

mode = st.selectbox("Chọn chế độ:", ["Tại nhà", " Máy "])
st.markdown("---")

# ========== MODE HOME ==========
def home_mode_ui():
    st.subheader("Chế độ: Tại nhà ")

    age = st.number_input("Tuổi của bạn:", min_value=1, max_value=120, step=1, key="home_age")

    activity = st.selectbox("Bạn vận động bao lâu mỗi ngày?", [
        "Ít hoặc không vận động", "10–30 phút", "30–60 phút", "Trên 1 giờ"
    ], key="home_act")

    sweet = st.selectbox("Bạn uống nước ngọt/đồ uống có đường?", [
        "Hầu như không","1–2 lần/tuần","3–6 lần/tuần","Mỗi ngày"
    ], key="home_sweet")

    family = st.selectbox("Gia đình có người mắc đái tháo đường?", ["Không","Có"], key="home_family")

    symptoms = st.multiselect("Bạn có các triệu chứng sau không?", [
        "Khát nước nhiều","Đi tiểu nhiều","Giảm cân nhanh","Mệt mỏi","Nhìn mờ"
    ], key="home_sym")

    belly = st.selectbox("Vòng bụng của bạn như thế nào?", ["Bình thường","Hơi to","To rõ"], key="home_belly")

    over = st.selectbox("Bạn có cảm thấy cơ thể dư cân hay bụng mỡ không?",
        ["Không","Có, hơi dư cân","Có, thừa cân rõ"], key="home_over")

    if st.button("Dự đoán nguy cơ (Tại nhà)"):

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

        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.markdown("### ✅ Kết quả dự đoán (Tại nhà):")
        st.progress(risk/100)
        st.success(f"Nguy cơ: **{risk:.1f}%**")
        st.markdown('</div>', unsafe_allow_html=True)

        if risk >= 70:
            st.error("🚨 Nguy cơ cao — nên khám và xét nghiệm HbA1c.")
        elif risk >= 40:
            st.warning("⚠ Trung bình — nên kiểm soát ăn uống & vận động.")
        else:
            st.info("✅ Nguy cơ thấp — tiếp tục lối sống lành mạnh.")

# ========== MODE HOSPITAL ==========
def hospital_mode_ui():
    st.subheader("Chế độ: Máy ")

    try:
        import pandas as pd
        from sklearn.model_selection import train_test_split
        from sklearn.linear_model import LogisticRegression
        from sklearn.metrics import accuracy_score
    except:
        st.error("Thiếu thư viện: pandas, scikit-learn")
        st.info("Cài bằng: pip install pandas scikit-learn")
        return

    pregnancies = st.number_input("Số lần mang thai (nếu không áp dụng để 0):", 0, 50, 0, key="h1")
    glucose = st.number_input("Glucose (mg/dL):", 0.0, 500.0, 0.0, key="h2")
    blood_pressure = st.number_input("Huyết áp tâm trương (mmHg):", 0.0, 200.0, 0.0, key="h3")
    bmi = st.number_input("BMI (kg/m²):", 0.0, 80.0, 0.0, key="h4")
    dpf = st.number_input("Chỉ số tiền sử gia đình (DPF):", 0.0, 5.0, 0.0, key="h5")
    age = st.number_input("Tuổi:", 1, 120, 1, key="h6")

    if st.button("Dự đoán (Bệnh viện)"):

        url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
        cols = ["Pregnancies","Glucose","BloodPressure","SkinThickness","Insulin","BMI","DiabetesPedigree","Age","Outcome"]

        try:
            df = pd.read_csv(url, header=None, names=cols)
        except:
            st.error("Không tải được dataset Pima (lỗi mạng)")
            return

        # GỠ SkinThickness và Insulin khỏi mô hình
        df = df.drop(columns=["SkinThickness","Insulin"])

        for c in ["Glucose","BloodPressure","BMI"]:
            df[c] = df[c].replace(0, np.nan)
            df[c] = df[c].fillna(df[c].median())

        X = df.drop(columns=["Outcome"])
        y = df["Outcome"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = LogisticRegression(max_iter=1000, solver='liblinear')
        model.fit(X_train, y_train)

        x_input = np.array([pregnancies, glucose, blood_pressure, bmi, dpf, age]).reshape(1, -1)
        proba = model.predict_proba(x_input)[0,1]
        pred = int(model.predict(x_input)[0])
        acc = accuracy_score(y_test, model.predict(X_test))

        st.markdown('<div class="result-box">', unsafe_allow_html=True)
        st.markdown("### Kết quả mô hình học máy:")
        st.write(f"Độ chính xác tham khảo: **{acc*100:.1f}%**")
        st.progress(proba)
        st.success(f"Xác suất mắc bệnh: **{proba*100:.1f}%**")
        st.markdown('</div>', unsafe_allow_html=True)

        if proba >= 0.7:
            st.error("🚨 Nguy cơ cao — nên xét nghiệm thêm.")
        elif proba >= 0.4:
            st.warning("⚠ Trung bình — theo dõi và cải thiện lối sống.")
        else:
            st.info("✅ Nguy cơ thấp.")

# ========== show UI ==========
if mode == "Tại nhà":
    home_mode_ui()
else:
    hospital_mode_ui()

st.markdown("---")
st.caption("Công cụ tham khảo — không thay thế chẩn đoán y khoa.")
