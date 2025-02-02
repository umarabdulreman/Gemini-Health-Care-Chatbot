import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(
    page_title="HealthCare Chatbot",
    page_icon=":robot_face:",  # Set your desired favicon
    layout="wide",  # Choose layout style ('wide' or 'centered')
)

# Initialize Gemini-Pro 
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# Initialize the GenerativeModel instance
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    system_instruction="You are a healthcare advisor helping diabetic patients with their mental and physical health."
)

# Gemini uses 'model' for assistant; Streamlit uses 'assistant'
def role_to_streamlit(role):
    if role == "model":
        return "assistant"
    else:
        return role

# Add a Gemini Chat history object to Streamlit session state
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# Display Form Title
st.title("HealthCare Chatbot")

# Display chat messages from history above current input box
for message in st.session_state.chat.history:
    with st.chat_message(role_to_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Send user's message to Gemini and display response
if st.session_state.chat:
    prompt = st.chat_input("How may I help you today?")
    if prompt:
        # Display user's message
        st.chat_message("user").markdown(prompt)
        
        # Send user's entry to Gemini and get the response
        response = st.session_state.chat.send_message(prompt)
        
        # Display Gemini's response
        with st.chat_message("assistant"):
            st.markdown(response.text)

        # Optionally, rerun the script to keep the input at the bottom
        st.experimental_rerun()