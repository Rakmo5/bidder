import math
import re
from typing import List, Dict
from app.ai_engine.chunking.base_chunker import DocumentChunk
from app.ai_engine.vector_store.base_store import BaseVectorStore, RetrievalResult
from app.ai_engine.config import ai_config

class InMemoryBM25HybridStore(BaseVectorStore):
    """
    In-Memory Hybrid BM25 & Keyword Inverted Index Store.
    Implements the Okapi BM25 probabilistic ranking model with exact phrase boosting.
    """

    def __init__(self):
        self._store: Dict[str, List[DocumentChunk]] = {}
        self._idf_vocab: Dict[str, Dict[str, float]] = {}

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        return [w.lower() for w in re.findall(r'\b[a-zA-Z0-9_\-\.]{2,}\b', text)]

    def add_chunks(self, document_name: str, chunks: List[DocumentChunk]):
        self._store[document_name] = chunks
        N = len(chunks)
        if N == 0:
            return

        # Calculate Document Frequencies
        df: Dict[str, int] = {}
        for c in chunks:
            tokens = set(self._tokenize(c.text))
            for t in tokens:
                df[t] = df.get(t, 0) + 1

        # Calculate Inverse Document Frequency (IDF)
        idf: Dict[str, float] = {}
        for t, freq in df.items():
            idf[t] = math.log(1 + (N - freq + 0.5) / (freq + 0.5))
        self._idf_vocab[document_name] = idf

    def get_chunks(self, document_name: str) -> List[DocumentChunk]:
        return self._store.get(document_name, [])

    def get_all_indexed_docs(self) -> List[str]:
        return list(self._store.keys())

    def search(self, document_name: str, query: str, top_k: int = 3) -> List[RetrievalResult]:
        chunks = self._store.get(document_name, [])
        if not chunks:
            return []

        query_tokens = self._tokenize(query)
        idf_dict = self._idf_vocab.get(document_name, {})
        avg_dl = sum(c.tokens_count for c in chunks) / max(len(chunks), 1)
        k1 = ai_config.bm25_k1
        b = ai_config.bm25_b

        results: List[RetrievalResult] = []

        for c in chunks:
            chunk_tokens = self._tokenize(c.text)
            chunk_len = c.tokens_count
            bm25_score = 0.0

            for qt in query_tokens:
                if qt in chunk_tokens:
                    f = chunk_tokens.count(qt)
                    idf = idf_dict.get(qt, 1.0)
                    numerator = f * (k1 + 1)
                    denominator = f + k1 * (1 - b + b * (chunk_len / avg_dl))
                    bm25_score += idf * (numerator / denominator)

            # Domain keyword boosting for statutory procurement terms
            keywords = ["turnover", "udin", "cbr", "bitumen", "sensor", "paver", "iso", "dlp", "solvency", "bg", "emd"]
            exact_boost = 1.4 if any(kw in c.text.lower() for kw in keywords if kw in query.lower()) else 1.0
            final_score = round(bm25_score * exact_boost, 4)

            results.append(RetrievalResult(
                chunk=c,
                similarity_score=final_score,
                retrieval_mode="hybrid_bm25_semantic"
            ))

        results.sort(key=lambda x: x.similarity_score, reverse=True)
        return results[:top_k]
