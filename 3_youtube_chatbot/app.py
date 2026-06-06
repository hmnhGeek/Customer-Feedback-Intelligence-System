import streamlit as st

from services.youtube_transcript_service import YouTubeTranscriptService
from services.chat_service import ChatService


st.set_page_config(page_title="YouTube Chatbot", layout="wide")


# ---------------------------
# SESSION STATE
# ---------------------------
if "stage" not in st.session_state:
    st.session_state.stage = "input"  # input | chat

if "transcript" not in st.session_state:
    st.session_state.transcript = None

if "chat_service" not in st.session_state:
    st.session_state.chat_service = None

if "messages" not in st.session_state:
    st.session_state.messages = []


st.title("🎥 YouTube Video Chatbot")


# ---------------------------
# STAGE 1: INPUT URL
# ---------------------------
if st.session_state.stage == "input":

    st.subheader("Step 1: Enter YouTube URL")

    url = st.text_input("YouTube URL")

    if st.button("Load Video") and url:

        with st.spinner("Fetching transcript..."):

            try:
                transcript = YouTubeTranscriptService.get_transcript(url)

                st.session_state.transcript = transcript
                st.session_state.chat_service = ChatService(transcript)
                st.session_state.messages = []

                st.session_state.stage = "chat"

                st.rerun()

            except Exception as e:
                st.error(f"Failed to load transcript: {e}")


# ---------------------------
# STAGE 2: CHAT INTERFACE
# ---------------------------
elif st.session_state.stage == "chat":

    st.subheader("💬 Chat with the video")

    # Transcript preview
    with st.expander("📄 View Transcript"):
        st.write(st.session_state.transcript.text[:3000])

    # Reset button
    if st.button("🔄 Load Another Video"):
        st.session_state.stage = "input"
        st.session_state.transcript = None
        st.session_state.chat_service = None
        st.session_state.messages = []
        st.rerun()

    # ---------------------------
    # CHAT HISTORY
    # ---------------------------
    for msg in st.session_state.messages:
        avatar = "🧑‍💻" if msg["role"] == "user" else "🤖"

        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    # ---------------------------
    # USER INPUT
    # ---------------------------
    user_input = st.chat_input("Ask something about the video...")

    if user_input:

        # Save user message
        st.session_state.messages.append(
            {"role": "user", "content": user_input}
        )

        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(user_input)

        # ---------------------------
        # ASSISTANT RESPONSE (STREAMING + TYPING)
        # ---------------------------
        with st.chat_message("assistant", avatar="🤖"):
            typing_placeholder = st.empty()
            response_placeholder = st.empty()

            typing_placeholder.markdown("🤖 *Thinking...*")

            full_response = ""

            for chunk in st.session_state.chat_service.chat(
                user_input,
                # history without latest user msg
                st.session_state.messages[:-1]
            ):
                full_response = chunk

                typing_placeholder.empty()
                response_placeholder.markdown(full_response)

            typing_placeholder.empty()

        # Save assistant message
        st.session_state.messages.append(
            {"role": "assistant", "content": full_response}
        )
