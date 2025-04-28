# Assuming necessary imports for your RAG pipeline components
# Ensure these libraries are installed:
# pip install langchain-community faiss-cpu sentence-transformers
from data_loader import fetch_arxiv, fetch_pubmed, fetch_ssrn, fetch_ai_companies
from cache_loader import load_cached_documents
import asyncio
from async_data_loader import fetch_all_sources
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

# Import the async gemini_query function from your updated gemini_client.py
from gemini_client import gemini_query # This should now be async def

# Assuming openrouter_client.py exists and contains a synchronous function
# for DeepSeek, let's assume it's named openrouter_query.
# If your DeepSeek function is async, you'll need to await it below.
# from openrouter_client import openrouter_query # Assuming synchronous function

import os
import json
import logging
from typing import List # Import List for type hinting

# Configure logging
logging.basicConfig(level=logging.INFO)

# --- Indexing Part ---
# This part runs when the script is imported, typically on startup.
# It loads data, splits it, creates embeddings, and builds/loads the FAISS index.
# Ensure your data_loader functions (fetch_arxiv, fetch_pubmed, fetch_ssrn) are synchronous
# and return data in the expected format, including relevant metadata like 'published_date' and 'url'.
try:
    os.makedirs("faiss_index", exist_ok=True)

    all_docs = []
    # --- Load cached documents ---
    cached_docs = load_cached_documents()
    logging.info(f"Loaded {len(cached_docs)} cached documents from cache directory.")
    all_docs.extend(cached_docs)

    # --- Fetch new data from sources ---
    logging.info("Fetching data from sources...")
    sources = {
        "arxiv": fetch_arxiv(),
        "pubmed": fetch_pubmed(),
        "ssrn": fetch_ssrn(),
        "ai_companies": fetch_ai_companies()
    }
    logging.info("Data fetching complete.")

    logging.info("Creating Langchain Documents from fetched sources...")
    for source_name, papers in sources.items():
        for paper in papers:
            # Ensure paper has 'title', 'summary', and ideally 'published_date', 'url' keys
            title = paper.get('title', 'No Title')
            summary = paper.get('summary', 'No Summary')
            published_date = paper.get('published_date')
            url = paper.get('url')

            if source_name == 'ai_companies':
                # For companies, include all enriched fields and lists
                fields = [
                    f"Name: {paper.get('name', '')}",
                    f"Category: {paper.get('category', '')}",
                    f"Description: {paper.get('description', '')}",
                    f"Founded: {paper.get('founded', '')}",
                    f"Founders: {', '.join(paper.get('founders', []))}",
                    f"Headquarters: {paper.get('headquarters', '')}",
                    f"CEO: {paper.get('ceo', '')}",
                    f"Valuation: {paper.get('valuation', '')}",
                    f"Funding: {paper.get('funding', '')}",
                    f"Twitter: {paper.get('twitter', '')}",
                    f"Website: {paper.get('website', '')}",
                    f"Active Years: {paper.get('active_years', '')}",
                    f"Top AI Agent in Years: {', '.join(str(y) for y in paper.get('top_in_year', []))}",
                    f"Latest Blog: {paper.get('latest_blog', {}).get('title', '')} ({paper.get('latest_blog', {}).get('url', '')})",
                ]
                # Add products
                products = paper.get('products', [])
                if products:
                    fields.append(f"Products: {', '.join(products)}")
                # Add notable projects
                notable_projects = paper.get('notable_projects', [])
                if notable_projects:
                    fields.append(f"Notable Projects: {', '.join(notable_projects)}")
                # Add resources (news, research, etc.)
                resources = paper.get('resources', [])[:200]
                if resources:
                    fields.append("Resources:")
                    for res in resources:
                        res_title = res.get('title', '')
                        res_url = res.get('url', '')
                        res_summary = res.get('summary', '') if 'summary' in res else ''
                        # Add a detailed, dedicated Document for each resource
                        resource_content = f"Resource Title: {res_title}\nResource URL: {res_url}\nParent: {paper.get('name', '')}\nCategory: {paper.get('category', '')}"
                        if res_summary:
                            resource_content += f"\nSummary: {res_summary}"
                        resource_metadata = {
                            "source": source_name,
                            "title": res_title,
                            "url": res_url,
                            "parent": paper.get('name', ''),
                            "category": paper.get('category', '')
                        }
                        all_docs.append(Document(page_content=resource_content, metadata=resource_metadata))
                        # Also include in the parent chunk
                        if res_summary:
                            fields.append(f"- {res_title} ({res_url})\n  Summary: {res_summary}")
                        else:
                            fields.append(f"- {res_title} ({res_url})")
                content = "\n".join([f for f in fields if f and f != '()'])
            else:
                content = f"Title: {title}\n\nSummary: {summary}"

            metadata = {"source": source_name, "title": title}
            if published_date:
                metadata['published_date'] = published_date
            if url:
                metadata['url'] = url

            doc = Document(page_content=content, metadata=metadata)
            all_docs.append(doc)

    # Fetch and add async resources from additional sources
    # To increase document count, raise max_docs below (e.g., 2000, 5000)
    # Async fetch moved to FastAPI startup event. See main.py for ingestion.
    pass

    # Deduplicate all_docs by URL (prefer most recent)
    seen_urls = set()
    deduped_docs = []
    for doc in all_docs:
        url = doc.metadata.get("url", "")
        if url and url not in seen_urls:
            deduped_docs.append(doc)
            seen_urls.add(url)
        elif not url:
            deduped_docs.append(doc)  # Always include docs with no URL (e.g., static or malformed)
    logging.info(f"Deduplicated to {len(deduped_docs)} unique documents (by URL).")

    logging.info("Splitting documents...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=2500, chunk_overlap=300)
    texts = splitter.split_documents(deduped_docs)
    logging.info(f"Split into {len(texts)} chunks.")

    # Define the path for the FAISS index
    faiss_index_path = "faiss_index"

    # Check if index already exists to avoid re-indexing every time
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    if os.path.exists(faiss_index_path):
        logging.info("Loading existing FAISS index...")
        # allow_dangerous_deserialization is needed for loading FAISS indexes
        vectorstore = FAISS.load_local(faiss_index_path, embeddings, allow_dangerous_deserialization=True)
        logging.info("FAISS index loaded.")
    else:
        logging.info("Creating new FAISS index...")
        vectorstore = FAISS.from_documents(texts, embeddings)
        vectorstore.save_local(faiss_index_path)
        logging.info("FAISS index created and saved.")

    # Save metadata (optional, but good for tracking sources)
    metadata_list = [{"title": doc.metadata.get("title", "N/A"),
                      "source": doc.metadata.get("source", "N/A"),
                      "published_date": doc.metadata.get("published_date", "N/A"),
                      "url": doc.metadata.get("url", "N/A")} for doc in all_docs]
    metadata_path = "faiss_index/metadata.json"
    with open(metadata_path, "w") as f:
        json.dump(metadata_list, f, indent=2)
    logging.info(f"Metadata saved to {metadata_path}")

    print("Indexing complete!")

except Exception as e:
    logging.error(f"Error during indexing process: {e}", exc_info=True)
    # Handle the error appropriately, maybe exit or set a flag
    vectorstore = None # Ensure vectorstore is None if indexing fails
    print("Indexing failed!")


# --- RAG Retrieval Logic ---
# This function now uses the vectorstore to find relevant context.
def retrieve_context(query: str, vectorstore: FAISS, k: int = 6, diversify_sources: bool = True, date_from: str = None, date_to: str = None) -> str:
    """
    Advanced RAG context retrieval: deduplicate, diversify, enrich metadata, allow dynamic k.
    """
    if vectorstore is None:
        logging.error("Vectorstore is not initialized. Cannot retrieve context.")
        return f"User Query: {query}\n\nRelevant Context:\nError: Vectorstore not available."
    try:
        logging.info(f"Performing similarity search for query: {query}")
        # Increased k for more context (default k=6, so 36 chunks)
        docs: List[Document] = vectorstore.similarity_search(query, k=k*6) # get more for dedup/diversity

        # --- Temporal Filtering (if requested) ---
        if date_from or date_to:
            from datetime import datetime
            def in_range(doc):
                date_str = doc.metadata.get('published_date', '')
                try:
                    date = datetime.fromisoformat(date_str[:19]) if date_str else None
                except Exception:
                    date = None
                if date_from and date:
                    if date < datetime.fromisoformat(date_from):
                        return False
                if date_to and date:
                    if date > datetime.fromisoformat(date_to):
                        return False
                return True
            docs = [doc for doc in docs if in_range(doc)]

        # --- Expanded AI-Related Keywords ---
        global keywords
        # --- AI-Related Filtering ---
        def is_ai_related(text):
            text_lower = text.lower()
            keywords = ["ai","artificial intelligence","machine learning","llm","agent","agents","company","companies"]
            return any(kw in text_lower for kw in keywords)
        filtered_docs = [doc for doc in docs if is_ai_related(doc.page_content) or is_ai_related(doc.metadata.get('title', ''))]
        logging.info(f"AI-related docs found: {len(filtered_docs)} / {len(docs)} for query: '{query}'")

        # Fallback: if too few, use keyword overlap
        if len(filtered_docs) < k:
            scored = []
            query_terms = set(query.lower().split())
            for doc in docs:
                doc_text = doc.page_content.lower() + ' ' + doc.metadata.get('title', '').lower()
                score = sum(1 for term in query_terms if term in doc_text)
                scored.append((score, doc))
            scored.sort(reverse=True, key=lambda x: x[0])
            fallback_docs = [doc for score, doc in scored if score > 0][:k]
            if len(fallback_docs) < k:
                fallback_docs = docs[:k]
            filtered_docs = filtered_docs + [doc for doc in fallback_docs if doc not in filtered_docs]
        # Pass more context to the model (up to k*4, e.g., 24 chunks)
        filtered_docs = filtered_docs[:k*4]
        if not filtered_docs:
            docs_sorted = sorted(docs, key=lambda d: d.metadata.get('published_date', ''), reverse=True)
            filtered_docs = docs_sorted[:k]

        # Deduplicate by title+source
        seen = set()
        deduped_docs = []
        for doc in filtered_docs:
            key = (doc.metadata.get('title', '').strip().lower(), doc.metadata.get('source', '').strip().lower())
            if key in seen:
                continue
            seen.add(key)
            deduped_docs.append(doc)

        # Source diversity: try to balance sources
        if diversify_sources:
            by_source = {}
            for doc in deduped_docs:
                src = doc.metadata.get('source', 'unknown')
                by_source.setdefault(src, []).append(doc)
            selected = []
            while len(selected) < k and any(by_source.values()):
                for src in list(by_source.keys()):
                    if by_source[src]:
                        selected.append(by_source[src].pop(0))
                    if len(selected) >= k:
                        break
            docs_final = selected
        else:
            docs_final = deduped_docs[:k]
        logging.info(f"Selected {len(docs_final)} documents after source diversity.")

        # Boost by recency and query keyword match
        from datetime import datetime
        def parse_date(date_str):
            from datetime import datetime
            try:
                # Try ISO format
                return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            except Exception:
                # Try YYYY-MM-DD or YYYY/MM/DD
                import re
                m = re.match(r'(\d{4})[-/](\d{2})[-/](\d{2})', date_str or '')
                if m:
                    try:
                        return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))
                    except Exception:
                        pass
                # If still fails, return a safe default (1970-01-01)
                return datetime(1970, 1, 1)
        def boost_score(doc):
            score = 0
            title = doc.metadata.get('title', '').lower()
            content = doc.page_content.lower()
            query_keywords = [w.lower() for w in query.split() if len(w) > 2]
            if any(qk in title or qk in content for qk in query_keywords):
                score += 2
            date_str = doc.metadata.get('published_date', '')
            try:
                date_val = parse_date(date_str)
                score += (date_val.timestamp()) / 1e12
            except Exception:
                score += 0
            return score
        docs_final.sort(key=boost_score, reverse=True)

        # Format context for LLM: detailed, clear, always with title/source/url
        context_blocks = []
        for idx, doc in enumerate(docs_final):
            context_blocks.append(f"--- Document {idx+1} ---\nTitle: {doc.metadata.get('title', 'N/A')}\nSource: {doc.metadata.get('source', 'N/A')}\nPublished: {doc.metadata.get('published_date', 'N/A')}\nURL: {doc.metadata.get('url', 'N/A')}\nContent: {doc.page_content}")
        context_str = "\n\n".join(context_blocks)
        # Compose the prompt to instruct for detailed, comprehensive answers
        prompt = f"""
Research Context:
{context_str}

User Question: {query}

Instructions:
- Provide a detailed, comprehensive answer using all relevant information from the context above.
- Cite sources (title and URL) for every fact or claim.
- If the answer is not found in the context, reply with the following detailed message:
  Sorry, the answer to your question could not be found in the provided research context. This means that, based on the indexed documents, there is currently no relevant or up-to-date information available to fully answer your query. The research context may include historical papers, summaries, or references to related topics, but does not contain a direct or comprehensive answer to your specific question. Please note: All indexed documents are preserved unless you manually delete the faiss_index directory. If you believe relevant research should be present, try re-indexing your sources or broadening your query. The database may contain older research (e.g., historical arXiv papers from 1995/1996) or recent papers on related but not identical topics (like LLM chatbots or general AI advances). For the most accurate results, ensure your question closely matches the topics and timeframes covered by the indexed documents. If you need the very latest research, consider updating your data sources or specifying your query more broadly.
- Do NOT use prior knowledge or make up facts. Only use the supplied context.
- Write clearly and thoroughly, not just a summary.
Answer:
"""
        return prompt
    except Exception as e:
        logging.error(f"Error during context retrieval: {e}", exc_info=True)
        return f"User Query: {query}\n\nRelevant Context:\nError during retrieval: {e}"

# --- Answer fetching part ---
# This function must be async because it calls async functions (like gemini_query)
async def get_research_answer(query: str, model: str) -> str:
    """
    Fetches a research answer using the specified model after retrieving context.
    Args:
        query: The user's original query.
        model: The name of the model to use ("gemini" or "deepseek").
    Returns:
        The answer generated by the model (string), or an error message (string).
    """
    logging.info(f"Received query for model: {model}")
    if 'vectorstore' not in globals() or vectorstore is None:
        logging.error("Vectorstore is not available. Cannot process query.")
        return "Error: Research index not available. Please check backend startup logs."
    # Use more context and instruct for detailed answer in the prompt
    rag_prompt_with_context = retrieve_context(query, vectorstore)
    logging.info("Context retrieval step completed.")
    try:
        if model == "gemini":
            from gemini_client import gemini_query
            response = await gemini_query(rag_prompt_with_context)
            logging.info("Received response from Gemini.")
            return response
        elif model == "deepseek":
            from openrouter_client import openrouter_query_async
            response = await openrouter_query_async(rag_prompt_with_context)
            logging.info("Received response from DeepSeek.")
            return response
        else:
            logging.warning(f"Unsupported model selected: {model}")
            return "Unsupported model selected."
    except Exception as e:
        logging.error(f"Error in get_research_answer: {e}", exc_info=True)
        return f"An error occurred while fetching the answer: {e}"