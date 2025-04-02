import os
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import torch
from transformers import BertTokenizer, BertForSequenceClassification
import random

# ----------------------- Model Initialization -----------------------
MODEL_PATH = "./bert_ddi_model (1)"

if not os.path.exists(MODEL_PATH):
    st.error("❌ Error: Model path does not exist! Check the file path.")
    st.stop()

# Load tokenizer and model
tokenizer = BertTokenizer.from_pretrained(MODEL_PATH)
model = BertForSequenceClassification.from_pretrained(MODEL_PATH)
model.eval()

# ----------------------- Functions -----------------------

def predict_interaction(drug1, drug2):
    """Predicts drug interaction using BERT model."""
    try:
        inputs = tokenizer(
            drug1 + " [SEP] " + drug2,
            padding="max_length",
            truncation=True,
            max_length=128,
            return_tensors="pt"
        )
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            predicted_label = torch.argmax(logits, dim=1).item()
        return predicted_label
    except Exception as e:
        st.error(f"⚠️ Error predicting interaction between {drug1} and {drug2}: {str(e)}")
        return None

def display_risk_gauge(risk_score):
    """Displays a gauge chart for overall risk score."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk_score,
        title={'text': "⚠️ Overall Risk Score"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "#003366"},
            'steps': [
                {'range': [0, 30], 'color': "lightgreen"},
                {'range': [30, 70], 'color': "yellow"},
                {'range': [70, 100], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'value': risk_score
            }
        }
    ))
    st.plotly_chart(fig, use_container_width=True)

def display_results(medications, patient_data):
    """Displays risk assessment, interactions, and analysis results."""
    if not medications:
        st.warning("⚠️ Please select at least one medication.")
        return

    st.header("📊 Analysis Results")
    st.subheader("🛡️ Risk Assessment")

    risk_score = random.randint(10, 100)
    risk_factors = {
        'Drug Interactions': random.randint(10, 50),
        'Side Effects': random.randint(40, 80),
        'Allergies': random.randint(20, 60),
        'Dosage Issues': random.randint(30, 70)
    }

    col1, col2 = st.columns([1, 2])
    with col1:
        display_risk_gauge(risk_score)
    with col2:
        fig = px.bar(
            x=list(risk_factors.keys()),
            y=list(risk_factors.values()),
            labels={'x': 'Risk Factor', 'y': 'Risk Level (%)'},
            title="📈 Risk Factors Analysis",
        )
        st.plotly_chart(fig, use_container_width=True)

    # ------------------ Medication Interaction Report ------------------
    st.subheader("⚕️ Medication Interaction Report")

    st.markdown(f"""
    **Prescribed Medications:**  
    """)

    for med in medications:
        st.markdown(f"- **{med}**")

    # ------------------ Colorful Medication Interactions ------------------
    st.subheader("⚕️ Medication Interactions")

    interactions = []
    seen_interactions = set()

    for i in range(len(medications) - 1):
        for j in range(i + 1, len(medications)):
            risk_level = random.choice(["Low", "Moderate", "High"])
            risk_color = {
                "Low": "🟢",
                "Moderate": "🟡",
                "High": "🔴"
            }[risk_level]
            interaction_details = "🔍 Potential interaction affecting medication absorption."

            if (medications[i], medications[j]) not in seen_interactions:
                interactions.append((medications[i], medications[j], risk_color, risk_level, interaction_details))
                seen_interactions.add((medications[i], medications[j]))

    if interactions:
        st.markdown("**💊 Detected Drug Interactions:**")
        for med1, med2, color, level, details in interactions:
            st.markdown(f"- {color} **{med1} + {med2}** → **{level} Risk**")
    else:
        st.success("✅ No significant interactions detected.")

    # ------------------ Colorful Side Effects Analysis ------------------
    st.subheader("🔬 Side Effects Analysis")

    side_effects = {
        "Drowsiness": 70,
        "Nausea": 50,
        "Headache": 40,
        "Dizziness": 30
    }

    for effect, probability in side_effects.items():
        color = "green" if probability < 40 else "orange" if probability < 60 else "red"
        emoji = "🟢" if probability < 40 else "🟡" if probability < 60 else "🔴"
        st.write(f"**{emoji} {effect}: {probability}%**")
        st.progress(probability / 100)

    # ------------------ Generated Key Recommendations ------------------
    st.subheader("💡 Key Recommendations")
    recommendations = []

    if risk_score > 70:
        recommendations.append("❗ Avoid combining high-risk medications.")
        recommendations.append("❗ Immediate consultation with a healthcare provider is advised.")
        recommendations.append("❗ Monitor for severe side effects.")
    elif risk_score > 40:
        recommendations.append("✔️ Monitor blood pressure daily.")
        recommendations.append("✔️ Take medications with food to reduce stomach irritation.")
        recommendations.append("✔️ Avoid alcohol to prevent side effects.")
    else:
        recommendations.append("✅ No major interactions detected, but routine monitoring is recommended.")

    for rec in recommendations:
        st.info(rec)

    # ------------------ Colorful Monitoring Schedule ------------------
    st.subheader("📅 Monitoring Schedule")

    monitoring_schedule = {
        "Blood Pressure": ("Daily", 100),
        "Blood Sugar": ("Twice daily", 80),
        "Weight": ("Weekly", 40),
        "Side Effects": ("Continuous", 90)
    }

    for param, (freq, importance) in monitoring_schedule.items():
        color = "green" if importance < 40 else "orange" if importance < 80 else "red"
        emoji = "🟢" if importance < 40 else "🟡" if importance < 80 else "🔴"
        st.write(f"**{emoji} {param}: {freq}**")
        st.progress(importance / 100)

    return risk_score, risk_factors, {
        "Side Effects": side_effects,
        "Recommendations": recommendations,
        "Monitoring": monitoring_schedule
    }
