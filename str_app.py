import streamlit as st
from pathlib import Path
from dotenv import load_dotenv

from app.agent_factory import create_csv_agent

# -----------------------------
# Load environment
# -----------------------------
load_dotenv()

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="CSV AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 CSV AI Chatbot")
st.caption("Upload any CSV and chat with your data")

# -----------------------------
# Storage
# -----------------------------
UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------
# Session State
# -----------------------------
if "agent" not in st.session_state:
    st.session_state.agent = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Sidebar (Upload)
# -----------------------------
with st.sidebar:
    st.header("📂 Upload CSV")
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"]
    )

    if uploaded_file:
        csv_path = UPLOAD_DIR / uploaded_file.name
        csv_path.write_bytes(uploaded_file.getbuffer())

        st.success("CSV uploaded successfully!")

        st.session_state.agent = create_csv_agent(csv_path)
        st.session_state.messages = []

# -----------------------------
# Chat history
# -----------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -----------------------------
# Chat input
# -----------------------------
if st.session_state.agent:
    user_prompt = st.chat_input("Ask a question about the CSV")

    if user_prompt:
        # Store user message
        st.session_state.messages.append(
            {"role": "user", "content": user_prompt}
        )

        # Display user message
        with st.chat_message("user"):
            st.markdown(user_prompt)

        # Assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.agent.run(user_prompt)
                st.markdown(response.content)

        # Store assistant message
        st.session_state.messages.append(
            {"role": "assistant", "content": response.content}
        )
else:
    st.info("👈 Upload a CSV file from the sidebar to start chatting.")
