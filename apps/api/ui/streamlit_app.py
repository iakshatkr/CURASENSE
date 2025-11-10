import streamlit as st

st.set_page_config(page_title="CURASENSE", page_icon="⚕️" , layout ="wide")

st.title("⚕️ CURASENSE - AI Symptom Screener & Triage Assistant")
st.caption("Empowering Healthcare with AI-Driven Symptom Analysis and Triage Recommendations")
st.caption("Educational tool, not a diagnosis. If you feel very unwell, seek immediate medical attention.")

with st.container():
    st.header("Describe your symptoms")
    symptoms = st.text_area("Type your symptoms here:", placeholder="e.g., fever, sore throat, fatigue since 3 days")

    age = st.selectbox("Age Range", ["<18", "18-40", "40-60", "60+"])
    sex = st.radio("Gender", ["Male", "Female", "Other"])
    chronic = st.multiselect("Chronic Conditions", ["Diabetes", "Hypertension", "Asthma", "None"])

    if st.button("Analyze My Symptoms"):
        st.write("⚙️ Processing...")
        # Later: call FastAPI endpoint here

st.divider()
st.write("© 2025 CURASENSE | Educational use only.") 