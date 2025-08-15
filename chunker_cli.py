"""Simple CLI for CodeChunker"""

from pathlib import Path

from src.core.chunker import CodeChunker
from src.utils.logging import get_logger

logger = get_logger(__name__)

if __name__ == "__main__":
    import argparse
    import json
    import sys
    from dataclasses import is_dataclass, asdict

    def chunk_to_dict(c) -> dict:
        """Best-effort serializer for CodeChunk-like objects."""
        if is_dataclass(c):
            return asdict(c)
        # Fallback: grab typical attributes if not a dataclass
        fields = ["id", "content", "file_path", "language", "start_line", "end_line", "metadata"]
        return {f: getattr(c, f, None) for f in fields}

    def iter_files(paths, recursive: bool, exts: set | None):
        """Yield Path objects to process."""
        seen = set()
        for p in paths:
            p = Path(p)
            if not p.exists():
                logger.warning(f"Path not found: {p}")
                continue
            if p.is_file():
                if (not exts) or (p.suffix.lower() in exts):
                    key = p.resolve()
                    if key not in seen:
                        seen.add(key)
                        yield p
            else:
                # directory
                if recursive:
                    for fp in p.rglob("*"):
                        if fp.is_file() and ((not exts) or (fp.suffix.lower() in exts)):
                            key = fp.resolve()
                            if key not in seen:
                                seen.add(key)
                                yield fp
                else:
                    for fp in p.glob("*"):
                        if fp.is_file() and ((not exts) or (fp.suffix.lower() in exts)):
                            key = fp.resolve()
                            if key not in seen:
                                seen.add(key)
                                yield fp

    parser = argparse.ArgumentParser(
        prog="code-chunker",
        description="Chunk source files into semantic or sliding-window chunks."
    )
    parser.add_argument(
        "paths", nargs="+",
        help="File(s) or directory(ies) to process."
    )
    parser.add_argument(
        "-r", "--recursive", action="store_true",
        help="Recurse into directories."
    )
    parser.add_argument(
        "--ext", nargs="*", default=None,
        help="Optional list of file extensions to include (e.g. --ext .py .ts .md). "
             "Defaults to all known LANGUAGE_EXTENSIONS."
    )
    parser.add_argument(
        "--max-tokens", type=int, default=None,
        help="Override settings.max_tokens for chunking."
    )
    parser.add_argument(
        "--overlap", type=int, default=None,
        help="Override settings.chunk_overlap for chunking."
    )
    parser.add_argument(
        "-f", "--format", choices=["jsonl", "json", "pretty"], default="jsonl",
        help="Output format: jsonl (default), json (compact array), pretty (indented array)."
    )
    parser.add_argument(
        "-o", "--out", default="-",
        help='Output file path (default "-" for stdout).'
    )
    parser.add_argument(
        "--summary", action="store_true",
        help="Print a brief summary to stderr after processing."
    )

    args = parser.parse_args()

    # Determine extensions
    if args.ext:
        # Normalize to lowercase with dot prefix
        exts = set(e if e.startswith(".") else f".{e}" for e in args.ext)
        exts = {e.lower() for e in exts}
    else:
        exts = set(CodeChunker.LANGUAGE_EXTENSIONS.keys())

    # Instantiate the chunker with optional overrides
    chunker = CodeChunker(max_tokens=args.max_tokens, overlap=args.overlap)

    all_chunks = []
    total_files = 0

    for file_path in iter_files(args.paths, recursive=args.recursive, exts=exts):
        total_files += 1
        chunks = chunker.chunk_file(file_path)
        if not chunks:
            logger.info(f"No chunks produced for: {file_path}")
        for c in chunks:
            all_chunks.append(chunk_to_dict(c))

    # Write output
    out_fp = sys.stdout if args.out == "-" else open(args.out, "w", encoding="utf-8")

    try:
        if args.format == "jsonl":
            for obj in all_chunks:
                out_fp.write(json.dumps(obj, ensure_ascii=False) + "\n")
        elif args.format == "json":
            out_fp.write(json.dumps(all_chunks, ensure_ascii=False))
        else:  # pretty
            out_fp.write(json.dumps(all_chunks, ensure_ascii=False, indent=2))
        if out_fp is not sys.stdout:
            out_fp.flush()
    finally:
        if out_fp is not sys.stdout:
            out_fp.close()

    if args.summary:
        # Basic summary to stderr so it doesn't pollute machine-readable output
        total_chunks = len(all_chunks)
        by_lang = {}
        for c in all_chunks:
            lang = c.get("language", "unknown")
            by_lang[lang] = by_lang.get(lang, 0) + 1
        sys.stderr.write(
            f"Processed {total_files} file(s); produced {total_chunks} chunk(s). "
            f"By language: {by_lang}\n"
        )
