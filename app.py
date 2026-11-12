
import streamlit as st
import requests
import os

st.set_page_config(
    page_title="Medical RAG Assistant",
    page_icon="🏥",
    layout="centered"
)

# API Gateway endpoint
API_URL = st.secrets.get(
    "API_URL",
    os.getenv("API_URL", "")
)

st.title("🏥 Medical RAG Assistant")
st.write("Ask questions based on your medical PDF documents.")

st.divider()

query = st.text_area(
    "Enter your medical question",
    placeholder="Example: What are the symptoms of diabetes?",
    height=120
)

if st.button("🚀 Hit", type="primary", use_container_width=True):

    if not query.strip():
        st.warning("Please enter a question.")

    elif not API_URL:
        st.error("API URL is not configured.")

    else:
        try:
            with st.spinner("Searching medical documents and generating answer..."):

                response = requests.post(
                    API_URL,
                    json={"query": query.strip()},
                    timeout=35
                )

                if response.status_code == 200:

                    result = response.json()

                    st.success("Answer generated successfully!")

                    st.subheader("Answer")
                    st.markdown(result.get("answer", "No answer returned."))

                    st.divider()

                    st.subheader("Sources")

                    sources = result.get("sources", [])

                    if sources:
                        for source in sources:
                            with st.expander(
                                f"{source['source']} - Chunk {source['chunk_index']}"
                            ):
                                st.write("Source:", source["source"])
                                st.write("Chunk:", source["chunk_index"])
                                st.write("Score:", source["score"])
                    else:
                        st.info("No sources available.")

                else:
                    st.error(
                        f"API Error ({response.status_code}): "
                        f"{response.text}"
                    )

        except requests.exceptions.Timeout:
            st.error(
                "The request timed out. The backend may need more time."
            )

        except requests.exceptions.RequestException as e:
            st.error(f"Connection error: {str(e)}")
