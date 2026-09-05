import re


def normalize(value):
    """Normalize text for comparison."""
    if value is None:
        return ""

    value = str(value).lower().strip()
    value = re.sub(r"\s+", " ", value)

    return value


def detect_priority(question):
    """Find the priority mentioned in the question."""

    priorities = ["critical", "high", "medium", "low"]

    question = normalize(question)

    for priority in priorities:
        if priority in question:
            return priority

    return None


def detect_requested_field(question):
    """Find which table field the question is asking for."""

    question = normalize(question)

    if "resolved" in question:
        return "resolved"

    if "received" in question:
        return "cases received"

    if "average resolution" in question:
        return "average resolution"

    return None


def answer_table_question(question, documents):
    """
    Answer simple structured questions directly from tables.

    Returns:
        str or None
    """

    priority = detect_priority(question)
    requested_field = detect_requested_field(question)

    if priority is None or requested_field is None:
        return None

    for document in documents:

        if document.get("type") != "table":
            continue

        fields = {}

        for line in document.get("content", "").splitlines():

            if ":" not in line:
                continue

            key, value = line.split(":", 1)

            fields[normalize(key)] = value.strip()

        table_priority = normalize(fields.get("priority"))

        if table_priority != priority:
            continue

        if requested_field in fields:
            return fields[requested_field]

    return None