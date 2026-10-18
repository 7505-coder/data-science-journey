import streamlit as st
import pandas as pd
from tensorflow import keras

st.set_page_config(page_title="Fraud Detector", page_icon="💳")

@st.cache_resource
def load_model():
    return keras.models.load_model('fraud_model.keras')

@st.cache_data
def load_data():
    return pd.read_csv('demo_data.csv')

model = load_model()
data = load_data()

st.title("💳 Credit Card Fraud Detector")
st.write("ANN trained on 284,807 transactions. Only 0.17% are fraud.")

choice = st.radio("Pick a transaction", ["Random", "Random fraud", "Random normal"], horizontal=True)

if st.button("Check transaction"):
    if choice == "Random fraud":
        row = data[data['Class'] == 1].sample(1)
    elif choice == "Random normal":
        row = data[data['Class'] == 0].sample(1)
    else:
        row = data.sample(1)

    X = row.drop(columns='Class')
    prob = float(model.predict(X, verbose=0)[0][0])
    actual = "Fraud" if int(row['Class'].iloc[0]) == 1 else "Normal"

    st.dataframe(X[['Time', 'Amount', 'V1', 'V2', 'V3']])
    st.metric("Fraud probability", f"{prob:.2%}")

    if prob > 0.5:
        st.error("🚨 Predicted: FRAUD")
    else:
        st.success("✅ Predicted: NORMAL")
    st.write(f"Actual label: **{actual}**")