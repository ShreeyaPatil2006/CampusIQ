
import os
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ..models import FAQ

# Google Cloud embedding cache
_document_cache = {}
_embedding_client = None


def normalize(text):
    return re.sub(
        r"\s+",
        " ",
        re.sub(r"[^a-zA-Z0-9% ]", " ", text.lower())
    ).strip()


def _get_client():
    global _embedding_client

    if _embedding_client is None:
        from google import genai

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is missing")

        _embedding_client = genai.Client(api_key=api_key)

    return _embedding_client


def _cloud_embeddings(corpus, query):
    global _document_cache

    from google.genai import types

    client = _get_client()

    # Reuse document embeddings until the FAQ content changes.
    if _document_cache.get("corpus") != tuple(corpus):
        response = client.models.embed_content(
            model="gemini-embedding-001",
            contents=corpus,
            config=types.EmbedContentConfig(
                task_type="RETRIEVAL_DOCUMENT",
                title="CampusIQ College FAQs"
            )
        )

        _document_cache = {
            "corpus": tuple(corpus),
            "vectors": [item.values for item in response.embeddings]
        }

    query_response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=query,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_QUERY"
        )
    )

    return (
        _document_cache["vectors"],
        query_response.embeddings[0].values
    )


def retrieve(query, limit=4):
    faqs = FAQ.query.all()

    if not faqs:
        return []

    corpus = [
        f"{f.question}. {f.answer}. {f.category}. {f.keywords or ''}"
        for f in faqs
    ]

    try:
        document_vectors, query_vector = _cloud_embeddings(
            corpus, query
        )

        scores = cosine_similarity(
            document_vectors,
            [query_vector]
        ).ravel()

    except Exception:
        # Lightweight fallback if cloud embeddings are unavailable.
        vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            stop_words="english"
        )

        matrix = vectorizer.fit_transform(corpus + [query])

        scores = cosine_similarity(
            matrix[-1],
            matrix[:-1]
        ).ravel()

    ranked = sorted(
        zip(faqs, scores.tolist()),
        key=lambda x: x[1],
        reverse=True
    )

    return [
        {
            "id": f.id,
            "question": f.question,
            "answer": f.answer,
            "category": f.category,
            "source": f.source,
            "score": float(score)
        }
        for f, score in ranked[:limit]
    ]
