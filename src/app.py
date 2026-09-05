import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.rag_pipeline import RAGPipeline
# -----------------------------
# Page configuration
# -----------------------------

st.set_page_config(
    page_title="Enterprise Multimodal RAG",
    page_icon="📚",
    layout="wide"
)


# -----------------------------
# Title
# -----------------------------

st.title("📚 Enterprise Multimodal RAG System")

st.write(
    "Ask questions about the Enterprise Operations Report "
    "using grounded retrieval."
)


# -----------------------------
# Load RAG pipeline
# -----------------------------

PDF_PATH = "documents/Enterprise_Operations_Report.pdf"

@st.cache_resource
def load_pipeline():
    return RAGPipeline(PDF_PATH)


pipeline = load_pipeline()


# -----------------------------
# Question input
# -----------------------------

question = st.text_input(
    "Ask a question",
    placeholder="Example: How many high-priority cases were resolved?"
)


# -----------------------------
# Ask button
# -----------------------------

if st.button("Ask Question"):

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        with st.spinner("Searching the enterprise document..."):

            answer, sources = pipeline.answer(question)

        # -----------------------------
        # Answer
        # -----------------------------

        st.subheader("Answer")

        st.success(answer)

        # -----------------------------
        # Sources
        # -----------------------------

        st.subheader("Sources")

        if sources:

            seen = set()

            for source in sources:

                key = (
                    source["source"],
                    source["page"],
                    source["type"]
                )

                if key in seen:
                    continue

                seen.add(key)

                st.write(
                    f"📄 **{source['source']}** | "
                    f"Page **{source['page']}** | "
                    f"Type: **{source['type']}**"
                )

        else:

            st.info("No sources available.")