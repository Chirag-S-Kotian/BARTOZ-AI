# BARTOZ-AI: Open Source AI/ML/LLM Research Assistant

[![GitHub Repo](https://img.shields.io/badge/GitHub-BARTOZ--AI-181717?logo=github)](https://github.com/Chirag-S-Kotian/BARTOZ-AI)
[![Open Source](https://img.shields.io/badge/Open%20Source-Yes-brightgreen)](https://github.com/Chirag-S-Kotian/BARTOZ-AI)
[![Stars](https://img.shields.io/github/stars/Chirag-S-Kotian/BARTOZ-AI?style=social)](https://github.com/Chirag-S-Kotian/BARTOZ-AI/stargazers)

---

> **by [Chirag S Kotian](https://github.com/Chirag-S-Kotian)**

---

## 🚀 What is BARTOZ-AI?

**BARTOZ-AI** is a modern, open-source research assistant that answers questions strictly about:
- Artificial Intelligence (AI)
- Machine Learning (ML)
- Large Language Models (LLMs)
- AI Agents
- Major AI Companies & Labs

It combines Retrieval-Augmented Generation (RAG) with Gemini and DeepSeek models, and always provides up-to-date, source-cited answers.

---

## ✨ Features
- **Unified RAG pipeline:** Consistent context for Gemini & DeepSeek
- **Strict topic focus:** Only AI/ML/LLM/Agents/Companies
- **Live sources:** OpenAI, DeepMind, Anthropic, Cohere, Hugging Face, Stability, arXiv, PubMed, SSRN, The Batch, and more
- **Company/LLM metadata:** Founders, HQ, year, website, latest blog, and more
- **Modern Streamlit UI:** Beautiful landing page, GitHub star button, open source branding
- **Automated daily re-indexing**
- **Easy to extend**: Add more sources or models

---

## 🖼️ Diagram: How BARTOZ-AI Works

```
[ User Query ]
      |
      v
[ Streamlit UI ]
      |
      v
[ FastAPI Backend ]
      |
      v
[ RAG Pipeline ]
      |
      +--> [ Vectorstore (FAISS) ]
      |        ^
      |        |
      |   [ Data Loader: arXiv, PubMed, SSRN, OpenAI, DeepMind, ... ]
      |
      v
[ Gemini or DeepSeek Model ]
      |
      v
[ Answer + Sources ]
```

---

## 🏢 Example Companies & Labs (auto-enriched)

| Name           | Founded | Founders                       | Headquarters        | Website                      | Latest Blog Title                |
|----------------|---------|-------------------------------|---------------------|------------------------------|----------------------------------|
| OpenAI         | 2015    | S. Altman, E. Musk, et al.    | San Francisco, USA  | https://openai.com           | (auto-fetched)                   |
| DeepMind       | 2010    | D. Hassabis, S. Legg, M. Suleyman | London, UK     | https://deepmind.com         | (auto-fetched)                   |
| Anthropic      | 2021    | D. Amodei, D. Amodei, et al.  | San Francisco, USA  | https://www.anthropic.com    | (auto-fetched)                   |
| Cohere         | 2019    | A. Gomez, I. Zhang, et al.    | Toronto, Canada     | https://cohere.com           | (auto-fetched)                   |
| Hugging Face   | 2016    | C. Delangue, J. Chaumond, T. Wolf | New York, USA  | https://huggingface.co       | (auto-fetched)                   |
| Stability AI   | 2020    | E. Mostaque                   | London, UK          | https://stability.ai         | (auto-fetched)                   |
| Google Research| 2006    | Google Inc.                   | Mountain View, USA  | https://research.google      | (auto-fetched)                   |
| Microsoft Research| 1991 | B. Gates                      | Redmond, USA        | https://microsoft.com/research| (auto-fetched)                 |

---

## 🛠️ Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

- Set your API keys in `.env`:
  - `OPENROUTER_API_KEY` for DeepSeek
  - `GEMINI_API_KEY` for Gemini

---

## ⚡ Usage

### 1. Run the Ingestion Pipeline
```bash
python rag_pipeline.py
```

### 2. Start the Backend
```bash
uvicorn main:app --reload --port 8000
```

### 3. Launch the Frontend
```bash
streamlit run frontend/app.py
```

---

### 4. Query Gemini or DeepSeek Directly
```python
from openrouter_client import query_deepseek
from gemini_client import query_gemini

print(query_deepseek("What is the latest breakthrough by OpenAI?"))
# or
import asyncio
print(asyncio.run(query_gemini("Who are the leading AI agents in 2025?")))
```

---

## 📂 Folder Structure
```
bartoz-ai/
├── data_loader.py
├── rag_pipeline.py
├── openrouter_client.py
├── gemini_client.py
├── frontend/
│   └── app.py
├── faiss_index/
│   ├── index.faiss
│   ├── index.pkl
│   └── metadata.json
├── requirements.txt
├── .env
├── scheduler.py
└── README.md
```

---

## 🤝 Contributing
- Star the repo ⭐ and open issues/PRs for features or bugfixes
- Suggest new sources or models
- All contributions welcome!

---

## 🙋 FAQ
- **Q: What questions does BARTOZ-AI answer?**
  - Only questions about AI, ML, LLMs, AI agents, or major AI companies/labs.
- **Q: How fresh is the info?**
  - Data is refreshed daily from top sources and news feeds.
- **Q: Can I add more sources?**
  - Yes! Edit `data_loader.py` to add more fetchers.

---

## 📣 License
MIT License. See [LICENSE](LICENSE) for details.

---

**Made with ❤️ by [Chirag S Kotian](https://github.com/Chirag-S-Kotian) — [Star us on GitHub!](https://github.com/Chirag-S-Kotian/BARTOZ-AI)**