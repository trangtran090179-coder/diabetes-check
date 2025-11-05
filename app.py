import streamlit as st
import numpy as np

st.set_page_config(page_title="Dự đoán đái tháo đường", page_icon="")

st.title(" HỆ THỐNG DỰ ĐOÁN NGUY CƠ ĐÁI THÁO ĐƯỜNG")
st.write("Nhập thông tin bên dưới để dự đoán:")

preg = st.number_input("Số lần mang thai (nữ, không áp dụng thì để 0)", min_value=0)
glucose = st.number_input("Glucose lúc đói (mg/dL)", min_value=0)
bp = st.number_input("Huyết áp tâm trương (mmHg)", min_value=0)
bmi = st.number_input("BMI", min_value=0.0, format="%.1f")
age = st.number_input("Tuổi", min_value=1)

if st.button("Dự đoán"):
    score = 0
    if glucose >= 126: score += 2
    if bmi >= 25: score += 1
    if bp >= 85: score += 1
    if age >= 45: score += 1
    if preg >= 3: score += 1

    st.subheader("Kết quả:")

    if score >= 3:
        st.error("⚠ Nguy cơ **CAO** – Có thể bị đái tháo đường. Nên xét nghiệm HbA1c hoặc đến bệnh viện.")
    elif score == 2:
        st.warning("⚠ Nguy cơ **TRUNG BÌNH** – Nên kiểm tra định kỳ hoặc tự đo tại nhà.")
    else:
        st.success("✅ Nguy cơ **THẤP** – Sức khỏe ổn, nhưng vẫn nên theo dõi đường huyết.")

st.info(" Đây chỉ là hệ thống gợi ý, không thay thế chuẩn đoán y khoa.")
