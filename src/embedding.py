from sentence_transformers import SentenceTransformer


class EmbeddingModel:

    def __init__(self, model_name="all-MiniLM-L6-v2"):
        """
        Load the pretrained sentence embedding model.
        """
        self.model = SentenceTransformer(model_name)

    def encode(self, texts):
        """
        Convert text into dense numerical vectors.
        """
        return self.model.encode(
            texts,
            convert_to_numpy=True
        )