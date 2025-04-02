import streamlit as st
from sidebar import create_sidebar
from medication_input import create_medication_input
from risk_analysis import display_results
from chat_interface import display_chat_interface
from export import export_to_pdf
import asyncio

try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

st.set_page_config(page_title="MediGuardAI Assistant", page_icon="🏥", layout="wide")

def main():
    st.title("🏥 MediGuard AI - Drug Interaction Analyzer")

    # Sidebar Inputs
    st.sidebar.header("📋 Patient Information")
    patient_data = create_sidebar()

    # st.sidebar.header("💊 Medication Details")
    medications, dosages = create_medication_input()

    with st.container():
        st.subheader("🔎 Drug Interaction Analysis")

        if st.button("Analyze Interactions", type="primary"):
            risk_score, risk_factors, detailed_analysis = display_results(medications, patient_data)

            if medications:
                pdf_bytes = export_to_pdf(medications, dosages, patient_data, risk_factors, detailed_analysis)
                st.download_button(
                    label="📄 Export Report (PDF)",
                    data=pdf_bytes,
                    file_name="drug_interaction_report.pdf",
                    mime="application/pdf"
                )

if __name__ == "__main__":
    main()
