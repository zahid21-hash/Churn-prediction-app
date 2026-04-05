import streamlit as st
import pandas as pd
import joblib

# ---------------- LOGIN SYSTEM ---------------- #

users = {
    "admin": {"password": "1234", "role": "admin"},
    "user": {"password": "abcd", "role": "user"}
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = None

def login():
    st.title("🔐 Login Page")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users and users[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.role = users[username]["role"]
            st.session_state.username = username
            st.success("Login Successful!")
        else:
            st.error("Invalid Credentials")

# ---------------- MAIN APP ---------------- #

def main_app():
    st.title("📊 Customer Churn Prediction")

    model = joblib.load("model.pkl")

    st.sidebar.header(f"Welcome {st.session_state.username}")

    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False

    # ---------------- USER INPUT ---------------- #
    st.sidebar.subheader("Enter Customer Data")

    tenure = st.sidebar.slider("Tenure", 0, 72, 12)
    monthly = st.sidebar.slider("Monthly Charges", 0, 200, 50)
    total = st.sidebar.slider("Total Charges", 0, 10000, 500)

    contract = st.sidebar.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
    internet = st.sidebar.selectbox("Internet", ["DSL", "Fiber optic", "No"])
    payment = st.sidebar.selectbox("Payment", [
        "Electronic check", "Mailed check",
        "Bank transfer (automatic)", "Credit card (automatic)"
    ])

    input_df = pd.DataFrame({
        "tenure": [tenure],
        "MonthlyCharges": [monthly],
        "TotalCharges": [total],
        "Contract": [contract],
        "InternetService": [internet],
        "PaymentMethod": [payment]
    })

    st.subheader("Input Data")
    st.write(input_df)

    # ---------------- PREDICTION ---------------- #
    if st.button("Predict"):
        pred = model.predict(input_df)[0]
        prob = model.predict_proba(input_df)[0][1]

        if pred == 1:
            st.error(f"⚠️ Customer likely to CHURN ({prob:.2f})")
        else:
            st.success(f"✅ Customer will STAY ({prob:.2f})")

    # ---------------- ADMIN PANEL ---------------- #
    if st.session_state.role == "admin":
        st.subheader("🛠 Admin Panel")

        df = pd.read_csv("dataset.csv")

        if st.button("View Dataset"):
            st.write(df.head())

        if st.button("Churn Distribution"):
            st.bar_chart(df["Churn"].value_counts())

# ---------------- ROUTING ---------------- #

if st.session_state.logged_in:
    main_app()
else:
    login()