from sentence_transformers import CrossEncoder


class Reranker:

    def __init__(
        self,
        model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"
    ):
        """
        Load the pretrained cross-encoder reranking model.
        """

        self.model = CrossEncoder(model_name)

    def rerank(self, query, documents, top_k=5):
        """
        Rerank retrieved documents according
        to their relevance to the query.
        """

        if not documents:
            return []

        pairs = [
            [query, document["content"]]
            for document in documents
        ]

        scores = self.model.predict(pairs)

        results = []

        for document, score in zip(documents, scores):

            result = document.copy()

            result["rerank_score"] = float(score)

            results.append(result)

        results.sort(
            key=lambda result: result["rerank_score"],
            reverse=True
        )

        return results[:top_k]