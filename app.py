
import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load API key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Page configuration
st.set_page_config(
    page_title="Brandstro AI",
    page_icon="💜",
    layout="centered"
)

# Purple theme
st.markdown("""
<style>
.stApp {
    background: linear-gradient(
        135deg, #10091f, #24113d, #321451
    );
    color: white;
}

header {
    background: transparent !important;
}

.main .block-container {
    max-width: 850px;
    padding-top: 2rem;
}

.brand-title {
    text-align: center;
    font-size: 45px;
    font-weight: 800;
    color: #c084fc;
    letter-spacing: 3px;
}

.brand-subtitle {
    text-align: center;
    color: #d8b4fe;
    font-size: 15px;
    margin-bottom: 25px;
}

.welcome-card {
    background: linear-gradient(
        135deg, #4c1d95, #7e22ce
    );
    padding: 22px;
    border-radius: 18px;
    text-align: center;
    margin-bottom: 25px;
}

.stChatMessage {
    background-color: rgba(126, 34, 206, 0.18);
    border: 1px solid rgba(192, 132, 252, 0.25);
    border-radius: 15px;
}

.stChatInput textarea {
    background-color: #24113d !important;
    color: white !important;
}

.stButton button {
    background: #7e22ce;
    color: white;
    border: 1px solid #c084fc;
    border-radius: 12px;
}

.stButton button:hover {
    background: #9333ea;
    color: white;
    border-color: #e9d5ff;
}
</style>
""", unsafe_allow_html=True)


# Brandstro AI instructions
SYSTEM_PROMPT = """
You are Brandstro AI, the official customer support
assistant for Brandstro, a branding and design studio
located in Nagercoil, Tamil Nadu, India.

Your main purpose is to help customers understand
Brandstro's services.

BRANDSTRO SERVICES:

1. Premium Logo Design
2. Brand Identity Systems
3. Packaging Design
4. Marketing Creatives

YOUR RESPONSIBILITIES:

- Welcome customers politely.
- Answer customer questions.
- Explain logo design services.
- Explain branding and identity services.
- Help customers with packaging design enquiries.
- Explain marketing creatives.
- Guide customers through the design process.
- Ask customers about their design requirements.

IMPORTANT RULES:

- Use simple and professional English.
- Be friendly and helpful.
- Give clear answers.
- Keep responses short and useful.
- Never invent prices or delivery dates.
- Never invent contact information.
- If you do not know something, say so politely.
- Do not claim a booking or payment is confirmed.
"""


# Initialize Gemini client
@st.cache_resource
def get_client():
    if not API_KEY:
        return None
    return genai.Client(api_key=API_KEY)


client = get_client()


# Main heading
st.markdown(
    '<div class="brand-title">BRANDSTRO AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="brand-subtitle">'
    'YOUR CREATIVE BRANDING ASSISTANT 💜'
    '</div>',
    unsafe_allow_html=True
)

# Welcome section
st.markdown("""
<div class="welcome-card">
    <h2>Welcome to Brandstro! 👋</h2>
    <p>Your brand deserves a beautiful identity.</p>
    <p>How can I help you today?</p>
</div>
""", unsafe_allow_html=True)


# Sidebar
with st.sidebar:
    st.markdown("## 💜 Brandstro AI")
    st.write("Your company support assistant.")

    st.markdown("---")
    st.markdown("### Our Services")

    st.write("🎨 Premium Logo Design")
    st.write("✨ Brand Identity Systems")
    st.write("📦 Packaging Design")
    st.write("📢 Marketing Creatives")

    st.markdown("---")
    st.caption("Powered by Google Gemini AI")

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Customer message input
user_input = st.chat_input(
    "Ask Brandstro anything... 💬"
)


if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):

        if client is None:
            response_text = (
                "Your Gemini API key is missing. "
                "Please check your .env file."
            )

        else:
            try:
                with st.spinner("Brandstro AI is thinking..."):

                    conversation = []

                    for msg in st.session_state.messages:
                        conversation.append(
                            types.Content(
                                role=(
                                    "user"
                                    if msg["role"] == "user"
                                    else "model"
                                ),
                                parts=[
                                    types.Part(text=msg["content"])
                                ]
                            )
                        )

                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=conversation,
                        config=types.GenerateContentConfig(
                            system_instruction=SYSTEM_PROMPT,
                            temperature=0.5,
                            max_output_tokens=800
                        )
                    )

                    response_text = (
                        response.text or
                        "Sorry, I couldn't generate a response."
                    )

            except Exception as e:
                response_text = (
                    "Sorry! Something went wrong. "
                    "Please check your API key and internet connection."
                )
                st.error(str(e))

        st.markdown(response_text)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response_text
    })


# Footer
st.markdown("---")

st.markdown(
    "<p style='text-align:center;color:#c084fc;'>"
    "💜 Made with AI for Brandstro | Nagercoil"
    "</p>",
    unsafe_allow_html=True
)
