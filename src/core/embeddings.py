from sentence_transformers import SentenceTransformer
import hashlib
import threading


class EmbeddingManager:
    """Manages embeddings generation with caching to avoid redundant computations."""

    def __init__(self, model_name: str = None, cache_dir: str = None):
        self.model_name = model_name or "BAAI/bge-m3"
        self.cache_dir = cache_dir or "./model_cache"
        self.model = SentenceTransformer(self.model_name, cache_folder=self.cache_dir)
        self.cache = {}
        self.lock = threading.Lock()

    def _get_cache_key(self, text: str) -> str:
        """Generate a cache key for a given text using MD5."""
        return hashlib.md5(text.encode('utf-8')).hexdigest()

    def encode(self, texts, batch_size: int = 32, show_progress_bar: bool = False, normalize_embeddings: bool = True):
        """Encode one or more texts into embeddings with caching.

        If a text has been encoded before, return the cached embedding.
        
        Args:
            texts (str or List[str]): The input text(s) to encode.
            batch_size (int): Batch size for encoding (if needed).
            show_progress_bar (bool): Whether to show a progress bar.
            normalize_embeddings (bool): Whether to normalize embeddings.

        Returns:
            np.ndarray or List[np.ndarray]: The embedding(s) for the input text(s).
        """
        single_input = False
        if isinstance(texts, str):
            texts = [texts]
            single_input = True
        
        # Prepare list for embeddings and track indexes to encode
        embeddings = [None] * len(texts)
        texts_to_encode = []
        index_map = {}
        
        with self.lock:
            for i, text in enumerate(texts):
                key = self._get_cache_key(text)
                if key in self.cache:
                    embeddings[i] = self.cache[key]
                else:
                    index_map[i] = key
                    texts_to_encode.append(text)

        # Only encode texts that were not cached
        if texts_to_encode:
            new_embeddings = self.model.encode(
                texts_to_encode,
                batch_size=batch_size,
                show_progress_bar=show_progress_bar,
                normalize_embeddings=normalize_embeddings
            )
            with self.lock:
                j = 0
                for i in index_map:
                    key = index_map[i]
                    self.cache[key] = new_embeddings[j]
                    embeddings[i] = new_embeddings[j]
                    j += 1

        return embeddings[0] if single_input else embeddings
