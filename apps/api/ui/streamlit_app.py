import streamlit as st
import requests
import time
import streamlit.components.v1 as components

# ------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------
st.set_page_config(page_title="CURASENSE", page_icon="⚕️", layout="wide")

# ------------------------------------------------------------
# CUSTOM CSS
# ------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

body, [class*="stAppViewContainer"] {
    background: linear-gradient(160deg, #0E1614 0%, #060A0A 100%) !important;
    color: #ECFDF5 !important;
    font-family: 'Inter', sans-serif !important;
}

h1 {
    color: #7FFFD4 !important;
    font-weight: 700;
    text-align: center;
    animation: fadeIn 1s ease-out;
}

@keyframes fadeIn {
    0% {opacity:0; transform: translateY(10px);}
    100% {opacity:1; transform: translateY(0);}
}

div[data-testid="stVerticalBlock"] {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(127,255,212,0.12);
    border-radius: 18px;
    backdrop-filter: blur(14px);
    padding: 28px;
    box-shadow: 0 4px 25px rgba(0,0,0,0.35);
}

textarea, input, select {
    background: rgba(255,255,255,0.04) !important;
    border-radius: 10px !important;
    color: #EAFBF5 !important;
    border: 1px solid rgba(127,255,212,0.13) !important;
}

div.stButton > button {
    background: linear-gradient(135deg, #7FFFD4 0%, #4FE3C1 100%);
    border: none;
    border-radius: 12px;
    font-weight: 600;
    color: #00150F;
    padding: 0.75em 1.6em;
    font-size: 1.05em;
    box-shadow: 0 0 14px rgba(127,255,212,0.25);
}
div.stButton > button:hover {
    transform: scale(1.03);
    box-shadow: 0 0 22px rgba(127,255,212,0.45);
}

footer{visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# TITLE
# ------------------------------------------------------------
placeholder = st.empty()
time.sleep(0.4)
placeholder.title("⚕️ CURASENSE — AI Symptom Screener & Triage Assistant")
st.caption("Empowering Healthcare with AI-Driven Symptom Analysis and Triage Recommendations")
st.caption("Educational tool, not a diagnosis. If severely unwell, seek immediate medical attention.")
st.write("---")

# ------------------------------------------------------------
# INPUT UI
# ------------------------------------------------------------
with st.container():
    st.header("Describe your symptoms :")

    symptoms = st.text_area("Type your symptoms here:", placeholder="e.g., fever, headache, nausea")
    age = st.selectbox("Age Range", ["<18", "18-40", "40-60", "60+"])
    sex = st.radio("Gender", ["Male", "Female", "Other"], horizontal=True)
    chronic = st.multiselect("Chronic Conditions", ["Diabetes", "Hypertension", "Asthma", "None"])

    if st.button("Analyze My Symptoms"):
        if not symptoms.strip():
            st.warning("Please enter your symptoms before analyzing.")
            st.stop()

        with st.spinner("⚙️ Analyzing your symptoms..."):
            try:
                payload = {
                    "text": symptoms,
                    "age_range": age,
                    "sex": sex,
                    "chronic_conditions": chronic
                }
                response = requests.post("http://127.0.0.1:8000/api/v1/triage", json=payload)
                data = response.json()

            except Exception as e:
                st.error(f"API error: {e}")
                st.stop()

        # ------------------------------------------------------------
        # EMERGENCY RED FLAG SECTION
        # ------------------------------------------------------------
        if data.get("urgency") == "emergency":
            components.html("""
<div style="
    padding:20px;
    border-radius:12px;
    background:rgba(255,0,0,0.2);
    border:1px solid rgba(255,80,80,0.5);
    color:#ffb3b3;
    font-weight:600;
    font-size:18px;
">
🚨 <strong>RED FLAG DETECTED — IMMEDIATE ACTION REQUIRED</strong><br><br>
Your symptoms match emergency medical indicators.
</div>
""", height=150)

            st.subheader("❗ Critical Findings")
            for flag in data["red_flags"]:
                st.write(f"• **{flag['reason']}** — triggered by: `{flag['phrase']}`")

            st.stop()

        # ------------------------------------------------------------
        # SEVERITY BADGES — FIXED (SPAN ONLY)
        # ------------------------------------------------------------
        high_severity_badge = """
<span style="
    display:inline-flex;
    align-items:center;
    background: rgba(255,0,0,0.25);
    padding:6px 12px;
    border-radius:8px;
    color:#ff9090;
    font-weight:600;
    border:1px solid rgba(255,90,90,0.5);
">🔴 HIGH SEVERITY</span>
"""

        moderate_severity_badge = """
<span style="
    display:inline-flex;
    align-items:center;
    background: rgba(255,165,0,0.18);
    padding:6px 12px;
    border-radius:8px;
    color:#ffcc80;
    font-weight:600;
    border:1px solid rgba(255,180,80,0.4);
">🟠 MODERATE SEVERITY</span>
"""

        low_severity_badge = """
<span style="
    display:inline-flex;
    align-items:center;
    background: rgba(127,255,212,0.12);
    padding:6px 12px;
    border-radius:8px;
    color:#7FFFD4;
    font-weight:600;
    border:1px solid rgba(127,255,212,0.3);
">🟢 LOW SEVERITY</span>
"""

        # ------------------------------------------------------------
        # POSSIBLE CONDITIONS
        # ------------------------------------------------------------
        st.markdown("## 🧠 AI Analysis —  Possible Conditions")

        for c in data["conditions"]:
            pct = int(c["final_score"] * 100)

            # Pick badge
            if pct >= 80:
                badge = high_severity_badge
            elif pct >= 50:
                badge = moderate_severity_badge
            else:
                badge = low_severity_badge

            # CONDITION TITLE BLOCK (NOW FIXED)
            components.html(f"""
<div style='margin-bottom:8px;'>
    <h3 style="color:#7FFFD4; margin-bottom:4px;">🔹 {c['name']}</h3>
    {badge}
</div>
""", height=80)

            # Confidence
            st.write("**Confidence Level:**")
            st.progress(pct)
            st.write(f"**Final Score:** {pct}%")

            # Rationale
            st.markdown(f"**Why this condition appears:** {c['rationale']}")

            st.markdown("---")

        # ------------------------------------------------------------
        # URGENCY BADGE (GLOBAL)
        # ------------------------------------------------------------
        urgency = data["urgency"].upper()

        if urgency == "EMERGENCY":
            color = "#ff8080"
            bg = "rgba(255,0,0,0.25)"
            icon = "🚨"
        elif urgency == "URGENT":
            color = "#ffcc80"
            bg = "rgba(255,165,0,0.15)"
            icon = "⚠️"
        else:
            color = "#7FFFD4"
            bg = "rgba(127,255,212,0.12)"
            icon = "🩺"

        components.html(f"""
<div style="
    margin-top:20px;
    padding:14px;
    border-radius:10px;
    background:{bg};
    border-left:6px solid {color};
    color:{color};
    font-weight:600;
    font-size:17px;
">
{icon} URGENCY LEVEL: {urgency}
</div>
""", height=80)

        # ------------------------------------------------------------
        # ADVICE SECTION
        # ------------------------------------------------------------
        st.markdown("## 📌 Medical Advice")

        advice = data["advice"]

        st.subheader("🩺 Self-care Suggestions")
        for tip in advice.get("selfcare", []):
            st.write(f"- {tip}")

        st.subheader("⚠️ When to Seek Help")
        for tip in advice.get("escalate_when", []):
            st.write(f"- {tip}")

# ------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------
st.write("---")
st.write("<p style='text-align:center;color:#A6FFCE;'>© 2025 <b>CURASENSE</b> | Educational use only.</p>", unsafe_allow_html=True)
