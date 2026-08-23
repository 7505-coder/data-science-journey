import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
import matplotlib.pyplot as plt
import seaborn as sns

# ---------- Page setup ----------
st.set_page_config(page_title="Heart Disease Predictor", layout="wide")
st.title("❤️ Heart Disease Risk Predictor")

# ---------- Folder this script lives in (works no matter what the working directory is) ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------- Load model, scaler, columns ----------
@st.cache_resource
def load_artifacts():
    with open(os.path.join(BASE_DIR, "model_svm.pkl"), "rb") as f:
        model = pickle.load(f)
    with open(os.path.join(BASE_DIR, "scaler.pkl"), "rb") as f:
        scaler = pickle.load(f)
    with open(os.path.join(BASE_DIR, "columns.pkl"), "rb") as f:
        columns = pickle.load(f)
    return model, scaler, columns

model, scaler, model_columns = load_artifacts()

# ---------- Tabs ----------
tab1, tab2 = st.tabs(["🩺 Predict", "📊 Dataset Insights"])

# ===================== TAB 1: PREDICTION FORM =====================
with tab1:
    st.subheader("Enter Patient Details")

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.number_input("Age", min_value=1, max_value=120, value=50)
        sex = st.selectbox("Sex", ["Male", "Female"])
        trestbps = st.number_input("Resting Blood Pressure (mm Hg)", min_value=60, max_value=250, value=120)

    with col2:
        chol = st.number_input("Cholesterol (mg/dl)", min_value=100, max_value=600, value=200)
        fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dl?", ["False", "True"])
        thalch = st.number_input("Max Heart Rate Achieved", min_value=60, max_value=220, value=150)

    with col3:
        exang = st.selectbox("Exercise-Induced Angina?", ["False", "True"])
        oldpeak = st.number_input("ST Depression (oldpeak)", min_value=0.0, max_value=10.0, value=1.0, step=0.1)

    cp = st.selectbox("Chest Pain Type", ["typical angina", "atypical angina", "non-anginal", "asymptomatic"])
    restecg = st.selectbox("Resting ECG Result", ["normal", "lv hypertrophy", "st-t abnormality"])

    if st.button("Predict", type="primary"):
        # Build a raw input row matching original (pre-encoding) feature names
        raw = {
            "age": age,
            "sex": 1 if sex == "Male" else 0,   # matches LabelEncoder's typical alphabetical mapping (Female=0, Male=1)
            "trestbps": trestbps,
            "chol": chol,
            "fbs": 1 if fbs == "True" else 0,
            "thalch": thalch,
            "exang": 1 if exang == "True" else 0,
            "oldpeak": oldpeak,
        }

        # One-hot encode cp and restecg manually, matching pd.get_dummies column names
        for col in model_columns:
            if col.startswith("cp_"):
                raw[col] = 1 if col == f"cp_{cp}" else 0
            elif col.startswith("restecg_"):
                raw[col] = 1 if col == f"restecg_{restecg}" else 0

        # Build a single-row dataframe in the exact column order the model expects
        input_df = pd.DataFrame([raw])
        input_df = input_df.reindex(columns=model_columns, fill_value=0)

        # Scale and predict
        input_scaled = scaler.transform(input_df)
        prediction = model.predict(input_scaled)[0]
        probability = model.predict_proba(input_scaled)[0][1]

        st.divider()
        if prediction == 1:
            st.error(f"⚠️ Higher risk of heart disease detected. (Probability: {probability:.1%})")
        else:
            st.success(f"✅ Lower risk of heart disease. (Probability: {probability:.1%})")

# ===================== TAB 2: DATASET INSIGHTS =====================
with tab2:
    st.subheader("Dataset Overview")
    st.caption("Upload your cleaned heart_disease CSV to explore it here.")

    uploaded_file = st.file_uploader("Upload cleaned dataset (CSV)", type=["csv"])

    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)

        st.write(f"**Rows:** {data.shape[0]} | **Columns:** {data.shape[1]}")
        st.dataframe(data.head())

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Target Distribution**")
            fig, ax = plt.subplots()
            if "num" in data.columns:
                sns.countplot(x="num", data=data, ax=ax)
            st.pyplot(fig)

        with col2:
            st.markdown("**Age Distribution**")
            fig2, ax2 = plt.subplots()
            if "age" in data.columns:
                sns.histplot(data["age"], kde=True, ax=ax2)
            st.pyplot(fig2)

        st.markdown("**Correlation Heatmap**")
        numeric_data = data.select_dtypes(include=[np.number])
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        sns.heatmap(numeric_data.corr(), annot=False, cmap="coolwarm", ax=ax3)
        st.pyplot(fig3)
    else:
        st.info("Upload a CSV above to see charts here.")
