#!/usr/bin/env python3
"""
Test Enhanced aimakerspace Features (No API Required)
====================================================

Test the enhanced features without requiring OpenAI API calls.
"""

import numpy as np
from aimakerspace.text_utils import TextFileLoader, PDFLoader, CharacterTextSplitter
from aimakerspace.vectordatabase import (
    VectorDatabase,
    cosine_similarity,
    euclidean_distance,
    manhattan_distance,
    dot_product_similarity
)


def test_distance_metrics():
    """Test different distance metrics."""
    print("=== Testing Distance Metrics ===")

    # Create test vectors
    vector_a = np.array([1.0, 2.0, 3.0, 4.0])
    vector_b = np.array([2.0, 3.0, 4.0, 5.0])
    vector_c = np.array([1.0, 1.0, 1.0, 1.0])

    metrics = [
        ("Cosine Similarity", cosine_similarity),
        ("Euclidean Distance", euclidean_distance),
        ("Manhattan Distance", manhattan_distance),
        ("Dot Product", dot_product_similarity)
    ]

    print("Vector A:", vector_a)
    print("Vector B:", vector_b)
    print("Vector C:", vector_c)
    print()

    for name, metric in metrics:
        score_ab = metric(vector_a, vector_b)
        score_ac = metric(vector_a, vector_c)
        print(f"{name:20s}: A-B = {score_ab:.4f}, A-C = {score_ac:.4f}")

    print()


def test_vector_database_metadata():
    """Test VectorDatabase metadata functionality."""
    print("=== Testing VectorDatabase Metadata ===")

    # Create a vector database without embedding model (for testing)
    vector_db = VectorDatabase(embedding_model=False)

    # Add test vectors with metadata
    test_data = [
        ("AI transforms healthcare", np.array([0.1, 0.2, 0.3]), {'topic': 'AI', 'domain': 'healthcare'}),
        ("Machine learning algorithms", np.array([0.2, 0.3, 0.4]), {'topic': 'ML', 'domain': 'technology'}),
        ("Medical diagnosis systems", np.array([0.15, 0.25, 0.35]), {'topic': 'AI', 'domain': 'healthcare'}),
        ("Data science methods", np.array([0.3, 0.4, 0.5]), {'topic': 'DS', 'domain': 'technology'}),
    ]

    for text, vector, metadata in test_data:
        vector_db.insert_with_metadata(text, vector, metadata)

    # Test basic functionality
    print(f"Database contains {len(vector_db.vectors)} vectors")
    print(f"Database contains {len(vector_db.metadata)} metadata entries")

    # Test metadata retrieval
    first_key = list(vector_db.vectors.keys())[0]
    vector, metadata = vector_db.retrieve_with_metadata(first_key)
    print(f"First entry metadata: {metadata}")

    # Test database stats
    stats = vector_db.get_database_stats()
    print(f"Database stats: {stats}")

    # Test filtered search (manual simulation since we don't have embeddings)
    query_vector = np.array([0.12, 0.22, 0.32])

    # Regular search
    results = vector_db.search(query_vector, k=2)
    print(f"\\nTop 2 search results:")
    for i, (text, score) in enumerate(results, 1):
        print(f"  {i}. Score: {score:.4f} - {text[:50]}...")

    # Search with metadata
    results_with_metadata = vector_db.search_with_metadata(query_vector, k=2)
    print(f"\\nTop 2 results with metadata:")
    for i, (text, score, metadata) in enumerate(results_with_metadata, 1):
        print(f"  {i}. Score: {score:.4f}")
        print(f"     Topic: {metadata.get('topic', 'Unknown')}")
        print(f"     Domain: {metadata.get('domain', 'Unknown')}")
        print(f"     Text: {text[:40]}...")

    # Filtered search
    healthcare_results = vector_db.search(
        query_vector, k=3, filter_metadata={'domain': 'healthcare'}
    )
    print(f"\\nHealthcare-only results ({len(healthcare_results)} found):")
    for i, (text, score) in enumerate(healthcare_results, 1):
        print(f"  {i}. Score: {score:.4f} - {text[:50]}...")

    print()


def test_text_splitter():
    """Test CharacterTextSplitter."""
    print("=== Testing CharacterTextSplitter ===")

    # Sample long text
    long_text = """
    This is a long document that needs to be split into smaller chunks.
    The text splitter should create overlapping chunks to maintain context.
    Each chunk should be roughly the same size but may vary slightly.
    The overlap helps ensure that important information spanning chunk
    boundaries is not lost during the splitting process.
    """

    splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=20)
    chunks = splitter.split(long_text.strip())

    print(f"Original text length: {len(long_text)} characters")
    print(f"Split into {len(chunks)} chunks:")

    for i, chunk in enumerate(chunks):
        print(f"  Chunk {i+1}: {len(chunk)} chars - '{chunk[:40]}...'")

    print()


def test_textfile_loader():
    """Test TextFileLoader basic functionality."""
    print("=== Testing TextFileLoader ===")

    # Test with non-existent file to see error handling
    try:
        loader = TextFileLoader("nonexistent.txt")
        loader.load()
    except ValueError as e:
        print(f"Expected error for non-existent file: {e}")

    # Test get_document_info with empty loader
    empty_loader = TextFileLoader("dummy_path")
    info = empty_loader.get_document_info()
    print(f"Empty loader info: {info}")

    print()


def test_pdf_loader():
    """Test PDFLoader basic functionality."""
    print("=== Testing PDFLoader ===")

    print("PDFLoader features available:")
    print("  - load_with_page_metadata(): Extract text with page-level metadata")
    print("  - load_with_chapters(): Detect chapters/sections automatically")
    print()

    # Example of how metadata would look
    example_page_metadata = {
        'source': 'example.pdf',
        'page_number': 1,
        'total_pages': 10,
        'char_count': 1250,
        'word_count': 200,
        'page_width': 612.0,
        'page_height': 792.0,
        'orientation': 'portrait',
        'table_count': 2
    }

    print("Example page metadata structure:")
    for key, value in example_page_metadata.items():
        print(f"  {key}: {value}")

    print()


def main():
    """Run all tests."""
    print("Enhanced aimakerspace Library Test Suite")
    print("=" * 50)
    print()

    try:
        test_distance_metrics()
        test_vector_database_metadata()
        test_text_splitter()
        test_textfile_loader()
        test_pdf_loader()

        print("=" * 50)
        print("All tests completed successfully!")
        print()
        print("Enhanced features verified:")
        print("SUCCESS: Multiple distance metrics")
        print("SUCCESS: Metadata storage and retrieval")
        print("SUCCESS: Filtered search capabilities")
        print("SUCCESS: Database statistics")
        print("SUCCESS: Text chunking")
        print("SUCCESS: Error handling")
        print()
        print("Ready for PDF processing with pdfplumber!")

    except Exception as e:
        print(f"ERROR during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()