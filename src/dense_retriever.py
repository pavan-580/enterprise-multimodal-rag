from src.embedding import EmbeddingModel
import numpy as np


class DenseRetriever:

    def __init__(self, documents):
        """
        Create dense embeddings for all document chunks.
        """

        self.documents = documents
        self.embedding_model = EmbeddingModel()

        self.document_embeddings = self.embedding_model.encode(
            [document["content"] for document in documents]
        )

    def search(self, query, top_k=5):
        """
        Find the chunks that are semantically
        most similar to the query.
        """

        query_embedding = self.embedding_model.encode([query])[0]

        # Calculate cosine similarity
        document_norms = np.linalg.norm(
            self.document_embeddings,
            axis=1
        )

        query_norm = np.linalg.norm(query_embedding)

        similarities = np.dot(
            self.document_embeddings,
            query_embedding
        ) / (document_norms * query_norm)

        # Highest similarity first
        ranked_indexes = np.argsort(
            similarities
        )[::-1]

        results = []

        for index in ranked_indexes[:top_k]:

            document = self.documents[index].copy()

            document["score"] = float(similarities[index])

            results.append(document)

        return results