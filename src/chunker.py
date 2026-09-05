import re


def split_text(text, max_chars=500, overlap=100):
    """
    Split long text into smaller overlapping chunks.
    """

    text = re.sub(r"\s+", " ", text).strip()

    chunks = []
    start = 0

    while start < len(text):

        end = min(start + max_chars, len(text))

        # Try to end the chunk at a word boundary
        if end < len(text):
            boundary = text.rfind(" ", start, end)

            if boundary > start:
                end = boundary

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        # Stop when we reach the end
        if end >= len(text):
            break

        # Move backward slightly to create overlap
        start = max(end - overlap, start + 1)

    return chunks


def create_chunks(documents, max_chars=500, overlap=100):
    """
    Create searchable chunks from normalized documents.
    """

    chunks = []
    chunk_number = 0

    for document in documents:

        document_type = document["type"]

        # Text can be long, so split it
        if document_type == "text":
            pieces = split_text(
                document["content"],
                max_chars=max_chars,
                overlap=overlap
            )

        # Tables and OCR images are already meaningful units
        else:
            pieces = [document["content"]]

        for piece in pieces:

            chunk = document.copy()

            chunk["content"] = piece
            chunk["chunk_id"] = f"chunk_{chunk_number:04d}"

            chunks.append(chunk)

            chunk_number += 1

    return chunks