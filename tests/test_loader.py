from app.rag.loader import chunk_text

def test_chunking_preserves_content():
    chunks = chunk_text("one two three four five six", 4, 1)
    assert chunks
    assert "one" in chunks[0]
    assert "six" in " ".join(chunks)
