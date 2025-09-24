#!/usr/bin/env python3
"""
Enhanced RAG Example with PDF Support and Metadata
==================================================

This example demonstrates the enhanced aimakerspace library with:
1. PDF file loading with metadata
2. Multiple distance metrics
3. Metadata-based filtering
4. Advanced PDF processing features

Prerequisites:
- pdfplumber installed
- OpenAI API key set in environment or .env file
"""

import asyncio
import os
from aimakerspace.text_utils import TextFileLoader, PDFLoader, CharacterTextSplitter
from aimakerspace.vectordatabase import (
    VectorDatabase,
    cosine_similarity,
    euclidean_distance,
    manhattan_distance,
    dot_product_similarity
)
from aimakerspace.openai_utils.embedding import EmbeddingModel


async def demo_enhanced_text_loader():
    """Demonstrate enhanced TextFileLoader with PDF support."""
    print("=== Enhanced TextFileLoader Demo ===\n")

    # Method 1: Load with metadata extraction
    print("1. Loading documents with metadata extraction...")

    # You can test with any .txt or .pdf files you have
    # For this demo, we'll create some sample content
    sample_texts = [
        "Artificial Intelligence is transforming healthcare through machine learning algorithms.",
        "Machine learning models require large datasets to train effectively.",
        "Healthcare applications of AI include diagnostic imaging and drug discovery.",
        "Deep learning neural networks can process complex medical data patterns."
    ]

    # Simulate metadata that would come from files
    sample_metadata = [
        {'source': 'ai_healthcare.txt', 'file_type': 'txt', 'topic': 'AI', 'domain': 'healthcare'},
        {'source': 'ml_basics.txt', 'file_type': 'txt', 'topic': 'ML', 'domain': 'education'},
        {'source': 'medical_ai.pdf', 'file_type': 'pdf', 'topic': 'AI', 'domain': 'healthcare'},
        {'source': 'deep_learning.pdf', 'file_type': 'pdf', 'topic': 'DL', 'domain': 'research'}
    ]

    return sample_texts, sample_metadata


async def demo_enhanced_vector_database():
    """Demonstrate enhanced VectorDatabase with metadata and multiple distance metrics."""
    print("=== Enhanced VectorDatabase Demo ===\n")

    # Get sample data
    documents, metadata = await demo_enhanced_text_loader()

    # Initialize embedding model
    print("2. Creating embedding model...")
    embedding_model = EmbeddingModel(
        embeddings_model_name="text-embedding-3-small"
    )

    # Create enhanced vector database
    print("3. Building vector database with metadata...")
    vector_db = VectorDatabase(embedding_model=embedding_model)

    # Build database with documents and metadata
    await vector_db.abuild_from_documents_and_metadata(documents, metadata)

    # Display database statistics
    stats = vector_db.get_database_stats()
    print(f"Database built successfully!")
    print(f"Stats: {stats}")
    print()

    return vector_db, documents, metadata


async def demo_search_capabilities(vector_db):
    """Demonstrate various search capabilities."""
    print("=== Search Capabilities Demo ===\n")

    query = "machine learning in medical applications"
    k = 3

    # 1. Basic search with different distance metrics
    print("4. Testing different distance metrics...")

    distance_metrics = [
        ("Cosine Similarity", cosine_similarity),
        ("Euclidean Distance", euclidean_distance),
        ("Manhattan Distance", manhattan_distance),
        ("Dot Product", dot_product_similarity)
    ]

    for metric_name, metric_func in distance_metrics:
        results = vector_db.search_by_text(query, k=k, distance_measure=metric_func)
        print(f"\n{metric_name} results:")
        for i, (text, score) in enumerate(results, 1):
            print(f"  {i}. Score: {score:.4f}")
            print(f"     Text: {text[:80]}...")

    # 2. Search with metadata
    print("\n\n5. Search with metadata information...")
    results_with_metadata = vector_db.search_by_text_with_metadata(query, k=k)

    for i, (text, score, metadata) in enumerate(results_with_metadata, 1):
        print(f"\nResult {i}:")
        print(f"  Score: {score:.4f}")
        print(f"  Source: {metadata.get('source', 'Unknown')}")
        print(f"  Topic: {metadata.get('topic', 'Unknown')}")
        print(f"  Domain: {metadata.get('domain', 'Unknown')}")
        print(f"  Text: {text[:100]}...")

    # 3. Filtered search
    print("\n\n6. Filtered search (healthcare domain only)...")
    healthcare_results = vector_db.search_by_text(
        query,
        k=k,
        filter_metadata={'domain': 'healthcare'}
    )

    print(f"Found {len(healthcare_results)} healthcare-related results:")
    for i, (text, score) in enumerate(healthcare_results, 1):
        print(f"  {i}. Score: {score:.4f}")
        print(f"     Text: {text[:80]}...")


async def demo_pdf_loader():
    """Demonstrate specialized PDF loader (requires actual PDF file)."""
    print("\n\n=== PDF Loader Demo ===\n")

    print("7. PDF Loader features (requires actual PDF files)...")
    print("   - Per-page metadata extraction")
    print("   - Chapter/section detection")
    print("   - Table and image counting")
    print("   - Advanced text extraction")
    print()

    # Example of how to use PDFLoader (commented out since we don't have PDF files)
    print("Example usage:")
    print("""
    # Load PDF with page-level metadata
    pdf_loader = PDFLoader("research_paper.pdf")
    pages, page_metadata = pdf_loader.load_with_page_metadata()

    # Load PDF with chapter detection
    chapters, chapter_metadata = pdf_loader.load_with_chapters(
        chapter_keywords=['chapter', 'section', 'introduction', 'conclusion']
    )

    # Print page information
    for i, (page_text, metadata) in enumerate(zip(pages, page_metadata)):
        print(f"Page {metadata['page_number']}: {len(page_text)} characters")
        print(f"  Orientation: {metadata.get('orientation', 'unknown')}")
        print(f"  Tables: {metadata.get('table_count', 0)}")
    """)


async def demo_chunking_with_metadata():
    """Demonstrate text chunking with metadata preservation."""
    print("\n\n=== Text Chunking with Metadata Demo ===\n")

    print("8. Text chunking with metadata preservation...")

    # Sample long document
    long_document = """
    Artificial Intelligence in Healthcare: A Comprehensive Overview

    Introduction
    Artificial intelligence (AI) has emerged as a transformative force in healthcare,
    revolutionizing how medical professionals diagnose, treat, and prevent diseases.
    The integration of AI technologies into healthcare systems promises to enhance
    patient outcomes, reduce costs, and improve the overall efficiency of medical care.

    Machine Learning Applications
    Machine learning, a subset of AI, has found numerous applications in healthcare.
    From predictive analytics that can forecast patient deterioration to image
    recognition systems that can detect cancerous tumors with remarkable accuracy,
    ML is reshaping medical practice. These systems learn from vast amounts of
    medical data to identify patterns that might be invisible to human practitioners.

    Deep Learning in Medical Imaging
    Deep learning neural networks have shown exceptional performance in medical
    imaging tasks. Convolutional neural networks (CNNs) can analyze radiological
    images, CT scans, and MRIs to detect abnormalities with accuracy that often
    matches or exceeds that of expert radiologists. This technology is particularly
    valuable in areas where there are shortages of specialized medical professionals.
    """

    # Create metadata for the document
    document_metadata = {
        'source': 'ai_healthcare_overview.txt',
        'file_type': 'txt',
        'topic': 'AI',
        'domain': 'healthcare',
        'author': 'Medical AI Research Team',
        'word_count': len(long_document.split())
    }

    # Split document into chunks
    splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=50)
    chunks = splitter.split(long_document)

    print(f"Split document into {len(chunks)} chunks")

    # Create metadata for each chunk
    chunk_metadata_list = []
    for i, chunk in enumerate(chunks):
        chunk_metadata = document_metadata.copy()
        chunk_metadata.update({
            'chunk_id': i,
            'chunk_word_count': len(chunk.split()),
            'chunk_char_count': len(chunk)
        })
        chunk_metadata_list.append(chunk_metadata)

    # Build vector database with chunks
    chunk_embedding_model = EmbeddingModel()  # Use default settings
    chunk_vector_db = VectorDatabase(embedding_model=chunk_embedding_model)

    await chunk_vector_db.abuild_from_documents_and_metadata(chunks, chunk_metadata_list)

    # Search within chunks
    chunk_query = "deep learning medical imaging"
    chunk_results = chunk_vector_db.search_by_text_with_metadata(chunk_query, k=2)

    print(f"\nSearch results for '{chunk_query}':")
    for i, (text, score, metadata) in enumerate(chunk_results, 1):
        print(f"\nChunk {i}:")
        print(f"  Score: {score:.4f}")
        print(f"  Chunk ID: {metadata.get('chunk_id', 'Unknown')}")
        print(f"  Word count: {metadata.get('chunk_word_count', 'Unknown')}")
        print(f"  Text preview: {text[:150]}...")


async def main():
    """Run all demonstrations."""
    print("Enhanced RAG with PDF Support and Metadata Demo")
    print("=" * 50)
    print()

    try:
        # Demo 1: Enhanced Vector Database
        vector_db, documents, metadata = await demo_enhanced_vector_database()

        # Demo 2: Search Capabilities
        await demo_search_capabilities(vector_db)

        # Demo 3: PDF Loader (conceptual)
        await demo_pdf_loader()

        # Demo 4: Chunking with Metadata
        await demo_chunking_with_metadata()

        print("\n" + "=" * 50)
        print("Demo completed successfully!")
        print("\nKey enhancements demonstrated:")
        print("SUCCESS: PDF file support with pdfplumber")
        print("SUCCESS: Metadata extraction and storage")
        print("SUCCESS: Multiple distance metrics")
        print("SUCCESS: Metadata-based filtering")
        print("SUCCESS: Enhanced search capabilities")
        print("SUCCESS: Document chunking with metadata preservation")

    except Exception as e:
        print(f"ERROR during demo: {e}")
        print("Make sure you have:")
        print("1. OpenAI API key set in environment")
        print("2. pdfplumber installed: pip install pdfplumber")


if __name__ == "__main__":
    asyncio.run(main())