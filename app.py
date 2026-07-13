import streamlit as st

from rag_utils import (
    extract_text,
    detect_document_type,
    generate_summary,
    ask_ai
)

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="AI Smart Document Assistant",
    layout="wide"
)

# ---------------- TITLE ---------------- #

st.title("🤖 AI Smart Document Assistant")

st.write("""
Upload any document:
- Health Report
- Resume
- Employee Tracker
- Research PDF
- Excel Files
- Notes

AI will:
- Summarize documents
- Give suggestions
- Answer questions
- Provide intelligent insights
""")

# ---------------- SESSION STATE ---------------- #

if "document_text" not in st.session_state:
    st.session_state.document_text = ""

if "doc_type" not in st.session_state:
    st.session_state.doc_type = ""

# ---------------- FILE UPLOAD ---------------- #

uploaded_files = st.file_uploader(
    "Upload Files",
    accept_multiple_files=True,
    type=["pdf", "docx", "txt", "xlsx", "csv"]
)

# ---------------- PROCESS FILES ---------------- #

if st.button("Process Files"):

    if uploaded_files:

        with st.spinner("Reading documents..."):

            all_text = extract_text(uploaded_files)

            st.session_state.document_text = all_text

        with st.spinner("Detecting document type..."):

            doc_type = detect_document_type(all_text)

            st.session_state.doc_type = doc_type

        st.success("Documents Processed Successfully!")

        st.subheader("Detected Document Type")

        st.write(doc_type.upper())

        with st.spinner("Generating AI Summary..."):

            summary = generate_summary(
                all_text,
                doc_type
            )

        st.subheader("AI Summary & Suggestions")

        st.write(summary)

    else:

        st.warning("Please upload files.")

# ---------------- QUESTIONS ---------------- #

st.subheader("Ask Questions")

user_question = st.text_input(
    "Ask anything about uploaded documents"
)

if user_question:

    if st.session_state.document_text == "":

        st.warning("Please upload documents first.")

    else:

        with st.spinner("Generating Answer..."):

            response = ask_ai(
                st.session_state.document_text,
                user_question,
                st.session_state.doc_type
            )

        st.subheader("AI Response")

        st.write(response)