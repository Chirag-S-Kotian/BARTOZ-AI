"""
cache_loader.py
- Loads all .txt files from the cache directory and returns them as LangChain Documents for indexing.
- Designed for integration into the RAG pipeline and async ingestion.
"""
import os
from langchain.schema import Document

CACHE_DIR = "cache"

def load_cached_documents():
    """
    Loads all .txt files from the cache directory and returns them as LangChain Documents.
    Returns:
        List[Document]: List of LangChain Document objects.
    """
    docs = []
    if not os.path.exists(CACHE_DIR):
        return docs
    for fname in os.listdir(CACHE_DIR):
        if fname.endswith(".txt"):
            fpath = os.path.join(CACHE_DIR, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                # Attempt to extract metadata if present (simple heuristics)
                lines = content.split("\n")
                title = lines[0].replace("Title:", "").strip() if lines and lines[0].lower().startswith("title:") else ""
                url = ""
                published_date = ""
                for line in lines:
                    if line.lower().startswith("url:"):
                        url = line.split(":", 1)[-1].strip()
                    if line.lower().startswith("published:"):
                        published_date = line.split(":", 1)[-1].strip()
                metadata = {"source": "cache", "title": title, "url": url, "published_date": published_date, "filename": fname}
                docs.append(Document(page_content=content, metadata=metadata))
            except Exception as e:
                print(f"[Cache Loader] Failed to load {fname}: {e}")
    return docs
