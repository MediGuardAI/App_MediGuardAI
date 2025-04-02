import streamlit as st
from chat_interface import display_chat_interface

def create_sidebar():
    with st.sidebar:
        st.header("Patient Information")
        patient_name = st.text_input("Patient Name")
        patient_age = st.number_input("Age", min_value=0, max_value=120, value=30)
        patient_gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        patient_weight = st.number_input("Weight (kg)", min_value=0, max_value=300, value=70)

        medical_conditions = st.multiselect(
            "Existing Medical Conditions",
            ["Diabetes", "Hypertension", "Asthma", "Heart Disease", "Kidney Disease", "Cancer",],
        )

        # Divider for separation
        st.divider()

        # Chat Assistant after Patient Info
        st.header("💬 MediGuardAI Chat Assistant")
        display_chat_interface()

        return {
            "name": patient_name,
            "age": patient_age,
            "gender": patient_gender,
            "weight": patient_weight,
            "conditions": medical_conditions
        }
