import streamlit as st
import numpy as np
import base64

# ========== cấu hình trang ==========
st.set_page_config(
    page_title="Diabetes Risk — Home / Hospital",
    layout="centered",
    initial_sidebar_state="collapsed"
)

BACKGROUND_IMAGE_PATH = "castorice-honkai-7680x4320-22114.jpg"

# ========== hàm set background + CSS (đã tối ưu mobile, chữ trắng) ==========
def set_background(img_path):
    try:
        with open(img_path, "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
    except Exception:
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
        margin-bottom: 8px;
    }}

    /* label / input text màu trắng */
    label, div[data-testid="stMarkdownContainer"], .stSelectbox, .stNumberInput, .stMultiSelect, .stTextInput {{
        color: #ffffff !important;
        font-weight: 500;
        text-shadow: 0 0 6px rgba(255,255,255,0.18);
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
        transform: scale(1.03);
        box-shadow: 0 0 12px #b88cff;
    }}

    .stProgress > div > div > div > div {{
        background: linear-gradient(90deg, #6fb5ff, #b88cff) !important;
    }}

    @keyframes fadeIn {{
        0% {{opacity: 0;}}
        100% {{opacity: 1;}}
    }}
    @keyframes slideUp {{
        0% {{transform: translateY(18px); opacity: 0;}}
        100% {{transform: translateY(0); opacity: 1;}}
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

# gọi background
set_background(BACKGROUND_IMAGE_PATH)

# ========== HEADER + chế độ ==========
st.title("DỰ ĐOÁN NGUY CƠ MẮC ĐÁI THÁO ĐƯỜNG")
st.markdown("Chọn chế độ và nhập thông tin. *'Tại nhà'* không cần thiết bị; *'Bệnh viện'* dùng chỉ số xét nghiệm để mô hình ML dự đoán.")

mode = st.selectbox("Chọn chế độ:", ["Tại nhà (không cần máy)", "Bệnh viện / Máy (dữ liệu xét nghiệm)"])

st.markdown("---")

# =========================
# CHẾ ĐỘ: TẠI NHÀ
# =========================
def home_mode_ui():
    st.subheader("Chế độ: Tại nhà — tự khai (không cần máy)")
    st.markdown("Chỉ cần trả lời một số câu hỏi, hệ thống sẽ ước lượng nguy cơ.")

    age = st.number_input("Tuổi của bạn:", min_value=1, max_value=120, step=1, key="home_age")

    activity = st.selectbox("Bạn vận động bao lâu mỗi ngày?", [
        "Ít hoặc không vận động",
        "10–30 phút",
        "30–60 phút",
        "Trên 1 giờ"
    ], key="home_activity")

    sweet_drink = st.selectbox("Bạn uống nước ngọt/đồ uống có đường?", [
        "Hầu như không",
        "1–2 lần/tuần",
        "3–6 lần/tuần",
        "Mỗi ngày"
    ], key="home_sweet")

    family = st.selectbox("Gia đình có người mắc đái tháo đường?", ["Không", "Có"], key="home_family")

    symptoms = st.multiselect(
        "Bạn có các triệu chứng sau không?",
        ["Khát nước nhiều", "Đi tiểu nhiều", "Giảm cân nhanh", "Mệt mỏi", "Nhìn mờ"],
        key="home_symptoms"
    )

    belly = st.selectbox("Vòng bụng của bạn như thế nào?", [
        "Bình thường",
        "Hơi to",
        "To rõ",
    ], key="home_belly")

    over_weight = st.selectbox("Bạn có cảm thấy cơ thể dư cân hay bụng mỡ không?", [
        "Không",
        "Có, hơi dư cân",
        "Có, thừa cân rõ"
    ], key="home_over")

    if st.button("Dự đoán nguy cơ (Tại nhà)"):
        # giữ nguyên logic tính điểm
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

# =========================
# CHẾ ĐỘ: BỆNH VIỆN / MÁY (ML)
# - dùng chỉ số xét nghiệm (những thứ KHÔNG đo được tại nhà có thể bị bỏ ra ở home mode)
# - huấn luyện nhanh trên Pima dataset (tải từ github)
# =========================
def hospital_mode_ui():
    st.subheader("Chế độ: Bệnh viện / Máy")
    st.markdown("Nhập các chỉ số xét nghiệm ")

    try:
        import pandas as pd
        from sklearn.model_selection import train_test_split
        from sklearn.linear_model import LogisticRegression
        from sklearn.metrics import accuracy_score
    except Exception as e:
        st.error("Thiếu thư viện cần thiết cho chế độ Bệnh viện / Máy.")
        st.info("Cài các gói: pandas, scikit-learn. Trên máy local chạy: pip install pandas scikit-learn")
        st.stop()

    st.markdown("**Các trường nhập (dùng giá trị thực tế từ xét nghiệm hoặc hồ sơ bệnh viện):**")

    # Các chỉ số dùng cho mô hình (các chỉ số này thường do bệnh viện cung cấp)
    pregnancies = st.number_input("Số lần mang thai (nếu không áp dụng để 0):", min_value=0, max_value=50, step=1, key="h_preg")
    glucose = st.number_input("Glucose (mg/dL) — (lưu ý: giá trị xét nghiệm):", min_value=0.0, max_value=500.0, step=0.1, key="h_glucose")
    blood_pressure = st.number_input("Huyết áp (mmHg) (tâm trương trong dataset Pima):", min_value=0.0, max_value=300.0, step=0.1, key="h_bp")
    skin_thickness = st.number_input("Độ dày nếp da (mm):", min_value=0.0, max_value=100.0, step=0.1, key="h_skin")
    insulin = st.number_input("Insulin (mu U/ml):", min_value=0.0, max_value=1000.0, step=0.1, key="h_insulin")
    bmi = st.number_input("BMI (kg/m²):", min_value=0.0, max_value=80.0, step=0.1, key="h_bmi")
    dpf = st.number_input("Chỉ số tiền sử gia đình (DiabetesPedigree) — nếu không biết để 0.0:", min_value=0.0, max_value=5.0, step=0.001, key="h_dpf")
    age = st.number_input("Tuổi:", min_value=1, max_value=120, step=1, key="h_age")

    if st.button("Dự đoán (Bệnh viện)"):
        # tải dataset pima
        url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
        cols = ["Pregnancies","Glucose","BloodPressure","SkinThickness","Insulin","BMI","DiabetesPedigree","Age","Outcome"]
        try:
            df = pd.read_csv(url, header=None, names=cols)
        except Exception as e:
            st.error("Không thể tải dataset tham khảo (không có mạng?). Hiện không thể huấn luyện mô hình.")
            st.stop()

        # xử lý: thay 0 -> NaN cho cột liên quan và thay bằng median
        for c in ["Glucose","BloodPressure","SkinThickness","Insulin","BMI"]:
            df[c] = df[c].replace(0, np.nan)
            df[c] = df[c].fillna(df[c].median())

        X = df.drop(columns=["Outcome"])
        y = df["Outcome"]

        # huấn luyện mô hình logistic đơn giản
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.18, random_state=42)
        model = LogisticRegression(max_iter=1000, solver='liblinear')
        model.fit(X_train, y_train)

        # dự đoán trên input
        x_input = np.array([pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, dpf, age]).reshape(1, -1)
        proba = model.predict_proba(x_input)[0,1]
        pred = int(model.predict(x_input)[0])
        acc = accuracy_score(y_test, model.predict(X_test))

        st.markdown("### 🔬 Kết quả dự đoán (Mô hình học máy):")
        st.write(f"Độ chính xác mô hình (tham khảo trên tập test): **{acc*100:.1f}%**")
        st.progress(proba)
        st.success(f"Xác suất mắc đái tháo đường (ước tính): **{proba*100:.1f}%**")
        st.write(f"→ Dự đoán nhị phân mô hình: **{'CÓ' if pred==1 else 'KHÔNG'}**")

        if proba >= 0.7:
            st.error("🚨 Mô hình: Nguy cơ CAO — nên làm xét nghiệm HbA1c / tư vấn bác sĩ.")
        elif proba >= 0.4:
            st.warning("⚠ Mô hình: Nguy cơ trung bình — theo dõi và cải thiện lối sống.")
        else:
            st.info("✅ Mô hình: Nguy cơ thấp.")

# ========== hiển thị UI theo chế độ ==========
if mode == "Tại nhà (không cần máy)":
    home_mode_ui()
else:
    hospital_mode_ui()

st.markdown("---")
st.caption("Công cụ tham khảo — không thay thế chẩn đoán y khoa.")
