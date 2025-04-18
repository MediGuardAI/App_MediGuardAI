# MediGuard AI – An Interactive Drug Interaction and Side Effect Predictor using LLMs with RAG-based Chat Assistance

## 🚀 Features
- **Drug Interaction Prediction**: Uses LLaMA models to analyze potential interactions between drugs.
- **Side Effect Analysis**: Identifies possible adverse effects based on drug combinations.
- **Intuitive UI**: Built using Streamlit for a seamless user experience.
- **Visualization Tools**: Uses Matplotlib and Plotly for interactive data representation.

## 📌 Prerequisites
Before installing MediGuard AI, ensure your system meets the following requirements:

- Python **3.7 or higher**
- An active internet connection (for package installations)
- Git installed (for cloning the repository)

## 🛠️ Installation Guide
Follow these steps to set up MediGuard AI on your local machine.

### 1️⃣ Clone the Repository
```bash
 git clone https://github.com/MediGuardAI/App_MediGuardAI.git
 cd App_MediGuardAI
```

### 2️⃣ Set Up a Virtual Environment
To avoid conflicts with system-wide dependencies, it’s recommended to use a virtual environment.
```bash
python -m venv venv
```
#### Activate the Virtual Environment
- **Windows**:
  ```bash
  venv\Scripts\activate
  ```
- **MacOS/Linux**:
  ```bash
  source venv/bin/activate
  ```

### 3️⃣ Upgrade Pip
Ensure you have the latest version of pip before proceeding.
```bash
python -m pip install --upgrade pip
```

### 4️⃣ Install Required Dependencies
Install the necessary Python libraries using the following command:
```bash
pip install -r requirements.txt
```
> If `requirements.txt` is not available, install manually:
```bash
pip install streamlit pandas plotly reportlab torch torchvision torchaudio transformers matplotlib
```

### 5️⃣ Run the Application
After successful installation, start MediGuard AI using:
```bash
streamlit run main.py
```
This will launch the app in your default web browser.

## 🏆 Contribution Guidelines
We welcome contributions from the community! If you'd like to contribute:
1. Fork the repository
2. Create a new branch (`feature-branch`)
3. Make your changes
4. Submit a pull request
---
⭐ **If you like this project, give it a star!** ⭐
