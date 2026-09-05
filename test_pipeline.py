from src.rag_pipeline import RAGPipeline


PDF_PATH = "documents/Enterprise_Operations_Report.pdf"


pipeline = RAGPipeline(PDF_PATH)


question = "How many high-priority support cases were resolved?"


answer, sources = pipeline.answer(question)


print("\n==============================")
print("QUESTION")
print("==============================")
print(question)


print("\n==============================")
print("ANSWER")
print("==============================")
print(answer)


print("\n==============================")
print("SOURCES")
print("==============================")


seen = set()

source_number = 1

for source in sources:

    key = (
        source["source"],
        source["page"],
        source["type"]
    )

    if key in seen:
        continue

    seen.add(key)

    print(
        f"[{source_number}] "
        f"{source['source']}, "
        f"Page {source['page']}, "
        f"Type: {source['type']}"
    )

    source_number += 1