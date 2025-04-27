### README.md

# AI Research Assistant (AI, Agents, Companies Only)

## Project Focus
This assistant exclusively answers questions about **AI, AI agents, and AI companies**. Any unrelated queries will be politely declined.

## Features
- Collects abstracts from arXiv, PubMed, and SSRN
- Embeds and stores them using FAISS and HuggingFace
- Supports semantic search and querying using Gemini or DeepSeek
- **Strict topic filtering:** Only AI, AI agents, and AI companies are considered for context and answers
- **Brief, accurate, up-to-date responses**
- **Source citation and URLs** in every answer
- **Unified RAG pipeline:** Both Gemini and DeepSeek use the same context and prompt template for consistent results

## Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run the Ingestion Pipeline
```bash
python rag_pipeline.py
```

## Query Gemini or DeepSeek
```python
from openrouter_client import query_deepseek
from gemini_client import query_gemini

# Only ask questions about AI, AI agents, or AI companies
print(query_deepseek("What is the latest breakthrough by OpenAI?"))
# or
import asyncio
print(asyncio.run(query_gemini("Who are the leading AI agents in 2025?")))
```

## Folder Structure
```
ai-research-assistant/
├── data_loader.py
├── rag_pipeline.py
├── openrouter_client.py
├── gemini_client.py
├── faiss_index/
│   ├── index.faiss
│   ├── index.pkl
│   └── metadata.json
├── requirements.txt
├── .env
└── README.md
```

You’re now ready to run queries on your indexed research with either AI model!

---

## Further Enhancements (Suggested)
- **More sources:** Add news feeds or company press releases for even more up-to-date AI info
- **Advanced citation formatting:** Inline citations or footnotes
- **Author and organization metadata:** Show who wrote each document
- **Interactive web UI:** Use Streamlit or similar for a user-friendly chat experience
- **User feedback loop:** Allow users to rate answers to improve retrieval and ranking
- **Real-time updates:** Periodically refresh the FAISS index with the latest AI research and news

---

**Note:** This assistant will only answer questions strictly about AI, AI agents, or AI companies, and will always provide concise, accurate, and up-to-date information with sources.