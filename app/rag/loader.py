from pathlib import Path
from pypdf import PdfReader
from app.core.config import settings

def read_documents(directory=None):
    base = Path(directory or settings.data_dir)
    base.mkdir(parents=True, exist_ok=True)
    docs = []
    for path in sorted(base.glob("*")):
        text = ""
        if path.suffix.lower() in {".txt", ".md"}:
            text = path.read_text(encoding="utf-8", errors="ignore")
        elif path.suffix.lower() == ".pdf":
            text = "\n".join(page.extract_text() or "" for page in PdfReader(str(path)).pages)
        if text.strip():
            docs.append({"source": path.name, "text": text.strip()})
    return docs

def chunk_text(text, size, overlap):
    words = text.split()
    step = max(1, size - overlap)
    return [" ".join(words[i:i + size]) for i in range(0, len(words), step)]
