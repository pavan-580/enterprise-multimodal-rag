import json
from datetime import datetime
from pathlib import Path


def log_query(
    question,
    answer,
    sources,
    log_file="logs/audit_log.jsonl"
):
    """
    Save one RAG query and its evidence to an audit log.
    """

    log_path = Path(log_file)

    log_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    record = {
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "answer": answer,
        "sources": []
    }

    for source in sources:

        record["sources"].append({
            "source": source.get("source"),
            "page": source.get("page"),
            "type": source.get("type"),
            "chunk_id": source.get("chunk_id"),
            "hybrid_score": source.get("hybrid_score"),
            "rerank_score": source.get("rerank_score")
        })

    with open(
        log_path,
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            json.dumps(record)
            + "\n"
        )