#!/usr/bin/env python3
"""
YouTube RAG Integration Example
==============================

This example demonstrates how to use YouTube videos as a data source for RAG applications.
Features include transcript extraction, timestamp preservation, and video metadata integration.

Requirements:
- youtube-transcript-api
- pytube
- OpenAI API key (optional, for embeddings)
"""

import asyncio
from aimakerspace.text_utils import TextFileLoader, YouTubeLoader, CharacterTextSplitter
from aimakerspace.vectordatabase import VectorDatabase


def test_youtube_url_detection():
    """Test YouTube URL detection functionality."""
    print("=== Testing YouTube URL Detection ===\n")

    test_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtu.be/dQw4w9WgXcQ",
        "https://youtube.com/watch?v=dQw4w9WgXcQ",
        "https://m.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://www.youtube.com/embed/dQw4w9WgXcQ",
        "https://example.com/not-youtube",
        "not-a-url-at-all"
    ]

    for url in test_urls:
        is_youtube = YouTubeLoader.is_youtube_url(url)
        print(f"✓ {url[:50]:<50} {'YouTube' if is_youtube else 'Not YouTube'}")

    print()


def test_video_id_extraction():
    """Test video ID extraction from various YouTube URL formats."""
    print("=== Testing Video ID Extraction ===\n")

    test_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtu.be/dQw4w9WgXcQ",
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=10s",
        "https://youtube.com/embed/dQw4w9WgXcQ",
    ]

    for url in test_urls:
        try:
            loader = YouTubeLoader(url)
            video_id = loader.video_id
            print(f"✓ URL: {url}")
            print(f"  Video ID: {video_id}")
        except Exception as e:
            print(f"✗ URL: {url}")
            print(f"  Error: {e}")
        print()


def demo_youtube_transcript_loading():
    """Demonstrate YouTube transcript loading with a real video."""
    print("=== YouTube Transcript Loading Demo ===\n")

    # Using a known educational video with transcripts
    # This is a TED Talk about AI (should have transcripts available)
    test_video_url = "https://www.youtube.com/watch?v=8FHBh_OmdsM"  # Example TED Talk

    print("Note: This demo uses a real YouTube video.")
    print("If the video doesn't have transcripts or is unavailable, it will show an error.")
    print(f"Testing with: {test_video_url}")
    print()

    try:
        # Test 1: Basic transcript loading
        print("1. Basic transcript loading...")
        youtube_loader = YouTubeLoader(test_video_url)
        transcript, metadata = youtube_loader.load_transcript()

        print(f"✓ Successfully loaded transcript!")
        print(f"  Video Title: {metadata.get('title', 'Unknown')}")
        print(f"  Author: {metadata.get('author', 'Unknown')}")
        print(f"  Length: {metadata.get('length_seconds', 0)} seconds")
        print(f"  Transcript Language: {metadata.get('transcript_language', 'Unknown')}")
        print(f"  Word Count: {metadata.get('word_count', 0)}")
        print(f"  First 200 characters: {transcript[:200]}...")
        print()

        # Test 2: Time-chunked loading
        print("2. Time-chunked transcript loading (5-minute chunks)...")
        chunks, chunk_metadata = youtube_loader.load_transcript_with_timestamps(
            chunk_by_time=True,
            chunk_duration=300  # 5 minutes
        )

        print(f"✓ Split into {len(chunks)} time-based chunks:")
        for i, (chunk, meta) in enumerate(zip(chunks[:3], chunk_metadata[:3])):  # Show first 3
            start_time = meta.get('chunk_start_time', 0)
            end_time = meta.get('chunk_end_time', 0)
            print(f"  Chunk {i+1}: {start_time:.0f}s - {end_time:.0f}s ({len(chunk)} chars)")
            print(f"    Preview: {chunk[:100]}...")
        print()

        # Test 3: Integration with TextFileLoader
        print("3. Integration with TextFileLoader...")
        text_loader = TextFileLoader(test_video_url, extract_metadata=True)
        documents, metadata_list = text_loader.load_documents_with_metadata()

        print(f"✓ Loaded {len(documents)} documents via TextFileLoader")
        if metadata_list:
            meta = metadata_list[0]
            print(f"  File Type: {meta.get('file_type', 'Unknown')}")
            print(f"  Video Title: {meta.get('title', 'Unknown')}")
            print(f"  Source: {meta.get('source', 'Unknown')}")
        print()

        return transcript, metadata, chunks, chunk_metadata

    except Exception as e:
        print(f"✗ Error loading transcript: {e}")
        print("This might happen if:")
        print("- The video doesn't have auto-generated or manual transcripts")
        print("- The video is private or restricted")
        print("- Network connectivity issues")
        print("- The video ID is invalid")
        return None, None, None, None


async def demo_youtube_rag_pipeline():
    """Demonstrate a complete RAG pipeline with YouTube content."""
    print("=== YouTube RAG Pipeline Demo ===\n")

    # Test URLs - using educational content that likely has transcripts
    educational_videos = [
        "https://www.youtube.com/watch?v=aircAruvnKk",  # 3Blue1Brown - Neural Networks
        "https://www.youtube.com/watch?v=8FHBh_OmdsM",  # TED Talk example
    ]

    print("Building a knowledge base from educational YouTube videos...")
    print("Note: This requires videos with available transcripts.")
    print()

    all_documents = []
    all_metadata = []

    # Load transcripts from multiple videos
    for i, url in enumerate(educational_videos):
        print(f"Processing video {i+1}/{len(educational_videos)}...")
        try:
            # Use TextFileLoader for consistent interface
            loader = TextFileLoader(url, extract_metadata=True)
            docs, meta = loader.load_documents_with_metadata()

            if docs:
                all_documents.extend(docs)
                all_metadata.extend(meta)
                print(f"✓ Successfully loaded: {meta[0].get('title', 'Unknown Title')}")
            else:
                print(f"✗ No content loaded from {url}")

        except Exception as e:
            print(f"✗ Error loading {url}: {e}")

    if not all_documents:
        print("❌ No documents loaded. Cannot proceed with RAG demo.")
        print("This demo requires videos with available transcripts.")
        return

    print(f"\n✓ Total documents loaded: {len(all_documents)}")
    print(f"✓ Total metadata entries: {len(all_metadata)}")

    # Split into smaller chunks for better retrieval
    print("\nSplitting documents into chunks...")
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    chunked_docs = []
    chunked_metadata = []

    for doc, meta in zip(all_documents, all_metadata):
        chunks = splitter.split(doc)
        for i, chunk in enumerate(chunks):
            chunked_docs.append(chunk)

            # Create metadata for each chunk
            chunk_meta = meta.copy()
            chunk_meta.update({
                'chunk_id': i,
                'total_chunks': len(chunks),
                'chunk_char_count': len(chunk),
                'chunk_word_count': len(chunk.split())
            })
            chunked_metadata.append(chunk_meta)

    print(f"✓ Created {len(chunked_docs)} chunks from {len(all_documents)} videos")

    # This is where you would build the vector database if you have an API key
    print("\nRAG Pipeline Ready!")
    print("To complete the pipeline with embeddings, you would:")
    print("1. Set your OpenAI API key")
    print("2. Create VectorDatabase with embedding model")
    print("3. Build embeddings from chunked documents")
    print("4. Query the knowledge base")

    # Return data for potential use
    return chunked_docs, chunked_metadata


def demo_youtube_features():
    """Demonstrate various YouTube-specific features."""
    print("=== YouTube-Specific Features Demo ===\n")

    test_url = "https://www.youtube.com/watch?v=aircAruvnKk"  # 3Blue1Brown video

    try:
        # Feature 1: Available languages
        print("1. Checking available transcript languages...")
        try:
            languages = YouTubeLoader.get_available_languages(test_url)
            print(f"✓ Available languages: {languages}")
        except Exception as e:
            print(f"✗ Could not get languages: {e}")

        # Feature 2: Custom language preference
        print("\n2. Loading transcript with language preference...")
        try:
            loader = YouTubeLoader(test_url)
            transcript, metadata = loader.load_transcript(languages=['en', 'en-US'])
            print(f"✓ Loaded transcript in: {metadata.get('transcript_language', 'Unknown')}")
        except Exception as e:
            print(f"✗ Error with language preference: {e}")

        # Feature 3: Timestamp information
        print("\n3. Examining timestamp information...")
        try:
            loader = YouTubeLoader(test_url)
            transcript, metadata = loader.load_transcript()

            timestamps = metadata.get('timestamps', [])
            if timestamps:
                print(f"✓ Found {len(timestamps)} timestamp entries")
                print("First few entries:")
                for i, entry in enumerate(timestamps[:3]):
                    start = entry.get('start', 0)
                    text = entry.get('text', '')
                    print(f"  {start:.1f}s: {text[:50]}...")
            else:
                print("✗ No timestamp information available")

        except Exception as e:
            print(f"✗ Error accessing timestamps: {e}")

    except Exception as e:
        print(f"✗ General error in demo: {e}")


def main():
    """Run all YouTube integration demos."""
    print("YouTube RAG Integration Demonstration")
    print("=" * 50)
    print()

    # Test basic functionality (no network required)
    test_youtube_url_detection()
    test_video_id_extraction()

    # Test real YouTube functionality (requires network and valid videos)
    print("=" * 50)
    print("NETWORK-DEPENDENT TESTS")
    print("=" * 50)
    print("The following tests require internet access and valid YouTube videos.")
    print("They may fail if videos are unavailable or don't have transcripts.")
    print()

    # Basic transcript loading
    transcript_result = demo_youtube_transcript_loading()

    # Advanced features
    demo_youtube_features()

    # RAG pipeline demo
    # asyncio.run(demo_youtube_rag_pipeline())

    print("\n" + "=" * 50)
    print("YouTube Integration Demo Complete!")
    print()
    print("Key capabilities demonstrated:")
    print("✓ YouTube URL detection and video ID extraction")
    print("✓ Transcript loading with metadata")
    print("✓ Time-based chunking with timestamps")
    print("✓ Integration with TextFileLoader")
    print("✓ Multi-language transcript support")
    print("✓ Ready for RAG pipeline integration")


if __name__ == "__main__":
    main()