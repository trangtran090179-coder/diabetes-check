# app.py
import streamlit as st
import base64
import numpy as np
import textwrap

# --------- cấu hình trang ----------
st.set_page_config(page_title="Diabetes Home Risk Checker", layout="wide")

# --------- đường dẫn ảnh nền (đặt file ảnh trong cùng thư mục) ----------
BACKGROUND_IMAGE_PATH = "castorice-honkai-7680x4320-22114.jpg"

# --------- helper: load ảnh -> base64 CSS ----------
def set_background(img_path):
    try:
        with open(img_path, "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
    except Exception as e:
        st.error("Không tìm thấy ảnh nền. Hãy đặt file ảnh đúng tên hoặc thay BACKGROUND_IMAGE_PATH.")
        return

    css = f"""
    <style>
    /* toàn trang nền */
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpg;base64,{b64}");
        background-size: cover;
        background-position: center center;
        background-attachment: fixed;
        animation: fadeIn 1s ease-in-out;
    }}

    /* top menu kiểu game landing */
    .topbar {{
        position: fixed;
        left: 0;
        right: 0;
        top: 0;
        z-index: 999;
        display:flex;
        justify-content:space-between;
        align-items:center;
        padding: 14px 36px;
        background: linear-gradient(90deg, rgba(0,0,0,0.30), rgba(0,0,0,0.12));
        backdrop-filter: blur(6px);
        border-bottom: 1px solid rgba(255,255,255,0.06);
    }}

    .logo {{
        font-weight:900;
        color: #ffffff;
        font-size:22px;
        letter-spacing:1px;
        text-shadow: 0 0 10px rgba(120,200,255,0.25);
    }}

    .menu a {{
        color: #ffffff;
        margin-left:18px;
        margin-right:6px;
        font-weight:700;
        text-decoration:none;
        cursor:pointer;
        transition: .18s;
        text-shadow: 0 0 6px rgba(120,200,255,0.18);
    }}

    .menu a:hover {{
        color: #cfeeff;
        transform: translateY(-2px);
        text-shadow: 0 0 14px rgba(170,220,255,0.28);
    }}

    /* hero box (giữ trong suốt) */
    .hero-box {{
        width: 100%;
        display:flex;
        justify-content:center;
        margin-top:86px;
        margin-bottom: 36px;
        padding: 40px 24px;
    }}

    .card {{
        max-width:1100px;
        width:100%;
        background: linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02));
        border-radius: 18px;
        padding: 48px;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 10px 40px rgba(10,20,40,0.25);
        backdrop-filter: blur(6px);
        color: #ffffff;
    }}

    .title {{
        font-size:46px;
        font-weight:900;
        color: #ffffff;
        margin-bottom: 8px;
        text-shadow: 0 4px 28px rgba(10,40,80,0.45);
    }}

    .subtitle {{
        color: rgba(235,245,255,0.88);
        margin-bottom: 22px;
        font-weight:600;
    }}

    /* thanh tìm/gõ giả */
    .fake-input {{
        width: 70%;
        height: 54px;
        margin: 14px auto 24px;
        border-radius: 999px;
        background: rgba(255,255,255,0.12);
        border: 1px solid rgba(255,255,255,0.08);
        display:flex;
        align-items:center;
        padding: 0 18px;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.03);
        color: #ffffff;
        font-weight:600;
        font-size:16px;
    }}

    /* nút chính */
    .start-btn { text-align:center; margin-top:6px; }
    .start-btn button {
        background: linear-gradient(90deg,#54e0ff,#7f6bff);
        color: #04121e;
        font-weight:800;
        padding: 14px 28px;
        border-radius: 12px;
        border: none;
        cursor:pointer;
        box-shadow: 0 8px 30px rgba(80,100,200,0.18);
        transition: transform .18s ease, box-shadow .18s ease;
    }
    .start-btn button:hover { transform: translateY(-3px); box-shadow: 0 14px 36px rgba(80,100,200,0.30); }

    /* glass form nhỏ cho nội dung trang con */
    .content-box {
        background: rgba(6,12,20,0.56);
        border-radius: 12px;
        padding: 20px;
        border: 1px solid rgba(255,255,255,0.06);
        color: #e9f5ff;
    }

    /* progress bar smoother */
    .stProgress > div > div { transition: width 1.2s ease-in-out !important; }

    @keyframes fadeIn {
        0% {opacity:0;}
        100% {opacity:1;}
    }
    </style>
    """

    st.markdown(css, unsafe_allow_html=True)

set_background(BACKGROUND_IMAGE_PATH)

# --------- top menu (reactive via session_state) ----------
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'

# topbar drawn by columns so we can use st.buttons to change state
top1, top2 = st.columns([1,3], gap="large")
with top1:
    st.markdown('<div class="topbar"><div class="logo">StellaSora Health</div><div style="width:8px"></div></div>', unsafe_allow_html=True)
with top2:
    # we draw menu inline using HTML anchors that call streamlit buttons is unreliable;
    # instead display transparent buttons laid over (using st.columns)
    cols = st.columns([1,1,1,1,6])
    with cols[0]:
        if st.button("HOME"):
            st.session_state['page'] = 'home'
    with cols[1]:
        if st.button("INFO"):
            st.session_state['page'] = 'info'
    with cols[2]:
        if st.button("CONTACT"):
            st.session_state['page'] = 'contact'
    with cols[3]:
        if st.button("BẮT ĐẦU DỰ ĐOÁN"):
            st.session_state['page'] = 'survey'

# spacer to avoid top overlap
st.write("") 
st.write("")

# --------- PAGE: HOME (hero) ----------
if st.session_state['page'] == 'home':
    st.markdown('<div class="hero-box"><div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="title">Dự đoán nguy cơ tiểu đường ngay tại nhà</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Hệ thống đánh giá nhanh các yếu tố nguy cơ — không cần xét nghiệm. Nhấn BẮT ĐẦU DỰ ĐOÁN để thực hiện.</div>', unsafe_allow_html=True)
    st.markdown('<div class="fake-input">🔎 Nhấn BẮT ĐẦU DỰ ĐOÁN để mở form — (dàn trang giống landing)</div>', unsafe_allow_html=True)
    st.markdown('<div class="start-btn"><button onclick="(function(){})()">BẮT ĐẦU DỰ ĐOÁN</button></div>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

# --------- PAGE: INFO ----------
elif st.session_state['page'] == 'info':
    st.markdown('<div class="hero-box"><div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="title">Thông tin về đái tháo đường</div>', unsafe_allow_html=True)
    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    st.markdown(textwrap.dedent("""
        - Đái tháo đường là tình trạng đường huyết cao do rối loạn sản xuất/hoạt động insulin.
        - Nếu kéo dài không kiểm soát gây tổn thương tim, thận, mắt, thần kinh.
        - Yếu tố nguy cơ: tuổi cao, thừa cân/đặc biệt vòng bụng lớn, ít vận động, ăn nhiều đồ ngọt.
        - Công cụ này chỉ ước lượng nguy cơ — KHÔNG THAY THẾ XÉT NGHIỆM Y TẾ.
    """), unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

# --------- PAGE: CONTACT ----------
elif st.session_state['page'] == 'contact':
    st.markdown('<div class="hero-box"><div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="title">Liên hệ hỗ trợ</div>', unsafe_allow_html=True)
    st.markdown('<div class="content-box">', unsafe_allow_html=True)
    st.markdown("""
        • Hotline: 1900-xxxxxx  
        • Email: support@example.com  
        • Ghi chú: Đây là dự án demo — không phải dịch vụ y tế.
    """, unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

# --------- PAGE: SURVEY (chứa cả 2 chế độ) ----------
elif st.session_state['page'] == 'survey':
    st.markdown('<div class="hero-box"><div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="title">DỰ ĐOÁN NGUY CƠ MẮC TIỂU ĐƯỜNG</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Chọn chế độ: <b>Tại nhà</b> (không cần máy) hoặc <b>Máy</b> (dùng dữ liệu y tế).</div>', unsafe_allow_html=True)

    mode = st.radio("Chọn chế độ", ["Tại nhà (rule)", "Máy (ml)"])

    # ---------- MODE: TẠI NHÀ (rule-based) ----------
    if mode == "Tại nhà (rule)":
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        age = st.number_input("Tuổi:", min_value=1, max_value=120, value=30)
        activity = st.selectbox("Bạn vận động mỗi ngày:", ["Ít hoặc không vận động","10–30 phút","30–60 phút","Trên 1 giờ"])
        sweet = st.selectbox("Uống đồ uống có đường:", ["Hầu như không","1–2 lần/tuần","3–6 lần/tuần","Mỗi ngày"])
        symptoms = st.multiselect("Bạn có triệu chứng nào:", ["Khát nước nhiều","Đi tiểu nhiều","Giảm cân nhanh","Mệt mỏi","Nhìn mờ"])
        belly = st.selectbox("Vòng bụng:", ["Bình thường","Hơi to","To rõ"])
        over_weight = st.selectbox("Bạn có dư cân?", ["Không","Có, hơi dư cân","Có, thừa cân rõ"])

        if st.button("Tính (Tại nhà)"):
            score = 0
            if age >= 45: score += 2
            if age >= 60: score += 3
            if activity == "Ít hoặc không vận động": score += 2
            elif activity == "10–30 phút": score += 1
            if sweet == "Mỗi ngày": score += 2
            elif sweet == "3–6 lần/tuần": score += 1
            score += len(symptoms)
            if belly == "Hơi to": score += 1
            elif belly == "To rõ": score += 2
            if over_weight == "Có, hơi dư cân": score += 1
            elif over_weight == "Có, thừa cân rõ": score += 2

            risk_pct = min(score * 6, 100)
            st.markdown("### Kết quả:")
            st.progress(risk_pct / 100)
            st.success(f"Nguy cơ ước tính: {risk_pct:.1f}%")
            if risk_pct >= 70:
                st.error("Nguy cơ CAO — nên khám và làm xét nghiệm.")
            elif risk_pct >= 40:
                st.warning("Nguy cơ trung bình — chú ý kiểm soát lối sống.")
            else:
                st.info("Nguy cơ thấp — duy trì thói quen tốt.")
        st.markdown('</div>', unsafe_allow_html=True)

    # ---------- MODE: MÁY (ml) ----------
    else:
        st.markdown('<div class="content-box">', unsafe_allow_html=True)
        st.write("Chế độ Máy: mô hình học máy sẽ sử dụng bộ dữ liệu tham khảo (Pima) để huấn luyện và dự đoán.")
        st.write("Lưu ý: cần có pandas, scikit-learn, numpy cài sẵn trong môi trường để chế độ này hoạt động.")
        # minimal numeric inputs that can be measured in bệnh viện but not necessarily at home:
        preg = st.number_input("Số lần mang thai (nếu không áp dụng, để 0):", min_value=0, value=0)
        glucose = st.number_input("Glucose (mg/dL):", min_value=20.0, value=100.0)
        bp = st.number_input("Huyết áp (mmHg):", min_value=20.0, value=70.0)
        skin = st.number_input("Độ dày da (mm) (nếu không có, để 0):", min_value=0.0, value=0.0)
        insulin = st.number_input("Insulin (mu U/ml) (nếu không có, để 0):", min_value=0.0, value=0.0)
        bmi = st.number_input("BMI (kg/m²):", min_value=10.0, value=25.0)
        pedigree = st.number_input("Chỉ số di truyền (0.0–2.5):", min_value=0.0, value=0.5)
        age2 = st.number_input("Tuổi:", min_value=1, value=30)

        if st.button("Tính (Máy)"):
            # try to import sklearn/pandas
            try:
                import pandas as pd
                import numpy as np
                from sklearn.model_selection import train_test_split
                from sklearn.linear_model import LogisticRegression
                from sklearn.metrics import accuracy_score
            except Exception as e:
                st.error("Chế độ Máy yêu cầu: pandas, scikit-learn, numpy. Hãy cài bằng: pip install pandas scikit-learn numpy")
                st.stop()

            # load dataset from internet (bỏ qua nếu không có)
            url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
            cols = ["Pregnancies","Glucose","BloodPressure","SkinThickness","Insulin","BMI","DiabetesPedigree","Age","Outcome"]
            try:
                df = pd.read_csv(url, header=None, names=cols)
            except Exception as e:
                st.error("Không thể tải dữ liệu Pima từ internet. Đặt file cục bộ hoặc đảm bảo có mạng.")
                st.stop()

            # preprocess
            for c in ["Glucose","BloodPressure","SkinThickness","Insulin","BMI"]:
                df[c] = df[c].replace(0, np.nan)
                df[c] = df[c].fillna(df[c].median())

            X = df.drop(columns=["Outcome"])
            y = df["Outcome"]

            # train
            model = LogisticRegression(max_iter=1000, solver='liblinear')
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            model.fit(X_train, y_train)
            acc = accuracy_score(y_test, model.predict(X_test))
            st.write(f"Độ chính xác mô hình (ước tính): {acc*100:.1f}%")

            # predict on user's input
            inp = [preg, glucose, bp, skin, insulin, bmi, pedigree, age2]
            proba = model.predict_proba([inp])[0,1]
            pred = model.predict([inp])[0]
            st.progress(proba)
            st.success(f"Xác suất theo mô hình: {proba*100:.1f}% → Dự đoán: {'CÓ' if pred==1 else 'KHÔNG'}")
            if proba >= 0.7:
                st.error("🚨 Nguy cơ cao theo mô hình — xin kiểm tra y tế.")
            elif proba >= 0.4:
                st.warning("⚠ Nguy cơ trung bình — theo dõi và kiểm tra.")
            else:
                st.info("✅ Nguy cơ thấp (mô hình).")

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div></div>', unsafe_allow_html=True)

# footer
st.markdown("<br><center><small style='color:rgba(255,255,255,0.8)'>© StellaSora Health — Tham khảo, không thay thế bác sĩ.</small></center>", unsafe_allow_html=True)
