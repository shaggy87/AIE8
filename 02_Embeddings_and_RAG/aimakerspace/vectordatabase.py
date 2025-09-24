import numpy as np
from collections import defaultdict
from typing import List, Tuple, Callable, Dict, Optional, Union
from aimakerspace.openai_utils.embedding import EmbeddingModel
import asyncio


def cosine_similarity(vector_a: np.array, vector_b: np.array) -> float:
    """Computes the cosine similarity between two vectors."""
    dot_product = np.dot(vector_a, vector_b)
    norm_a = np.linalg.norm(vector_a)
    norm_b = np.linalg.norm(vector_b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


def euclidean_distance(vector_a: np.array, vector_b: np.array) -> float:
    """Computes similarity based on Euclidean distance (higher = more similar)."""
    distance = np.linalg.norm(vector_a - vector_b)
    return 1 / (1 + distance)  # Convert distance to similarity


def manhattan_distance(vector_a: np.array, vector_b: np.array) -> float:
    """Computes similarity based on Manhattan distance (higher = more similar)."""
    distance = np.sum(np.abs(vector_a - vector_b))
    return 1 / (1 + distance)  # Convert distance to similarity


def dot_product_similarity(vector_a: np.array, vector_b: np.array) -> float:
    """Computes dot product similarity."""
    return np.dot(vector_a, vector_b)


class VectorDatabase:
    """Enhanced vector database with metadata support and multiple distance metrics."""

    def __init__(self, embedding_model: EmbeddingModel = None):
        self.vectors = {}  # Changed from defaultdict to regular dict
        self.metadata = {}  # Store metadata for each vector
        # Only create EmbeddingModel if not explicitly set to None
        if embedding_model is False:
            self.embedding_model = None
        else:
            self.embedding_model = embedding_model or EmbeddingModel()
        self.document_count = 0

    def insert(self, key: str, vector: np.array, metadata: Optional[Dict] = None) -> None:
        """Insert a vector with optional metadata."""
        self.vectors[key] = vector
        if metadata:
            self.metadata[key] = metadata
        self.document_count += 1

    def insert_with_metadata(self, key: str, vector: np.array, metadata: Dict) -> None:
        """Insert a vector with metadata (alias for clarity)."""
        self.insert(key, vector, metadata)

    def search(
        self,
        query_vector: np.array,
        k: int,
        distance_measure: Callable = cosine_similarity,
        filter_metadata: Optional[Dict] = None,
    ) -> List[Tuple[str, float]]:
        """Search for similar vectors with optional metadata filtering."""
        if k <= 0:
            raise ValueError("k must be a positive integer")

        # Filter vectors based on metadata if specified
        candidate_items = self.vectors.items()

        if filter_metadata:
            filtered_items = []
            for key, vector in candidate_items:
                if key in self.metadata:
                    metadata = self.metadata[key]
                    # Check if all filter criteria match
                    if all(metadata.get(filter_key) == filter_value
                          for filter_key, filter_value in filter_metadata.items()):
                        filtered_items.append((key, vector))
            candidate_items = filtered_items

        scores = [
            (key, distance_measure(query_vector, vector))
            for key, vector in candidate_items
        ]
        return sorted(scores, key=lambda x: x[1], reverse=True)[:k]

    def search_by_text(
        self,
        query_text: str,
        k: int,
        distance_measure: Callable = cosine_similarity,
        return_as_text: bool = False,
        filter_metadata: Optional[Dict] = None,
    ) -> Union[List[Tuple[str, float]], List[str]]:
        """Search using text query with optional metadata filtering."""
        query_vector = self.embedding_model.get_embedding(query_text)
        results = self.search(query_vector, k, distance_measure, filter_metadata)
        return [result[0] for result in results] if return_as_text else results

    def search_with_metadata(
        self,
        query_vector: np.array,
        k: int,
        distance_measure: Callable = cosine_similarity,
        filter_metadata: Optional[Dict] = None,
    ) -> List[Tuple[str, float, Dict]]:
        """Search and return results with metadata."""
        results = self.search(query_vector, k, distance_measure, filter_metadata)
        return [
            (key, score, self.metadata.get(key, {}))
            for key, score in results
        ]

    def search_by_text_with_metadata(
        self,
        query_text: str,
        k: int,
        distance_measure: Callable = cosine_similarity,
        filter_metadata: Optional[Dict] = None,
    ) -> List[Tuple[str, float, Dict]]:
        """Search by text and return results with metadata."""
        query_vector = self.embedding_model.get_embedding(query_text)
        return self.search_with_metadata(query_vector, k, distance_measure, filter_metadata)

    def retrieve_from_key(self, key: str) -> Optional[np.array]:
        """Retrieve vector by key."""
        return self.vectors.get(key, None)

    def retrieve_metadata(self, key: str) -> Optional[Dict]:
        """Retrieve metadata by key."""
        return self.metadata.get(key, None)

    def retrieve_with_metadata(self, key: str) -> Optional[Tuple[np.array, Dict]]:
        """Retrieve both vector and metadata by key."""
        vector = self.vectors.get(key)
        metadata = self.metadata.get(key, {})
        return (vector, metadata) if vector is not None else None

    async def abuild_from_list(
        self,
        list_of_text: List[str],
        metadata_list: Optional[List[Dict]] = None
    ) -> "VectorDatabase":
        """Build database from list of texts with optional metadata."""
        embeddings = await self.embedding_model.async_get_embeddings(list_of_text)

        for i, (text, embedding) in enumerate(zip(list_of_text, embeddings)):
            metadata = metadata_list[i] if metadata_list and i < len(metadata_list) else None
            self.insert(text, np.array(embedding), metadata)

        return self

    async def abuild_from_documents_and_metadata(
        self,
        documents: List[str],
        metadata_list: List[Dict]
    ) -> "VectorDatabase":
        """Build database from documents with corresponding metadata."""
        return await self.abuild_from_list(documents, metadata_list)

    def get_database_stats(self) -> Dict:
        """Get statistics about the vector database."""
        if not self.vectors:
            return {'total_vectors': 0, 'total_metadata': 0}

        vector_dims = len(next(iter(self.vectors.values())))

        # Analyze metadata if available
        metadata_keys = set()
        file_types = {}
        sources = set()

        for metadata in self.metadata.values():
            metadata_keys.update(metadata.keys())
            if 'file_type' in metadata:
                file_type = metadata['file_type']
                file_types[file_type] = file_types.get(file_type, 0) + 1
            if 'source' in metadata:
                sources.add(metadata['source'])

        return {
            'total_vectors': len(self.vectors),
            'total_metadata': len(self.metadata),
            'vector_dimensions': vector_dims,
            'unique_sources': len(sources),
            'file_types': file_types,
            'metadata_fields': list(metadata_keys)
        }


if __name__ == "__main__":
    # Example usage of enhanced VectorDatabase
    list_of_text = [
        "I like to eat broccoli and bananas.",
        "I ate a banana and spinach smoothie for breakfast.",
        "Chinchillas and kittens are cute.",
        "My sister adopted a kitten yesterday.",
        "Look at this cute hamster munching on a piece of broccoli.",
    ]

    # Example metadata
    metadata_list = [
        {'topic': 'food', 'sentiment': 'positive'},
        {'topic': 'food', 'sentiment': 'positive'},
        {'topic': 'animals', 'sentiment': 'positive'},
        {'topic': 'animals', 'sentiment': 'positive'},
        {'topic': 'animals', 'sentiment': 'positive'},
    ]

    vector_db = VectorDatabase()
    vector_db = asyncio.run(vector_db.abuild_from_list(list_of_text, metadata_list))
    k = 2

    # Basic search
    searched_vector = vector_db.search_by_text("I think fruit is awesome!", k=k)
    print(f"Closest {k} vector(s):", searched_vector)

    # Search with metadata
    results_with_metadata = vector_db.search_by_text_with_metadata(
        "I think fruit is awesome!", k=k
    )
    print(f"Results with metadata:", results_with_metadata)

    # Filtered search
    animal_results = vector_db.search_by_text(
        "cute pets", k=k, filter_metadata={'topic': 'animals'}
    )
    print(f"Animal-related results:", animal_results)

    # Database stats
    stats = vector_db.get_database_stats()
    print(f"Database stats:", stats)

    # Test different distance metrics
    euclidean_results = vector_db.search_by_text(
        "I think fruit is awesome!", k=k, distance_measure=euclidean_distance
    )
    print(f"Euclidean distance results:", euclidean_results)
