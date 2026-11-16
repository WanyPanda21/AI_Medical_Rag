
import streamlit as st
import requests


# -----------------------------------
# CONFIGURATION
# -----------------------------------

API_BASE_URL = (
    "https://uoeiu0x0ue.execute-api.ap-southeast-2.amazonaws.com/Prod"
)

st.set_page_config(
    page_title="PharmaCare AI",
    page_icon="🏥",
    layout="centered"
)


# -----------------------------------
# API HELPER FUNCTIONS
# -----------------------------------

def call_api(method, endpoint, payload=None):

    url = f"{API_BASE_URL}{endpoint}"

    try:
        response = requests.request(
            method=method,
            url=url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=60
        )

        try:
            data = response.json()
        except ValueError:
            data = {"message": response.text}

        response.raise_for_status()

        return data

    except requests.exceptions.HTTPError:
        try:
            error_data = response.json()
        except ValueError:
            error_data = response.text

        st.error(f"API Error ({response.status_code})")
        st.json(error_data)

    except requests.exceptions.RequestException as error:
        st.error(f"Unable to connect to AWS API: {error}")

    return None


# -----------------------------------
# APPLICATION HEADER
# -----------------------------------

st.title("🏥 PharmaCare AI")
st.caption("AI-powered Medical Knowledge Assistant")

st.divider()


# -----------------------------------
# PATIENT PORTAL
# -----------------------------------

def patient_portal():

    st.header("Patient Portal")

    st.subheader("Submit Medical Question")

    with st.form("patient_form"):

        patient_id = st.text_input(
            "Patient ID",
            placeholder="PATIENT001"
        )

        age = st.number_input(
            "Age",
            min_value=1,
            max_value=120,
            value=25
        )

        gender = st.selectbox(
            "Gender",
            ["Female", "Male", "Other"]
        )

        question = st.text_area(
            "Your Medical Question",
            placeholder="Enter your medical question here..."
        )

        submitted = st.form_submit_button(
            "Submit Question",
            use_container_width=True
        )

    if submitted:

        if not patient_id.strip() or not question.strip():
            st.warning("Please enter Patient ID and your question.")

        else:

            payload = {
                "patient_id": patient_id.strip(),
                "age": int(age),
                "gender": gender,
                "question": question.strip()
            }

            with st.spinner("Processing your medical question..."):

                result = call_api(
                    "POST",
                    "/cases",
                    payload
                )

            if result is not None:

                st.success("Medical case created successfully!")

                st.subheader("Case Details")
                st.json(result)

                st.session_state.last_case = result

    st.divider()

    # Retrieve existing patient case

    st.subheader("Check Existing Case")

    case_id = st.text_input(
        "Enter Case ID",
        key="patient_case_id"
    )

    if st.button("Get Case Details", use_container_width=True):

        if not case_id.strip():
            st.warning("Please enter a Case ID.")

        else:

            with st.spinner("Retrieving case..."):

                result = call_api(
                    "GET",
                    f"/cases/{case_id.strip()}"
                )

            if result is not None:
                st.success("Case retrieved successfully!")
                st.json(result)


# -----------------------------------
# DOCTOR DASHBOARD
# -----------------------------------

def doctor_dashboard():

    st.header("Doctor Dashboard")

    st.subheader("Pending Medical Cases")

    if st.button("Load Pending Cases", use_container_width=True):

        with st.spinner("Loading pending cases..."):

            result = call_api(
                "GET",
                "/doctor/cases"
            )

        if result is not None:

            st.session_state.pending_cases = result

            st.success("Cases loaded successfully!")

    if "pending_cases" in st.session_state:

        st.write("Pending Cases")

        st.json(st.session_state.pending_cases)

    st.divider()

    # Retrieve individual case

    st.subheader("Review Patient Case")

    case_id = st.text_input(
        "Enter Case ID",
        key="doctor_case_id"
    )

    if st.button("Get Patient Case", use_container_width=True):

        if not case_id.strip():
            st.warning("Please enter a Case ID.")

        else:

            with st.spinner("Retrieving patient case..."):

                result = call_api(
                    "GET",
                    f"/doctor/cases/{case_id.strip()}"
                )

            if result is not None:

                st.session_state.doctor_case = result
                st.session_state.review_case_id = case_id.strip()

                st.success("Patient case retrieved!")
                st.json(result)

    st.divider()

    # Doctor approval / rejection

    st.subheader("Submit Doctor Review")

    with st.form("doctor_review_form"):

        review_case_id = st.text_input(
            "Case ID",
            value=st.session_state.get(
                "review_case_id", ""
            )
        )

        doctor_id = st.text_input(
            "Doctor ID",
            placeholder="DOCTOR001"
        )

        decision = st.selectbox(
            "Review Decision",
            ["APPROVED", "REJECTED"]
        )

        comments = st.text_area(
            "Doctor Comments",
            placeholder="Enter your review comments..."
        )

        review_submitted = st.form_submit_button(
            "Submit Review",
            use_container_width=True
        )

    if review_submitted:

        if not review_case_id.strip() or not doctor_id.strip():
            st.warning("Please enter Case ID and Doctor ID.")

        elif not comments.strip():
            st.warning("Please enter doctor comments.")

        else:

            payload = {
                "doctor_id": doctor_id.strip(),
                "decision": decision,
                "comments": comments.strip()
            }

            with st.spinner("Submitting doctor review..."):

                result = call_api(
                    "POST",
                    f"/doctor/cases/{review_case_id.strip()}",
                    payload
                )

            if result is not None:

                st.success("Doctor review submitted successfully!")

                st.subheader("Review Result")
                st.json(result)


# -----------------------------------
# MAIN APPLICATION
# -----------------------------------

patient_tab, doctor_tab = st.tabs(
    ["Patient Portal", "Doctor Dashboard"]
)

with patient_tab:
    patient_portal()

with doctor_tab:
    doctor_dashboard()


# -----------------------------------
# FOOTER
# -----------------------------------

st.divider()

st.caption(
    "PharmaCare AI | Educational medical information only. "
    "Not a substitute for professional medical advice."
)
