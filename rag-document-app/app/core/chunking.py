import re
from typing import List, Literal

ChunkStrategy = Literal["fixed", "recursive"]

# Separators for recursive chunking, from coarsest to finest:
# paragraph -> line -> sentence -> word. Below word level we fall back to a hard cut.
_RECURSIVE_SEPARATORS: List[str] = [
    r"\n\s*\n",          # paragraph
    r"\n",               # line
    r"(?<=[.!?…])\s+",   # sentence end
    r"\s+",              # word
]


def split_text_into_chunks(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 100,
    strategy: ChunkStrategy = "recursive",
) -> List[str]:
    """Split a raw document text into overlapping chunks.

    strategy:
        - "fixed":     cut every `chunk_size` characters, sliding by
                       `chunk_size - chunk_overlap`.
        - "recursive": split by paragraph -> line -> sentence -> word (-> character
                       as last resort), then merge pieces back into chunks of at most
                       `chunk_size` characters with ~`chunk_overlap` characters overlap.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")
    if chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be >= 0 and < chunk_size")
    if not text or not text.strip():
        return []

    if strategy == "fixed":
        return _fixed_size_chunks(text, chunk_size, chunk_overlap)
    if strategy == "recursive":
        pieces = _recursive_split(text, chunk_size, level=0)
        return _merge_pieces(pieces, chunk_size, chunk_overlap)
    raise ValueError(f"Unknown chunk strategy: {strategy!r} (expected 'fixed' or 'recursive')")


# ---------------------------------------------------------------------------
# Fixed size
# ---------------------------------------------------------------------------

def _fixed_size_chunks(text: str, chunk_size: int, chunk_overlap: int) -> List[str]:
    step = chunk_size - chunk_overlap
    chunks: List[str] = []
    for start in range(0, len(text), step):
        chunk = text[start:start + chunk_size].strip()
        if chunk:
            chunks.append(chunk)
        if start + chunk_size >= len(text):
            break
    return chunks


# ---------------------------------------------------------------------------
# Recursive
# ---------------------------------------------------------------------------

def _split_keep_separator(text: str, pattern: str) -> List[str]:
    """Split by regex but keep each separator attached to the preceding piece,
    so that "".join(result) == text."""
    parts = re.split(f"({pattern})", text)
    pieces: List[str] = []
    # parts = [piece, sep, piece, sep, ..., piece]
    for i in range(0, len(parts), 2):
        piece = parts[i] + (parts[i + 1] if i + 1 < len(parts) else "")
        if piece:
            pieces.append(piece)
    return pieces


def _recursive_split(text: str, chunk_size: int, level: int) -> List[str]:
    """Return pieces that are each <= chunk_size, using the coarsest separator possible."""
    if len(text) <= chunk_size:
        return [text]

    if level >= len(_RECURSIVE_SEPARATORS):
        # No separator left (e.g. a very long word/URL): hard cut by characters.
        return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

    pieces: List[str] = []
    for part in _split_keep_separator(text, _RECURSIVE_SEPARATORS[level]):
        if len(part) <= chunk_size:
            pieces.append(part)
        else:
            pieces.extend(_recursive_split(part, chunk_size, level + 1))
    return pieces


def _merge_pieces(pieces: List[str], chunk_size: int, chunk_overlap: int) -> List[str]:
    """Greedily pack small pieces into chunks <= chunk_size, carrying over the
    trailing pieces (up to chunk_overlap chars) into the next chunk."""
    chunks: List[str] = []
    current: List[str] = []
    current_len = 0

    for piece in pieces:
        if current and current_len + len(piece) > chunk_size:
            chunk = "".join(current).strip()
            if chunk:
                chunks.append(chunk)
            # Drop pieces from the front until we keep only the overlap
            # and the new piece fits.
            while current and (
                current_len > chunk_overlap or current_len + len(piece) > chunk_size
            ):
                current_len -= len(current.pop(0))
        current.append(piece)
        current_len += len(piece)

    chunk = "".join(current).strip()
    if chunk and (not chunks or chunk != chunks[-1]):
        chunks.append(chunk)
    return chunks


def normalize_whitespace(text: str) -> str:
    """Clean text before chunking."""
    # TODO: strip extra spaces, newlines, repeated whitespace
    return text
