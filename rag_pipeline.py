# Assuming necessary imports for your RAG pipeline components
# Ensure these libraries are installed:
# pip install langchain-community faiss-cpu sentence-transformers
from data_loader import fetch_arxiv, fetch_pubmed, fetch_ssrn, fetch_ai_companies # Import fetch_ai_companies for company/agent info
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
    logging.info("Fetching data from sources...")
    # Note: Ensure your fetch functions add metadata like 'published_date' and 'url'
    sources = {
        "arxiv": fetch_arxiv(), # Assuming fetch_arxiv returns data synchronously with metadata
        "pubmed": fetch_pubmed(), # Assuming fetch_pubmed returns data synchronously with metadata
        "ssrn": fetch_ssrn(), # Assuming fetch_ssrn returns data synchronously with metadata
        "ai_companies": fetch_ai_companies() # New: company/LLM/agent info
    }
    logging.info("Data fetching complete.")

    logging.info("Creating Langchain Documents...")
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

    logging.info(f"Created {len(all_docs)} documents.")

    logging.info("Splitting documents...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=2500, chunk_overlap=300)
    texts = splitter.split_documents(all_docs)
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
def retrieve_context(query: str, vectorstore: FAISS, k: int = 12, diversify_sources: bool = True) -> str:
    """
    Advanced RAG context retrieval: deduplicate, diversify, enrich metadata, allow dynamic k.
    """
    if vectorstore is None:
        logging.error("Vectorstore is not initialized. Cannot retrieve context.")
        return f"User Query: {query}\n\nRelevant Context:\nError: Vectorstore not available."
    try:
        logging.info(f"Performing similarity search for query: {query}")
        docs: List[Document] = vectorstore.similarity_search(query, k=k*3) # get more for dedup/diversity
        logging.info(f"Found {len(docs)} relevant documents before dedup/diversity.")

        # Deduplicate by title+source
        seen = set()
        deduped_docs = []
        for doc in docs:
            key = (doc.metadata.get('title', '').strip().lower(), doc.metadata.get('source', '').strip().lower())
            if key in seen:
                continue
            seen.add(key)
            deduped_docs.append(doc)
        logging.info(f"Deduplicated to {len(deduped_docs)} documents.")

        # Source diversity: try to balance sources
        if diversify_sources:
            by_source = {}
            for doc in deduped_docs:
                src = doc.metadata.get('source', 'unknown')
                by_source.setdefault(src, []).append(doc)
            # Round-robin select up to k
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

        # --- Boost by recency and query keyword match ---
        from datetime import datetime
        def parse_date(date_str):
            try:
                return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            except Exception:
                return datetime.min
        query_keywords = [w.lower() for w in query.split() if len(w) > 2]
        def boost_score(doc):
            score = 0
            title = doc.metadata.get('title', '').lower()
            content = doc.page_content.lower()
            if any(qk in title or qk in content for qk in query_keywords):
                score += 2
            if 'openai' in title or 'openai' in content:
                score += 3
            # Add more orgs if desired
            date_str = doc.metadata.get('published_date', '')
            score += (parse_date(date_str).timestamp() if date_str else 0) / 1e12
            return score
        docs_final.sort(key=boost_score, reverse=True)

        # Filter/prioritize context chunks mentioning AI, AI agents, or AI companies or query keywords
        keywords = ["ai", "artificial intelligence", "ai agent", "ai agents", "ai company", "ai companies"] + query_keywords
        def is_ai_related(text):
            text_lower = text.lower()
            return any(kw in text_lower for kw in keywords)
        filtered_docs = [doc for doc in docs_final if is_ai_related(doc.page_content) or is_ai_related(doc.metadata.get('title', ''))]
        # Loosen filtering: if at least 1, use, else fallback to top k most relevant
        if len(filtered_docs) >= 1:
            docs_to_use = filtered_docs[:k]
        else:
            # Fallback: always provide top k most relevant context
            docs_to_use = docs_final[:k]
        # TODO: Integrate more sources (OpenAI blog, AI news, etc) in data_loader.py and indexing.

        # Format context
        context_parts = []
        for i, doc in enumerate(docs_to_use):
            title = doc.metadata.get('title', 'No Title')
            source = doc.metadata.get('source', 'Unknown Source')
            url = doc.metadata.get('url', 'No URL Available')
            published_date = doc.metadata.get('published_date', 'No Date Available')
            content = doc.page_content
            context_parts.append(f"--- Document {i+1} ---\n")
            context_parts.append(f"Title: {title}\n")
            context_parts.append(f"Source: {source}\n")
            if url != 'No URL Available':
                context_parts.append(f"URL: {url}\n")
            if published_date != 'No Date Available':
                context_parts.append(f"Published: {published_date}\n")
            context_parts.append(f"Content: {content}\n")
        context = "\n".join(context_parts)
        formatted_context_prompt = f"""
You are an expert AI/ML/LLM research assistant.
STRICT INSTRUCTIONS:
- ONLY answer using the information provided in the context below.
- If the answer is not found in the context, reply: 'Sorry, the answer was not found in the provided research context.'
- Do NOT use prior knowledge or make up answers.
- Always cite the source title and URL for any fact.

---
[RESEARCH CONTEXT]
{context}
---
[USER QUESTION]
{query}
---
Provide a brief, accurate answer using only the context above. If not found, say so.
"""
        return formatted_context_prompt
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

    # Step 1: Retrieve relevant context based on the user's query
    # Pass the global vectorstore object to the retrieval function
    # Check if vectorstore was initialized successfully
    if 'vectorstore' not in globals() or vectorstore is None:
         logging.error("Vectorstore is not available. Cannot process query.")
         return "Error: Research index not available. Please check backend startup logs."

    rag_prompt_with_context = retrieve_context(query, vectorstore)
    logging.info("Context retrieval step completed.")
    # Optional: Log the full prompt being sent to the LLM (can be verbose)
    # logging.debug(f"Full prompt sent to LLM:\n{rag_prompt_with_context}")


    try:
        # Step 2: Pass the context-augmented prompt to the selected model
        if model == "gemini":
            logging.info("Calling Gemini model with unified RAG prompt...")
            try:
                from gemini_client import gemini_query
                response = await gemini_query(rag_prompt_with_context)
                logging.info("Received response from Gemini.")
                return response
            except Exception as e:
                logging.error(f"Error calling Gemini: {e}", exc_info=True)
                return f"Error calling Gemini: {e}"

        elif model == "deepseek":
            logging.info("Calling DeepSeek model with unified RAG prompt...")
            try:
                from openrouter_client import openrouter_query
                response = openrouter_query(rag_prompt_with_context)
                logging.info("Received response from DeepSeek.")
                return response
            except Exception as e:
                logging.error(f"Error calling DeepSeek: {e}", exc_info=True)
                return f"Error calling DeepSeek: {e}"


        else:
            logging.warning(f"Unsupported model selected: {model}")
            return "Unsupported model selected." # Returns a string

    except Exception as e:
        logging.error(f"Error in get_research_answer: {e}", exc_info=True) # Log traceback
        # Return an error message string so the FastAPI endpoint receives a serializable value.
        # This prevents the JSON encoding error in the endpoint.
        return f"An error occurred while fetching the answer: {e}"
        # If you prefer the FastAPI endpoint to catch and handle the exception:
        # raise # Re-raise the exception (but you'd need error handling in the endpoint)