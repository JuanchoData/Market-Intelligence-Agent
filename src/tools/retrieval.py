from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"

START_MARKER = "Item 1A. Risk Factors"
END_MARKER = "Item 1B. Unresolved Staff Comments"


class DocumentRetriever:
    def __init__(self):
        """
        Load the embedding model and prepare storage
        for text chunks and their embeddings.
        """

        self.model = SentenceTransformer(
            MODEL_NAME
        )

        self.chunks = []
        self.embeddings = None

    def extract_risk_section(
        self,
        text: str
    ) -> str:
        """
        Extract only NVIDIA's Item 1A Risk Factors section.
        """

        start = text.find(
            START_MARKER
        )

        end = text.find(
            END_MARKER,
            start
        )

        if start == -1:
            raise ValueError(
                "Could not find Item 1A Risk Factors."
            )

        if end == -1:
            raise ValueError(
                "Could not find Item 1B."
            )

        return text[start:end]

    def chunk_text(
        self,
        text: str,
        chunk_size: int = 400,
        overlap: int = 80
    ):
        """
        Split the risk section into overlapping chunks.

        Overlap helps preserve context between chunks.
        """

        words = text.split()

        chunks = []

        start = 0

        while start < len(words):
            end = start + chunk_size

            chunk = " ".join(
                words[start:end]
            )

            chunks.append(chunk)

            start += (
                chunk_size - overlap
            )

        return chunks

    def index_document(
        self,
        file_path: str
    ):
        """
        Load the 10-K, isolate Item 1A,
        split it into chunks,
        and create embeddings.
        """

        text = Path(
            file_path
        ).read_text(
            encoding="utf-8"
        )

        risk_text = self.extract_risk_section(
            text
        )

        self.chunks = self.chunk_text(
            risk_text
        )

        print(
            f"Risk Factors chunks: "
            f"{len(self.chunks)}"
        )

        self.embeddings = self.model.encode(
            self.chunks,
            normalize_embeddings=True
        )

    def retrieve(
        self,
        query: str,
        top_k: int = 3
    ):
        """
        Retrieve the most relevant Risk Factors chunks.
        """

        query_embedding = self.model.encode(
            [query],
            normalize_embeddings=True
        )[0]

        scores = np.dot(
            self.embeddings,
            query_embedding
        )

        top_indices = np.argsort(
            scores
        )[::-1][:top_k]

        results = []

        for index in top_indices:
            results.append(
                {
                    "score": float(
                        scores[index]
                    ),
                    "text": self.chunks[index]
                }
            )

        return results