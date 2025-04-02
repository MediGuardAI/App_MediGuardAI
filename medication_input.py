# import streamlit as st

# def create_medication_input():
#     st.header("Medication Information")
#     cols = st.columns(2)

#     with cols[0]:
#         drug_database = [
#             "Aspirin", "Ibuprofen", "Paracetamol", "Amoxicillin",
#             "Lisinopril", "Metformin", "Omeprazole", "Simvastatin"
#         ]
#         selected_medications = st.multiselect(
#             "Select Current Medications", drug_database, key="medication_select"
#         )

#     with cols[1]:
#         dosages = {}
#         for med in selected_medications:
#             dosages[med] = st.number_input(
#                 f"Dosage for {med} (mg)", min_value=0, max_value=1000, value=100, key=f"dosage_{med}"
#             )


#     return selected_medications, dosages


import streamlit as st
import pandas as pd

def load_medications(file_path):
    df = pd.read_csv(file_path)
    drug_names = set(df['drug1_name']).union(set(df['drug2_name']))
    return sorted(drug_names)

def create_medication_input():
    st.header("Medication Information")
    cols = st.columns(2)
    
    # Load medication names from dataset
    file_path = r"./dataset/DDI_data.csv"  # Ensure this file is available
    drug_database = load_medications(file_path)

    with cols[0]:
        selected_medications = st.multiselect(
            "Select Current Medications", drug_database, key="medication_select"
        )
    
    with cols[1]:
        dosages = {}
        for med in selected_medications:
            dosages[med] = st.number_input(
                f"Dosage for {med} (mg)", min_value=0, max_value=1000, value=100, key=f"dosage_{med}"
            )

    return selected_medications, dosages

# Example usage
if __name__ == "__main__":
    create_medication_input()