import streamlit as st
import requests
import logging

# Set API Token & Model
HUGGINGFACE_API_TOKEN = "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"  # Replace with your actual token
MODEL_ID = "tiiuae/falcon-7b-instruct"

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def query_huggingface_api(history, new_prompt):
    """Queries Hugging Face API while maintaining chat history for context."""
    API_URL = f"https://api-inference.huggingface.co/models/{MODEL_ID}"
    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}",
        "Content-Type": "application/json"
    }

    system_prompt = "You are a medical assistant. Answer concisely and provide only one response per question."

    # Combine chat history with new prompt
    context = "\n".join(history) + f"\n {new_prompt}\nAssistant:"

    payload = {
        "inputs": f"{system_prompt}\n{context}",
        "parameters": {
            "max_length": 200,
            "temperature": 0.7,
            "top_p": 0.85,
            "do_sample": True,
            "num_return_sequences": 1,
            "stop": ["\n\n", "User:"],  # Prevents multiple responses
        }
    }

    try:
        logger.debug(f"Sending request to {MODEL_ID} with prompt: {new_prompt}")
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()

        # Extract response correctly
        if isinstance(result, list) and len(result) > 0 and "generated_text" in result[0]:
            response_text = result[0]["generated_text"].strip()
            return response_text.split("\nAssistant:")[-1]  # Only return assistant's response
        else:
            return "I'm sorry, but I couldn't generate a proper response. Please try again."

    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}")
        return "⚠️ Unable to connect to the AI service. Please check your internet connection."

def display_chat_interface():
    """Displays the chatbot interface with optimized responses."""
    
    st.markdown("## 🏥 MediGuardAI - Your Medical Assistant")
    st.write("Ask any medical-related questions, and I'll provide clear, direct answers.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous messages
    for message in st.session_state.messages:
        role = "👤" if message["role"] == "user" else "🤖"
        st.write(f"{role} {message['content']}")

    # User input
    if user_input := st.chat_input("Ask your medical question..."):
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.spinner("Thinking..."):
            chat_history = [msg["content"] for msg in st.session_state.messages[-3:]]  # Keep only last 3 messages
            response = query_huggingface_api(chat_history, user_input)
            st.session_state.messages.append({"role": "assistant", "content": response})

        st.rerun()

    # Clear chat history button
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

if __name__ == "__main__":
    display_chat_interface()
