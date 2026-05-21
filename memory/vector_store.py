from sentence_transformers import SentenceTransformer
import numpy as np


model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

memory_store = []


def add_memory(text, metadata=None):

    embedding = model.encode(text)

    memory_store.append({
        "text": text,
        "embedding": embedding,
        "metadata": metadata
    })


def search_memory(query, top_k=3):

    query_embedding = model.encode(query)

    similarities = []

    for item in memory_store:

        similarity = np.dot(
            query_embedding,
            item["embedding"]
        ) / (
            np.linalg.norm(query_embedding)
            * np.linalg.norm(item["embedding"])
        )

        similarities.append(
            (similarity, item)
        )

    similarities.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return [
        item[1]
        for item in similarities[:top_k]
    ]
