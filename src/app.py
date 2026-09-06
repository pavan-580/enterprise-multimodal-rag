import sys
import tempfile
from pathlib import Path

import streamlit as st


# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.rag_pipeline import RAGPipeline


st.set_page_config(
    page_title="Enterprise Multimodal RAG",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Enterprise Multimodal RAG System")

st.write(
    "Upload a PDF containing text, tables, or images "
    "and ask questions about its content."
)


# --------------------------------------------------
# PDF Upload
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "Upload a PDF document",
    type=["pdf"]
)


if uploaded_file is not None:

    st.success(f"Uploaded: {uploaded_file.name}")

    # Create a temporary directory
    temp_dir = Path(tempfile.mkdtemp())

    # Keep the original uploaded filename
    safe_filename = Path(uploaded_file.name).name

    # Create the PDF path using the original filename
    pdf_path = temp_dir / safe_filename

    # Save the uploaded PDF
    with open(pdf_path, "wb") as temp_file:
        temp_file.write(uploaded_file.getbuffer())


    # --------------------------------------------------
    # Process PDF
    # --------------------------------------------------

    if st.button("Process PDF"):

        with st.spinner(
            "Processing PDF. Extracting text, tables and images..."
        ):

            try:
                pipeline = RAGPipeline(pdf_path)

                st.session_state["pipeline"] = pipeline
                st.session_state["document_name"] = uploaded_file.name

                st.success(
                    "PDF processed successfully. "
                    "You can now ask questions."
                )

            except Exception as error:

                st.error(
                    "Unable to process the PDF."
                )

                st.exception(error)


# --------------------------------------------------
# Question Answering
# --------------------------------------------------

if "pipeline" in st.session_state:

    st.divider()

    st.subheader(
        f"Ask questions about: "
        f"{st.session_state['document_name']}"
    )

    question = st.text_input(
        "Your question",
        placeholder="Example: What was the highest revenue?"
    )


    if st.button("Ask Question"):

        if not question.strip():

            st.warning("Please enter a question.")

        else:

            pipeline = st.session_state["pipeline"]

            with st.spinner(
                "Searching relevant content..."
            ):

                answer, sources = pipeline.answer(
                    question
                )


            # --------------------------------------------------
            # Answer
            # --------------------------------------------------

            st.subheader("Answer")

            st.success(answer)


            # --------------------------------------------------
            # Sources
            # --------------------------------------------------

            st.subheader("Sources")

            if sources:

                seen = set()

                for source in sources:

                    key = (
                        source.get("source"),
                        source.get("page"),
                        source.get("type")
                    )

                    if key in seen:
                        continue

                    seen.add(key)

                    st.write(
                        f"📄 **{source.get('source')}** | "
                        f"Page **{source.get('page')}** | "
                        f"Type: **{source.get('type')}**"
                    )

            else:

                st.info(
                    "No sources were available."
                )