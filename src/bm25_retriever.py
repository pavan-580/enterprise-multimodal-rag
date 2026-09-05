from rank_bm25 import BM25Okapi
import re


def tokenize(text):
    """
    Convert text into lowercase tokens.
    """
    return re.findall(r"\b\w+\b", text.lower())


class BM25Retriever:

    def __init__(self, documents):
        """
        Build a BM25 index from our document chunks.
        """

        self.documents = documents

        # Tokenize every chunk
        self.tokenized_documents = [
            tokenize(document["content"])
            for document in documents
        ]

        # Create BM25 index
        self.bm25 = BM25Okapi(self.tokenized_documents)

    def search(self, query, top_k=5):
        """
        Search the chunks using BM25.
        """

        query_tokens = tokenize(query)

        scores = self.bm25.get_scores(query_tokens)

        # Sort indexes by score, highest first
        ranked_indexes = sorted(
            range(len(scores)),
            key=lambda index: scores[index],
            reverse=True
        )

        results = []

        for index in ranked_indexes[:top_k]:

            document = self.documents[index].copy()

            document["score"] = float(scores[index])

            results.append(document)

        return results