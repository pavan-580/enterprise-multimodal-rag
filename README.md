# Enterprise Multimodal RAG System

An enterprise-focused Multimodal Retrieval-Augmented Generation (RAG)
system designed to answer questions from enterprise documents using
text, tables, images, OCR, hybrid retrieval, reranking, and grounded
LLM generation.

## Project Overview

The system processes enterprise PDF documents and converts their
content into searchable information.

It supports:

- Text extraction
- Table extraction
- Image extraction
- OCR processing
- Text chunking
- BM25 lexical retrieval
- Dense vector retrieval
- Hybrid retrieval
- Cross-encoder reranking
- Structured table question answering
- Chart question answering
- Grounded LLM generation
- Source/page attribution
- Audit logging
- Error logging
- Streamlit web interface

## Architecture

PDF Document
    |
    v
Document Loader
    |
    +---- Text
    |
    +---- Tables
    |
    +---- Images
             |
             v
            OCR
    |
    v
Normalization
    |
    v
Chunking
    |
    +-------------------+
    |                   |
    v                   v
 BM25 Retrieval    Dense Retrieval
    |                   |
    +---------+---------+
              |
              v
       Hybrid Retrieval
              |
              v
       Cross-Encoder
         Reranking
              |
              v
     Structured QA Layer
       |             |
       |             +---- Chart QA
       +------------------ Table QA
              |
              v
       Grounded LLM
              |
              v
       Answer + Sources
              |
              v
        Audit Logging

## Technologies

- Python
- PyMuPDF
- Tesseract OCR
- pytesseract
- Pillow
- Sentence Transformers
- BM25
- Cross-Encoder
- Hugging Face Transformers
- FLAN-T5
- Streamlit

## Project Structure

major/
|
+-- documents/
|   +-- Enterprise_Operations_Report.pdf
|
+-- src/
|   +-- app.py
|   +-- rag_pipeline.py
|   +-- document_loader.py
|   +-- image_extractor.py
|   +-- ocr_processor.py
|   +-- chunker.py
|   +-- bm25_retriever.py
|   +-- embedding.py
|   +-- dense_retriever.py
|   +-- hybrid_retriever.py
|   +-- reranker.py
|   +-- table_qa.py
|   +-- chart_qa.py
|   +-- llm.py
|   +-- audit_logger.py
|   +-- error_handler.py
|
+-- test_pipeline.py
+-- requirements.txt
+-- README.md

## Running the Application

Activate the virtual environment:

    venv\Scripts\activate

Install dependencies:

    pip install -r requirements.txt

Run the Streamlit application:

    streamlit run src/app.py

The application will open locally in the browser.

## Example Questions

### Text question

What are the standard working hours?

### Table question

How many high-priority support cases were resolved?

Expected answer:

88

### Another table question

How many medium-priority cases were received?

Expected answer:

214

### Chart question

Which quarter had the highest revenue?

Expected answer:

Q4

### Unsupported question

Who is the CEO of the company?

The system should respond that the answer is not available
in the provided document instead of inventing an answer.

## Error Handling

The system records application errors in:

    logs/error.log

For example, an invalid PDF path produces a logged
FileNotFoundError.

## Audit Logging

Each processed question is recorded in:

    logs/audit_log.jsonl

The audit record contains information such as:

- Timestamp
- Question
- Answer
- Source document
- Page
- Document type
- Chunk ID
- Retrieval scores
- Reranking score

## Key Design Principle

The system separates retrieval from generation.

Retrieval identifies relevant evidence from the enterprise
document, while the LLM generates a natural-language answer
using that evidence.

This helps reduce unsupported answers and provides traceability
through source information and audit logs.