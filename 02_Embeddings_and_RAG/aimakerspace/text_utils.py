import os
import re
from typing import List, Dict, Tuple, Optional
from urllib.parse import urlparse, parse_qs
import pdfplumber

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    from pytube import YouTube
    YOUTUBE_AVAILABLE = True
except ImportError:
    YOUTUBE_AVAILABLE = False

class TextFileLoader:
    """Enhanced file loader supporting .txt, .pdf files, and YouTube URLs with metadata."""

    def __init__(self,
                 path: str,
                 encoding: str = "utf-8",
                 include_page_numbers: bool = True,
                 extract_metadata: bool = False):
        self.documents = []
        self.metadata = []  # Store metadata for each document
        self.path = path
        self.encoding = encoding
        self.include_page_numbers = include_page_numbers
        self.extract_metadata = extract_metadata
        self.is_youtube_url = YouTubeLoader.is_youtube_url(path) if YOUTUBE_AVAILABLE else False

    def load(self):
        """Load documents from file, directory, or YouTube URL."""
        if self.is_youtube_url:
            self.load_youtube()
        elif os.path.isdir(self.path):
            self.load_directory()
        elif os.path.isfile(self.path):
            if self.path.endswith(".txt"):
                self.load_file()
            elif self.path.endswith(".pdf"):
                self.load_pdf()
            else:
                raise ValueError(
                    "Provided path must be a directory, .txt file, .pdf file, or YouTube URL."
                )
        else:
            raise ValueError("Provided path does not exist or is not a valid YouTube URL.")

    def load_file(self):
        """Load a single text file."""
        try:
            with open(self.path, "r", encoding=self.encoding) as f:
                content = f.read()
                self.documents.append(content)

                if self.extract_metadata:
                    metadata = {
                        'source': self.path,
                        'file_type': 'txt',
                        'char_count': len(content),
                        'word_count': len(content.split()),
                        'file_size': os.path.getsize(self.path)
                    }
                    self.metadata.append(metadata)

        except Exception as e:
            raise ValueError(f"Error reading text file {self.path}: {str(e)}")

    def load_pdf(self):
        """Load a PDF file with enhanced text extraction."""
        try:
            text = ""
            total_pages = 0
            total_chars = 0

            with pdfplumber.open(self.path) as pdf:
                total_pages = len(pdf.pages)

                for page_num, page in enumerate(pdf.pages, 1):
                    page_text = page.extract_text()
                    if page_text and page_text.strip():
                        if self.include_page_numbers:
                            formatted_text = f"[Page {page_num}]\n{page_text.strip()}\n\n"
                        else:
                            formatted_text = f"{page_text.strip()}\n\n"

                        text += formatted_text
                        total_chars += len(page_text)

            if text.strip():  # Only add if we extracted text
                self.documents.append(text)

                if self.extract_metadata:
                    metadata = {
                        'source': self.path,
                        'file_type': 'pdf',
                        'total_pages': total_pages,
                        'char_count': total_chars,
                        'word_count': len(text.split()),
                        'file_size': os.path.getsize(self.path),
                        'pages_with_text': text.count('[Page ') if self.include_page_numbers else total_pages
                    }
                    self.metadata.append(metadata)
            else:
                print(f"Warning: No text extracted from {self.path}")
                if self.extract_metadata:
                    self.metadata.append({
                        'source': self.path,
                        'file_type': 'pdf',
                        'total_pages': total_pages,
                        'char_count': 0,
                        'word_count': 0,
                        'error': 'No text extracted'
                    })

        except Exception as e:
            error_msg = f"Error reading PDF file {self.path}: {str(e)}"
            print(f"Warning: {error_msg}")
            if self.extract_metadata:
                self.metadata.append({
                    'source': self.path,
                    'file_type': 'pdf',
                    'error': str(e)
                })
            # Don't raise exception, just continue with other files

    def load_youtube(self):
        """Load transcript from YouTube URL."""
        if not YOUTUBE_AVAILABLE:
            raise ImportError(
                "YouTube functionality requires youtube-transcript-api and pytube. "
                "Install with: pip install youtube-transcript-api pytube"
            )

        try:
            youtube_loader = YouTubeLoader(self.path)
            transcript_text, metadata = youtube_loader.load_transcript()

            self.documents.append(transcript_text)

            if self.extract_metadata:
                # Add file_type for consistency with other loaders
                metadata['file_type'] = 'youtube'
                self.metadata.append(metadata)

        except Exception as e:
            error_msg = f"Error loading YouTube transcript from {self.path}: {str(e)}"
            print(f"Warning: {error_msg}")
            if self.extract_metadata:
                self.metadata.append({
                    'source': self.path,
                    'file_type': 'youtube',
                    'error': str(e)
                })

    def load_directory(self):
        """Load all supported files from a directory recursively."""
        supported_extensions = ('.txt', '.pdf')
        files_processed = 0

        for root, _, files in os.walk(self.path):
            for file in files:
                if file.lower().endswith(supported_extensions):
                    file_path = os.path.join(root, file)

                    try:
                        # Temporarily store current path
                        original_path = self.path
                        self.path = file_path

                        if file.lower().endswith('.txt'):
                            self.load_file()
                        elif file.lower().endswith('.pdf'):
                            self.load_pdf()

                        files_processed += 1

                        # Restore original path
                        self.path = original_path

                    except Exception as e:
                        print(f"Warning: Could not process {file_path}: {e}")
                        # Restore original path even on error
                        self.path = original_path

        print(f"Processed {files_processed} files from directory {self.path}")

    def load_documents(self) -> List[str]:
        """Load and return all documents."""
        self.load()
        return self.documents

    def load_documents_with_metadata(self) -> Tuple[List[str], List[Dict]]:
        """Load documents and return both documents and metadata."""
        self.extract_metadata = True
        self.load()
        return self.documents, self.metadata

    def get_document_info(self) -> Dict:
        """Get summary information about loaded documents."""
        total_docs = len(self.documents)
        total_chars = sum(len(doc) for doc in self.documents)
        total_words = sum(len(doc.split()) for doc in self.documents)

        file_types = {}
        if self.metadata:
            for meta in self.metadata:
                file_type = meta.get('file_type', 'unknown')
                file_types[file_type] = file_types.get(file_type, 0) + 1

        return {
            'total_documents': total_docs,
            'total_characters': total_chars,
            'total_words': total_words,
            'average_doc_length': total_chars // total_docs if total_docs > 0 else 0,
            'file_types': file_types
        }


class PDFLoader:
    """Specialized PDF loader with advanced features and per-page metadata."""

    def __init__(self, path: str):
        self.path = path
        self.documents = []
        self.metadata = []

    def load_with_page_metadata(self) -> Tuple[List[str], List[Dict]]:
        """Load PDF with detailed metadata for each page."""
        try:
            with pdfplumber.open(self.path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    page_text = page.extract_text()

                    if page_text and page_text.strip():
                        self.documents.append(page_text.strip())

                        # Extract detailed page metadata
                        page_metadata = {
                            'source': self.path,
                            'page_number': page_num,
                            'total_pages': len(pdf.pages),
                            'char_count': len(page_text),
                            'word_count': len(page_text.split()),
                            'page_width': page.width,
                            'page_height': page.height,
                        }

                        # Try to extract additional information
                        try:
                            # Count tables and images if available
                            tables = page.find_tables()
                            page_metadata['table_count'] = len(tables) if tables else 0

                            # Get page orientation
                            page_metadata['orientation'] = 'landscape' if page.width > page.height else 'portrait'

                        except Exception:
                            # If advanced features fail, continue with basic metadata
                            pass

                        self.metadata.append(page_metadata)

        except Exception as e:
            raise ValueError(f"Error processing PDF {self.path}: {str(e)}")

        return self.documents, self.metadata

    def load_with_chapters(self, chapter_keywords: List[str] = None) -> Tuple[List[str], List[Dict]]:
        """Load PDF and attempt to split by chapters/sections."""
        if chapter_keywords is None:
            chapter_keywords = ['chapter', 'section', 'part', 'introduction', 'conclusion']

        full_text = ""
        page_mapping = []

        # First pass: extract all text with page tracking
        with pdfplumber.open(self.path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    start_pos = len(full_text)
                    full_text += page_text + "\n"
                    end_pos = len(full_text)
                    page_mapping.append({
                        'page': page_num,
                        'start': start_pos,
                        'end': end_pos
                    })

        # Second pass: split by chapters
        chapters = []
        chapter_metadata = []

        lines = full_text.split('\n')
        current_chapter = []
        current_chapter_title = "Introduction"
        char_count = 0

        for line in lines:
            line_start = char_count
            char_count += len(line) + 1  # +1 for newline

            # Check if line might be a chapter heading
            line_lower = line.strip().lower()
            is_chapter_start = any(keyword in line_lower for keyword in chapter_keywords)

            if is_chapter_start and current_chapter and len(line.strip()) < 100:
                # Save current chapter
                chapter_text = '\n'.join(current_chapter)
                if chapter_text.strip():
                    chapters.append(chapter_text.strip())

                    # Find which page this chapter spans
                    chapter_pages = []
                    for page_info in page_mapping:
                        if page_info['start'] <= line_start <= page_info['end']:
                            chapter_pages.append(page_info['page'])

                    chapter_metadata.append({
                        'source': self.path,
                        'chapter_title': current_chapter_title,
                        'chapter_number': len(chapters),
                        'char_count': len(chapter_text),
                        'word_count': len(chapter_text.split()),
                        'pages': chapter_pages,
                        'start_page': min(chapter_pages) if chapter_pages else None,
                        'end_page': max(chapter_pages) if chapter_pages else None
                    })

                # Start new chapter
                current_chapter = [line]
                current_chapter_title = line.strip()[:50]  # First 50 chars as title
            else:
                current_chapter.append(line)

        # Add final chapter
        if current_chapter:
            chapter_text = '\n'.join(current_chapter)
            if chapter_text.strip():
                chapters.append(chapter_text.strip())
                chapter_metadata.append({
                    'source': self.path,
                    'chapter_title': current_chapter_title,
                    'chapter_number': len(chapters),
                    'char_count': len(chapter_text),
                    'word_count': len(chapter_text.split()),
                    'pages': [pm['page'] for pm in page_mapping[-len(current_chapter):]]
                })

        self.documents = chapters
        self.metadata = chapter_metadata

        return chapters, chapter_metadata


class YouTubeLoader:
    """YouTube video transcript loader with metadata extraction."""

    def __init__(self, url: str):
        if not YOUTUBE_AVAILABLE:
            raise ImportError(
                "YouTube functionality requires youtube-transcript-api and pytube. "
                "Install with: pip install youtube-transcript-api pytube"
            )

        self.url = url
        self.video_id = self._extract_video_id(url)
        self.documents = []
        self.metadata = []

    def _extract_video_id(self, url: str) -> str:
        """Extract video ID from various YouTube URL formats."""
        # Handle different YouTube URL formats
        patterns = [
            r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([^&\n?#]+)',
            r'youtube\.com/watch\?.*v=([^&\n?#]+)',
        ]

        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)

        # If no pattern matches, try parsing as query parameter
        parsed_url = urlparse(url)
        if parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
            query_params = parse_qs(parsed_url.query)
            if 'v' in query_params:
                return query_params['v'][0]
        elif parsed_url.hostname == 'youtu.be':
            return parsed_url.path[1:]  # Remove leading slash

        raise ValueError(f"Could not extract video ID from URL: {url}")

    def load_transcript(self, languages: List[str] = None) -> Tuple[str, Dict]:
        """Load transcript from YouTube video."""
        if languages is None:
            languages = ['en', 'en-US', 'en-GB']

        try:
            # Create API instance
            yt_api = YouTubeTranscriptApi()

            # Try to get transcript in preferred languages
            transcript_data = None
            used_language = None

            try:
                transcript_data = yt_api.fetch(self.video_id, languages)
                used_language = languages[0]  # Assume first language worked
            except Exception:
                # If specific languages failed, try any available transcript
                try:
                    # Get list of available transcripts
                    transcript_list = yt_api.list(self.video_id)
                    # Get first available transcript
                    transcript = next(iter(transcript_list))
                    transcript_data = transcript.fetch()
                    used_language = transcript.language_code
                except Exception as e:
                    raise ValueError(f"No transcript available for video ID: {self.video_id}. Error: {str(e)}")

            # Combine transcript text
            full_text = ""
            timestamps = []

            # transcript_data is a FetchedTranscript object with transcript entries
            for entry in transcript_data:
                text = entry.text.strip()
                start_time = entry.start
                duration = entry.duration

                full_text += f"{text} "
                timestamps.append({
                    'text': text,
                    'start': start_time,
                    'duration': duration,
                    'end': start_time + duration
                })

            # Get video metadata using pytube
            try:
                yt = YouTube(self.url)
                video_metadata = {
                    'source': self.url,
                    'video_id': self.video_id,
                    'title': yt.title,
                    'author': yt.author,
                    'length_seconds': yt.length,
                    'view_count': yt.views,
                    'publish_date': str(yt.publish_date) if yt.publish_date else None,
                    'description': yt.description[:500] if yt.description else None,  # First 500 chars
                    'transcript_language': used_language,
                    'transcript_entries': len(transcript_data),
                    'word_count': len(full_text.split()),
                    'char_count': len(full_text),
                    'timestamps': timestamps
                }
            except Exception as e:
                # Fallback metadata if pytube fails
                video_metadata = {
                    'source': self.url,
                    'video_id': self.video_id,
                    'transcript_language': used_language,
                    'transcript_entries': len(transcript_data),
                    'word_count': len(full_text.split()),
                    'char_count': len(full_text),
                    'timestamps': timestamps,
                    'metadata_error': str(e)
                }

            self.documents.append(full_text.strip())
            self.metadata.append(video_metadata)

            return full_text.strip(), video_metadata

        except Exception as e:
            raise ValueError(f"Error loading transcript for {self.url}: {str(e)}")

    def load_transcript_with_timestamps(self, chunk_by_time: bool = True, chunk_duration: int = 300) -> Tuple[List[str], List[Dict]]:
        """Load transcript split by time chunks with detailed metadata."""
        try:
            # First get the full transcript
            full_text, base_metadata = self.load_transcript()

            if not chunk_by_time:
                return [full_text], [base_metadata]

            # Split by time chunks
            timestamps = base_metadata['timestamps']
            chunks = []
            chunk_metadata = []

            current_chunk = ""
            current_start = None
            chunk_entries = []

            for entry in timestamps:
                # Start new chunk if duration exceeded or this is the first entry
                if (current_start is None or
                    (entry['start'] - current_start) >= chunk_duration):

                    # Save previous chunk if it exists
                    if current_chunk.strip():
                        chunks.append(current_chunk.strip())

                        chunk_meta = base_metadata.copy()
                        chunk_meta.update({
                            'chunk_start_time': current_start,
                            'chunk_end_time': chunk_entries[-1]['end'] if chunk_entries else current_start,
                            'chunk_duration': (chunk_entries[-1]['end'] - current_start) if chunk_entries else 0,
                            'chunk_entries': len(chunk_entries),
                            'chunk_word_count': len(current_chunk.split()),
                            'chunk_char_count': len(current_chunk),
                            'chunk_number': len(chunks)
                        })
                        chunk_metadata.append(chunk_meta)

                    # Start new chunk
                    current_chunk = entry['text'] + " "
                    current_start = entry['start']
                    chunk_entries = [entry]
                else:
                    # Add to current chunk
                    current_chunk += entry['text'] + " "
                    chunk_entries.append(entry)

            # Add final chunk
            if current_chunk.strip():
                chunks.append(current_chunk.strip())

                chunk_meta = base_metadata.copy()
                chunk_meta.update({
                    'chunk_start_time': current_start,
                    'chunk_end_time': chunk_entries[-1]['end'] if chunk_entries else current_start,
                    'chunk_duration': (chunk_entries[-1]['end'] - current_start) if chunk_entries else 0,
                    'chunk_entries': len(chunk_entries),
                    'chunk_word_count': len(current_chunk.split()),
                    'chunk_char_count': len(current_chunk),
                    'chunk_number': len(chunks)
                })
                chunk_metadata.append(chunk_meta)

            self.documents = chunks
            self.metadata = chunk_metadata

            return chunks, chunk_metadata

        except Exception as e:
            raise ValueError(f"Error processing transcript chunks for {self.url}: {str(e)}")

    @staticmethod
    def is_youtube_url(url: str) -> bool:
        """Check if a URL is a valid YouTube URL."""
        youtube_domains = ['youtube.com', 'www.youtube.com', 'youtu.be', 'm.youtube.com']
        try:
            parsed = urlparse(url)
            return parsed.hostname in youtube_domains
        except:
            return False

    @staticmethod
    def get_available_languages(url: str) -> List[str]:
        """Get list of available transcript languages for a YouTube video."""
        if not YOUTUBE_AVAILABLE:
            raise ImportError("YouTube functionality requires youtube-transcript-api")

        try:
            loader = YouTubeLoader(url)
            yt_api = YouTubeTranscriptApi()
            transcript_list = yt_api.list(loader.video_id)
            return [t.language_code for t in transcript_list]
        except Exception as e:
            raise ValueError(f"Could not get available languages for {url}: {str(e)}")


class CharacterTextSplitter:
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        assert (
            chunk_size > chunk_overlap
        ), "Chunk size must be greater than chunk overlap"

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split(self, text: str) -> List[str]:
        chunks = []
        for i in range(0, len(text), self.chunk_size - self.chunk_overlap):
            chunks.append(text[i : i + self.chunk_size])
        return chunks

    def split_texts(self, texts: List[str]) -> List[str]:
        chunks = []
        for text in texts:
            chunks.extend(self.split(text))
        return chunks


if __name__ == "__main__":
    loader = TextFileLoader("data/KingLear.txt")
    loader.load()
    splitter = CharacterTextSplitter()
    chunks = splitter.split_texts(loader.documents)
    print(len(chunks))
    print(chunks[0])
    print("--------")
    print(chunks[1])
    print("--------")
    print(chunks[-2])
    print("--------")
    print(chunks[-1])
