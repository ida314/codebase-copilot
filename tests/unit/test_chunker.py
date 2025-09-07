# tests/test_chunker.py
from pathlib import Path
import pytest

from src.core.chunker import CodeChunker
from src.models.code_chunk import CodeChunk


def _make_file(tmp_path: Path, name: str, text: str) -> Path:
    p = tmp_path / name
    p.write_text(text, encoding="utf-8")
    return p


def test_python_structural_chunking(tmp_path: Path):
    code = """
def foo():
    return 1

class Bar:
    def baz(self):
        return 2
"""
    path = _make_file(tmp_path, "example.py", code)
    chunker = CodeChunker(max_tokens=200, overlap=20)

    chunks = chunker.chunk_file(path)

    assert len(chunks) >= 2  # def foo + class Bar
    assert all(isinstance(c, CodeChunk) for c in chunks)
    assert all(c.language == "python" for c in chunks)
    assert all(c.metadata.get("chunk_type") == "structural" for c in chunks)


def test_window_chunking_for_non_code_files(tmp_path: Path):
    lines = "\n".join(f"line {i}" for i in range(1, 13))  # 12 lines
    path = _make_file(tmp_path, "README.md", lines)
    # Pick values that make windowing deterministic enough
    chunker = CodeChunker(max_tokens=100, overlap=10)

    chunks = chunker.chunk_file(path)

    assert len(chunks) > 0
    assert all(isinstance(c, CodeChunk) for c in chunks)
    assert chunks[0].metadata.get("chunk_type") == "window"
    # Last chunk should end at total number of lines
    assert chunks[-1].end_line == 12


def test_missing_file_returns_empty_list(tmp_path: Path):
    missing = tmp_path / "does_not_exist.py"
    chunker = CodeChunker(max_tokens=100, overlap=10)

    chunks = chunker.chunk_file(missing)

    assert chunks == []
