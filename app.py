
import os
import requests
import streamlit as st

API_URL = os.getenv("RAG_API_URL", "")

st.set_page_config(
    page_title="Medical AI Assistant",
    page_icon="🩺",
    layout="centered"
)

st.title("🩺 Medical AI Assistant")
st.caption("Ask questions about medicines, diseases and symptoms.")

if not API_URL:
    st.error("RAG_API_URL is not configured.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

        if msg.get("sources"):
            with st.expander("Retrieved Sources"):
                for source in msg["sources"]:
                    st.write(f"PDF: {source.get('source')}")
                    st.write(f"Chunk: {source.get('chunk_index')}")
                    st.write(f"Score: {source.get('score')}")

question = st.chat_input("Ask your medical question...")

if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching medical documents..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"question": question},
                    timeout=35
                )

                response.raise_for_status()
                data = response.json()

                if not data.get("success"):
                    raise Exception(data.get("error", "Request failed"))

                answer = data["answer"]
                sources = data.get("sources", [])

                st.markdown(answer)

                if sources:
                    with st.expander("Retrieved Sources"):
                        for source in sources:
                            st.write(f"PDF: {source.get('source')}")
                            st.write(f"Chunk: {source.get('chunk_index')}")
                            st.write(f"Score: {source.get('score')}")

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })

            except requests.exceptions.Timeout:
                st.error("Request timed out.")

            except requests.exceptions.RequestException as e:
                st.error(f"Backend connection failed: {e}")

            except Exception as e:
                st.error(f"Error: {e}")
