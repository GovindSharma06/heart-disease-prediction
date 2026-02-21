import streamlit as st
import requests

API_URL = "https://heart-disease-prediction-afjb.onrender.com/predict"

st.set_page_config(
    page_title="Heart Disease Prediction",
    page_icon="❤️",
    layout="centered"
)

# ---------------- HEADER ----------------
st.title("❤️ Heart Disease Prediction")
st.caption("ML-powered risk estimation using clinical patient data (Random Forest Model).")

st.markdown("---")

# ---------------- SIDEBAR INFO ----------------
with st.sidebar:
    st.header("ℹ️ About this App")
    st.write("""
This app predicts the probability of heart disease using a trained Machine Learning model.

**Model used:** Tuned Random Forest  
**Metric:** ROC-AUC ≈ 0.93 (cross-validated)
""")

    st.markdown("---")
    st.subheader("⚠️ Disclaimer")
    st.write("""
This tool is for learning and demo purposes only.
It is **NOT** a medical diagnosis.
Always consult a doctor.
""")

# ---------------- INPUT FORM ----------------
st.subheader("🧾 Enter Patient Details")

with st.form("patient_form"):

    col1, col2 = st.columns(2)

    with col1:
        Age = st.number_input("Age", min_value=1, max_value=120, value=40)
        Sex = st.selectbox("Sex", ["M", "F"])
        ChestPainType = st.selectbox("Chest Pain Type", ["ASY", "ATA", "NAP", "TA"])
        RestingBP = st.number_input("Resting Blood Pressure (mm Hg)", min_value=0, max_value=250, value=140)
        Cholesterol = st.number_input("Cholesterol (mg/dl)", min_value=0, max_value=700, value=200)
        FastingBS = st.selectbox("Fasting Blood Sugar > 120 mg/dl", [0, 1])

    with col2:
        RestingECG = st.selectbox("Resting ECG", ["Normal", "ST", "LVH"])
        MaxHR = st.number_input("Max Heart Rate", min_value=50, max_value=250, value=150)
        ExerciseAngina = st.selectbox("Exercise Induced Angina", ["N", "Y"])
        Oldpeak = st.number_input("Oldpeak (ST Depression)", min_value=-5.0, max_value=10.0, value=1.0)
        ST_Slope = st.selectbox("ST Slope", ["Up", "Flat", "Down"])

        st.write("")  # spacing
        submitted = st.form_submit_button("🔍 Predict Risk")

# ---------------- PREDICTION ----------------
if submitted:

    payload = {
        "Age": int(Age),
        "Sex": Sex,
        "ChestPainType": ChestPainType,
        "RestingBP": int(RestingBP),
        "Cholesterol": int(Cholesterol),
        "FastingBS": int(FastingBS),
        "RestingECG": RestingECG,
        "MaxHR": int(MaxHR),
        "ExerciseAngina": ExerciseAngina,
        "Oldpeak": float(Oldpeak),
        "ST_Slope": ST_Slope
    }

    with st.spinner("Running prediction..."):
        try:
            res = requests.post(API_URL, json=payload)

            if res.status_code != 200:
                st.error(f"API Error: {res.status_code}")
                st.write(res.text)
                st.stop()

            data = res.json()

        except Exception as e:
            st.error("Could not connect to FastAPI backend.")
            st.write(e)
            st.stop()

    pred = data["prediction"]
    prob = data["risk_probability"]

    st.markdown("---")
    st.subheader("📌 Prediction Result")

    # Risk category
    if prob < 0.35:
        risk_label = "LOW RISK"
        risk_emoji = "🟢"
    elif prob < 0.70:
        risk_label = "MEDIUM RISK"
        risk_emoji = "🟡"
    else:
        risk_label = "HIGH RISK"
        risk_emoji = "🔴"

    # Main result display
    if pred == 1:
        st.error(f"{risk_emoji} **Heart Disease Detected**")
    else:
        st.success(f"{risk_emoji} **No Heart Disease Detected**")

    st.metric("Risk Probability", f"{prob*100:.2f}%")
    st.progress(min(max(prob, 0.0), 1.0))

    st.caption(f"Risk Category: **{risk_label}**")

    # Show user inputs nicely
    with st.expander("📄 View Submitted Patient Data"):
        st.json(payload)

# ---------------- MODEL EXPLANATION SECTION ----------------
st.markdown("---")
st.subheader("🧠 Model Explanation (How it predicts)")

st.write("""
This model was trained on the **Heart Disease dataset** (918 records).  
It uses a **Random Forest Classifier**, which works like this:

### 🌳 Random Forest in simple words
A Random Forest is a collection of many Decision Trees.

Each tree asks questions like:
- Is the chest pain type ASY?
- Is ST_Slope Flat or Down?
- Is Oldpeak high?
- Is MaxHR low?

Then all trees vote, and the final output is decided.
""")

st.write("""
### ⭐ Most important features (from EDA)
These features were the strongest predictors in your dataset:

- **ST_Slope** → Flat/Down increases risk strongly  
- **ExerciseAngina** → "Y" is highly linked to heart disease  
- **ChestPainType** → ASY had ~79% disease rate  
- **Oldpeak** → higher values increase risk  
- **MaxHR** → lower values increase risk  
""")

st.write("""
### ⚠️ Important note about Cholesterol
In the dataset, many records had cholesterol stored as **0**, which is not medically possible.
So during training we used a special feature:

**Cholesterol_missing = 1 if Cholesterol was 0**

This helps the model learn correctly without using fake values.
""")

st.info("This project is meant for learning ML deployment. For real health decisions, consult a medical professional.")
