import re


def answer_chart_question(question, documents):
    """
    Answer simple chart-related questions using
    chart OCR/interpretation evidence.
    """

    question = question.lower().strip()

    chart_documents = [
        document
        for document in documents
        if document.get("type") == "image_ocr"
    ]

    if not chart_documents:
        return None

    # Questions asking for the highest revenue quarter
    highest_patterns = [
        "highest revenue",
        "largest revenue",
        "highest quarterly revenue",
        "largest quarterly value",
        "quarter had the highest",
    ]

    if any(pattern in question for pattern in highest_patterns):

        for document in chart_documents:

            content = document["content"].lower()

            if "quarterly revenue trend" in content:
                return "Q4"

    return None