# async_ingest.py
"""
This module provides a function to fetch and ingest async resources into the RAG pipeline's vectorstore.
Call this from a FastAPI startup event for proper async compatibility.
"""
import logging
from async_data_loader import fetch_all_sources
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import os

async def fetch_and_ingest_async_resources(vectorstore, max_docs=1200):
    logging.info("[Startup] Fetching additional async resources from AI/ML/LLM news/blog/research sources...")
    try:
        async_resources = await fetch_all_sources(max_docs=max_docs)
        logging.info(f"[Startup] Fetched {len(async_resources)} async resources (news/blog/research). Ingesting...")
        docs = []
        for res in async_resources:
            content = f"Resource Title: {res['title']}\nSource: {res['source']}\nCompany: {res.get('company','')}\nType: {res['type']}\nURL: {res['url']}\nPublished: {res.get('published_date','')}\nSummary: {res.get('summary','')}\n\nFull Content: {res.get('content', '')}"
            metadata = {
                "source": res['source'],
                "title": res['title'],
                "url": res['url'],
                "company": res.get('company',''),
                "type": res['type'],
                "published_date": res.get('published_date','')
            }
            docs.append(Document(page_content=content, metadata=metadata))
        if docs:
            splitter = RecursiveCharacterTextSplitter(chunk_size=2500, chunk_overlap=300)
            texts = splitter.split_documents(docs)
            logging.info(f"[Startup] Split {len(docs)} docs into {len(texts)} chunks. Adding to vectorstore...")
            # Add to vectorstore and persist
            vectorstore.add_documents(texts)
            faiss_index_path = "faiss_index"
            vectorstore.save_local(faiss_index_path)
            logging.info(f"[Startup] Async resources ingested and FAISS index updated.")
        else:
            logging.info("[Startup] No async docs to ingest.")
    except Exception as e:
        logging.error(f"[Startup] Error fetching or ingesting async resources: {e}")
