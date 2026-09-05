from src.llm import LLM


llm = LLM()

documents = [
    {
        "content": "Risk: System outage | Impact: High | Likelihood: Low | Mitigation: Backup and recovery testing",
        "type": "table",
        "page": 3,
        "source": "Enterprise_Operations_Report.pdf"
    }
]

question = "What is the mitigation for system outage risk?"

answer = llm.generate(question, documents)

print("\nQuestion:")
print(question)

print("\nAnswer:")
print(answer)