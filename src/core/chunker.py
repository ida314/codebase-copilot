"""Code chunking functionality with language awareness"""

import re
import hashlib
import time
from pathlib import Path
from typing import List
from src.models.code_chunk import CodeChunk
from src.config.settings import settings
from src.utils.logging import get_logger

logger = get_logger(__name__)


class CodeChunker:
    """Intelligent code chunking with language awareness"""

    LANGUAGE_EXTENSIONS = {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".go": "go",
        ".rs": "rust",
        ".java": "java",
        ".cpp": "cpp",
        ".c": "c",
        ".md": "markdown",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".json": "json",
    }

    def __init__(self, max_tokens: int = None, overlap: int = None):
        self.max_tokens = max_tokens or settings.max_tokens
        self.overlap = overlap or settings.chunk_overlap

    def chunk_file(self, file_path: Path) -> List[CodeChunk]:
        """Chunk a single file into semantic units"""
        if not file_path.exists():
            logger.warning(f"File not found: {file_path}")
            return []

        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            logger.error(f"Error reading {file_path}: {e}")
            return []

        language = self._detect_language(file_path)
        chunks = []

        # For code files, try to chunk by functions/classes
        if language in ["python", "javascript", "typescript", "go", "java"]:
            chunks = self._chunk_by_structure(content, file_path, language)

        # Fallback to sliding window if structural chunking fails or for other files
        if not chunks:
            chunks = self._chunk_by_window(content, file_path, language)

        return chunks

    def _detect_language(self, file_path: Path) -> str:
        """Detect programming language from file extension"""
        ext = file_path.suffix.lower()
        return self.LANGUAGE_EXTENSIONS.get(ext, "text")

    def _chunk_by_structure(
        self, content: str, file_path: Path, language: str
    ) -> List[CodeChunk]:
        """Chunk code by structural elements (functions, classes)"""
        chunks = []

        if language == "python":
            pattern = r"^(class |def |async def ).*?(?=^(?:class |def |async def |\Z))"
            matches = re.finditer(pattern, content, re.MULTILINE | re.DOTALL)

            for match in matches:
                chunk_content = match.group(0).strip()
                if len(chunk_content.split()) <= self.max_tokens * 1.5:
                    start_line = content[: match.start()].count("\n") + 1
                    end_line = start_line + chunk_content.count("\n")

                    chunk = CodeChunk(
                        id=self._generate_chunk_id(file_path, start_line),
                        content=chunk_content,
                        file_path=str(file_path),
                        language=language,
                        start_line=start_line,
                        end_line=end_line,
                        metadata={"chunk_type": "structural"},
                    )
                    chunks.append(chunk)

        return chunks

    def _chunk_by_window(
        self, content: str, file_path: Path, language: str
    ) -> List[CodeChunk]:
        """Fallback sliding window chunking"""
        chunks = []
        lines = content.split("\n")

        window_lines = max(1, self.max_tokens // 10)
        overlap_lines = max(1, self.overlap // 10)

        i = 0
        while i < len(lines):
            chunk_lines = lines[i : i + window_lines]
            chunk_content = "\n".join(chunk_lines)

            if chunk_content.strip():
                chunk = CodeChunk(
                    id=self._generate_chunk_id(file_path, i + 1),
                    content=chunk_content,
                    file_path=str(file_path),
                    language=language,
                    start_line=i + 1,
                    end_line=min(i + window_lines, len(lines)),
                    metadata={"chunk_type": "window"},
                )
                chunks.append(chunk)

            i += window_lines - overlap_lines

        return chunks

    def _generate_chunk_id(self, file_path: Path, start_line: int) -> str:
        """Generate unique chunk ID"""
        unique_str = f"{file_path}:{start_line}:{time.time()}"
        return hashlib.md5(unique_str.encode()).hexdigest()[:12]
