from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


class LLM:
    def __init__(self, model_name="google/flan-t5-base"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    def build_prompt(self, question, documents):
        context_parts = []

        for document in documents:
            context_parts.append(
                f"Source: {document['source']}, "
                f"Page: {document['page']}\n"
                f"Content: {document['content']}"
            )

        context = "\n\n".join(context_parts)

        prompt = f"""
Answer the question using only the provided context.

Rules:
- Use only information supported by the context.
- Do not invent or guess facts.
- For table questions, carefully match the requested field or column with its value.
- Do not confuse "Cases Received" with "Resolved".
- If the question asks for a number, return the exact number from the relevant field.
- If the answer is not present, say:
The answer is not available in the provided document.

Context:
{context}

Question:
{question}

Answer:
"""

        return prompt

    def generate(self, question, documents):
        prompt = self.build_prompt(question, documents)

        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True
        )

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=100
        )

        answer = self.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        )

        return answer.strip()