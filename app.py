
import os
import requests
import streamlit as st


# -----------------------------------
# CONFIGURATION
# -----------------------------------

API_URL = os.getenv(
    "MEDICAL_API_URL",
    ""
).rstrip("/")


st.set_page_config(
    page_title="Medical AI Assistant",
    page_icon="🏥",
    layout="wide"
)


st.title("🏥 Medical AI Assistant")

st.caption(
    "AI-powered medical information with doctor review"
)


if not API_URL:
    st.error(
        "MEDICAL_API_URL is missing. "
        "Set your API Gateway URL before running the application."
    )
    st.stop()


# -----------------------------------
# API HELPER
# -----------------------------------

def api_call(method, endpoint, payload=None):

    url = f"{API_URL}{endpoint}"

    try:

        if method == "POST":

            result = requests.post(
                url,
                json=payload,
                timeout=60
            )

        else:

            result = requests.get(
                url,
                timeout=60
            )

        try:
            data = result.json()
        except ValueError:
            data = {"message": result.text}

        if not result.ok:
            st.error(
                data.get("message", "API request failed")
            )
            return None

        return data

    except requests.RequestException as error:

        st.error(f"API connection error: {error}")

        return None


# -----------------------------------
# MAIN TABS
# -----------------------------------

patient_tab, doctor_tab = st.tabs(
    ["👤 Patient Portal", "🩺 Doctor Dashboard"]
)


# ==================================================
# PATIENT PORTAL
# ==================================================

with patient_tab:

    st.header("Submit Medical Query")

    with st.form("patient_query_form"):

        patient_id = st.text_input(
            "Patient ID"
        )

        col1, col2 = st.columns(2)

        with col1:

            age = st.number_input(
                "Age",
                min_value=0,
                max_value=120,
                value=25
            )

        with col2:

            gender = st.selectbox(
                "Gender",
                ["Female", "Male", "Other", "Prefer not to say"]
            )

        query = st.text_area(
            "Describe your symptoms or medical question",
            height=150
        )

        submitted = st.form_submit_button(
            "Submit Query",
            type="primary"
        )

    if submitted:

        if not patient_id.strip() or not query.strip():

            st.warning(
                "Please enter Patient ID and your query."
            )

        else:

            payload = {

                "patient_id": patient_id,

                "patient_info": {
                    "age": age,
                    "gender": gender
                },

                "query": query
            }

            with st.spinner(
                "Retrieving medical information and generating response..."
            ):

                result = api_call(
                    "POST",
                    "/patient/query",
                    payload
                )

            if result:

                st.session_state["request_id"] = (
                    result["request_id"]
                )

                st.success(
                    result["message"]
                )

                st.info(
                    f"Request ID: {result['request_id']}"
                )

                st.warning(
                    "Your AI-generated response is awaiting doctor approval."
                )


    st.divider()

    st.header("Check Your Request")

    request_id = st.text_input(
        "Enter your Request ID",
        value=st.session_state.get("request_id", "")
    )

    if st.button("Check Status"):

        if request_id.strip():

            result = api_call(
                "GET",
                f"/patient/status/{request_id}"
            )

            if result:

                st.info(
                    f"Status: {result['status']}"
                )

                st.session_state["patient_status"] = (
                    result["status"]
                )

        else:

            st.warning("Enter your Request ID.")


    if st.button("View Approved Response"):

        if request_id.strip():

            result = api_call(
                "GET",
                f"/patient/response/{request_id}"
            )

            if result:

                if result["status"] == "APPROVED":

                    st.success("Doctor approved your response.")

                    st.subheader("AI Medical Information")

                    st.write(result["ai_answer"])

                    st.subheader("Sources")

                    for source in result.get("sources", []):

                        st.write(
                            f"- {source.get('source')} "
                            f"(Chunk: {source.get('chunk_index')}, "
                            f"Score: {source.get('score')})"
                        )

                    st.subheader("Doctor Review")

                    review = result["doctor_review"]

                    st.write(
                        f"Doctor ID: {review.get('doctor_id')}"
                    )

                    st.write(
                        f"Comments: {review.get('review_comments')}"
                    )

                    st.write(
                        f"Reviewed at: {review.get('reviewed_at')}"
                    )

                elif result["status"] == "REJECTED":

                    st.error(
                        result["message"]
                    )

                    st.write(
                        result.get("doctor_review", {})
                    )

                else:

                    st.warning(
                        result["message"]
                    )

        else:

            st.warning("Enter your Request ID.")


# ==================================================
# DOCTOR DASHBOARD
# ==================================================

with doctor_tab:

    st.header("Doctor Review Dashboard")

    if st.button("Load Pending Requests"):

        with st.spinner("Loading requests..."):

            result = api_call(
                "GET",
                "/doctor/pending"
            )

        if result:

            st.session_state["pending_requests"] = (
                result["requests"]
            )


    pending_requests = st.session_state.get(
        "pending_requests",
        []
    )

    if pending_requests:

        st.success(
            f"{len(pending_requests)} pending requests found."
        )

        request_ids = [
            item["request_id"]
            for item in pending_requests
        ]

        selected_id = st.selectbox(
            "Select Patient Request",
            request_ids
        )

        selected_request = next(
            item for item in pending_requests
            if item["request_id"] == selected_id
        )

        st.divider()

        st.subheader("Patient Information")

        st.json(
            selected_request["patient_info"]
        )

        st.write(
            f"Patient ID: {selected_request['patient_id']}"
        )

        st.subheader("Patient Query")

        st.write(
            selected_request["patient_query"]
        )

        st.subheader("AI Generated Response")

        st.write(
            selected_request["ai_answer"]
        )

        st.subheader("Retrieved Sources")

        st.json(
            selected_request["sources"]
        )

        st.divider()

        st.subheader("Doctor Review")

        doctor_id = st.text_input(
            "Doctor ID",
            key="doctor_id"
        )

        comments = st.text_area(
            "Doctor Comments",
            height=120
        )

        col1, col2 = st.columns(2)

        with col1:

            approve = st.button(
                "Approve Response",
                type="primary"
            )

        with col2:

            reject = st.button(
                "Reject Response"
            )

        decision = None

        if approve:
            decision = "APPROVED"

        elif reject:
            decision = "REJECTED"

        if decision:

            if not doctor_id.strip() or not comments.strip():

                st.warning(
                    "Doctor ID and review comments are required."
                )

            else:

                payload = {
                    "doctor_id": doctor_id,
                    "decision": decision,
                    "review_comments": comments
                }

                result = api_call(
                    "POST",
                    f"/doctor/review/{selected_id}",
                    payload
                )

                if result:

                    st.success(
                        result["message"]
                    )

                    st.session_state["pending_requests"] = [
                        item for item in pending_requests
                        if item["request_id"] != selected_id
                    ]

                    st.rerun()

    else:

        st.info(
            "No pending requests loaded. Click Load Pending Requests."
        )
