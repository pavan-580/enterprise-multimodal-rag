from src.bm25_retriever import BM25Retriever
from src.dense_retriever import DenseRetriever


class HybridRetriever:

    def __init__(self, documents):
        """
        Create both BM25 and dense retrievers.
        """

        self.documents = documents

        self.bm25_retriever = BM25Retriever(documents)
        self.dense_retriever = DenseRetriever(documents)

    def normalize_scores(self, scores):
        """
        Convert scores to a 0-1 range.
        """

        minimum = min(scores)
        maximum = max(scores)

        if maximum == minimum:
            return [1.0 for _ in scores]

        return [
            (score - minimum) / (maximum - minimum)
            for score in scores
        ]

    def search(self, query, top_k=5):
        """
        Perform hybrid retrieval using BM25
        and dense semantic search.
        """

        bm25_results = self.bm25_retriever.search(
            query,
            top_k=len(self.documents)
        )

        dense_results = self.dense_retriever.search(
            query,
            top_k=len(self.documents)
        )

        # Extract scores
        bm25_scores = [
            result["score"]
            for result in bm25_results
        ]

        dense_scores = [
            result["score"]
            for result in dense_results
        ]

        # Normalize scores
        normalized_bm25 = self.normalize_scores(
            bm25_scores
        )

        normalized_dense = self.normalize_scores(
            dense_scores
        )

        # Store scores by chunk ID
        bm25_score_map = {
            result["chunk_id"]: score
            for result, score in zip(
                bm25_results,
                normalized_bm25
            )
        }

        dense_score_map = {
            result["chunk_id"]: score
            for result, score in zip(
                dense_results,
                normalized_dense
            )
        }

        # Combine both scores
        combined_results = []

        for document in self.documents:

            chunk_id = document["chunk_id"]

            bm25_score = bm25_score_map.get(
                chunk_id,
                0.0
            )

            dense_score = dense_score_map.get(
                chunk_id,
                0.0
            )

            hybrid_score = (
                0.5 * bm25_score
                + 0.5 * dense_score
            )

            result = document.copy()

            result["bm25_score"] = bm25_score
            result["dense_score"] = dense_score
            result["hybrid_score"] = hybrid_score

            combined_results.append(result)

        # Highest hybrid score first
        combined_results.sort(
            key=lambda result: result["hybrid_score"],
            reverse=True
        )

        return combined_results[:top_k]