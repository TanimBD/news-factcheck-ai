import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st

from backend.agent.factcheck_agent import factcheck_claim
from backend.tools.ocr_tool import extract_text_from_image

st.set_page_config(page_title="News FactCheck AI", page_icon="📰")

st.title("📰 News FactCheck AI")

# ---------------------------
# Button Styling
# ---------------------------
st.markdown(
    """
    <style>
    div.stButton > button:first-child {
        background-color: #ff4b4b;
        color: white;
        border-radius: 10px;
        height: 3em;
        width: 200px;
        font-weight: bold;
    }
    div.stButton > button:hover {
        background-color: #ff2b2b;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------
# Chatbot Section
# ---------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

prompt = st.chat_input("Enter a news claim")

if prompt:

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("Fact checking..."):

            result = factcheck_claim(prompt)

            st.markdown(result)

    st.session_state.messages.append(
        {"role": "assistant", "content": result}
    )

# ---------------------------
# OCR Image Verification
# ---------------------------

st.divider()

st.subheader("Fact-check news screenshot")

uploaded_file = st.file_uploader(
    "Upload image",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file:

    with open("temp.png", "wb") as f:
        f.write(uploaded_file.getbuffer())

    text = extract_text_from_image("temp.png")

    

    # Session state for button
    if "image_verified" not in st.session_state:
        st.session_state.image_verified = False

    if not st.session_state.image_verified:

        if st.button("Verify Image Claim"):

            st.session_state.image_verified = True

            with st.spinner("Fact checking image claim..."):

                result = factcheck_claim(text)

                st.success("Verification Result")

                st.write(result)