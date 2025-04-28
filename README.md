<p align="center">
  <img src="https://raw.githubusercontent.com/Chirag-S-Kotian/BARTOZ-AI/main/.github/assets/animated-neural-net.svg" alt="Animated Neural Network" width="600"/>
</p>

# 🧠 BARTOZ-AI: Open Source AI/LLM/Agent Research Assistant

<p align="center">
  <a href="https://github.com/Chirag-S-Kotian/BARTOZ-AI">
    <img alt="GitHub stars" src="https://img.shields.io/github/stars/Chirag-S-Kotian/BARTOZ-AI?style=social">
  </a>
  <a href="https://github.com/Chirag-S-Kotian/BARTOZ-AI/blob/main/LICENSE">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-blue.svg">
  </a>
  <img alt="Python Version" src="https://img.shields.io/badge/python-3.9%2B-blue">
  <img alt="LangChain" src="https://img.shields.io/badge/Made%20with-LangChain-4B275F?logo=langchain">
  <img alt="Streamlit" src="https://img.shields.io/badge/UI-Streamlit-FF4B4B?logo=streamlit">
  <img alt="Gemini" src="https://img.shields.io/badge/LLM-Gemini-4285F4?logo=google">
  <img alt="DeepSeek" src="https://img.shields.io/badge/LLM-DeepSeek-00897B">
  <img alt="Async" src="https://img.shields.io/badge/Async-Enabled-8BC34A">
</p>

---

> <span style="font-size:1.1em;">BARTOZ-AI is a modern, open-source Retrieval-Augmented Generation (RAG) system focused on <b>AI, LLMs, agents, and major AI companies</b>. It combines scalable async ingestion (1000+ docs), robust deduplication, and a beautiful Streamlit UI, powered by Gemini and DeepSeek models. <b>Always up-to-date, always cited.</b></span>
[![Open Source](https://img.shields.io/badge/Open%20Source-Yes-brightgreen)](https://github.com/Chirag-S-Kotian/BARTOZ-AI)
[![Stars](https://img.shields.io/github/stars/Chirag-S-Kotian/BARTOZ-AI?style=social)](https://github.com/Chirag-S-Kotian/BARTOZ-AI/stargazers)

---

## 📚 Table of Contents

- [Why BARTOZ-AI?](#-why-bartoz-ai)
- [Features](#-features)
- [Quickstart](#-quickstart)
- [Architecture Overview](#-architecture-overview)
- [Project Structure](#-project-structure)
- [Setup & Usage](#-setup--usage)
- [Demo Commands](#-demo-commands)
- [Advanced Usage](#-advanced-usage)
- [Troubleshooting & FAQ](#-troubleshooting--faq)
- [Contributing](#-contributing)
- [License](#-license)

---

<details open>
<summary>🌟 <strong>Why BARTOZ-AI?</strong></summary>

> "Not just another chatbot."

| Feature                | BARTOZ-AI | Typical RAG | Proprietary AI Chatbot |
|------------------------|:---------:|:-----------:|:---------------------:|
| Async Ingestion        |    ✅     |      ❌      |          ❌           |
| Streamlit UI           |    ✅     |      ❌      |          ❌           |
| Gemini & DeepSeek      |    ✅     |      ❌      |          ❓           |
| 1000+ Docs/Run         |    ✅     |      ⚠️      |          ❌           |
| Source Cited Answers   |    ✅     |      ⚠️      |          ⚠️           |
| Easy Extensibility     |    ✅     |      ⚠️      |          ❌           |
| Open Source            |    ✅     |      ✅      |          ❌           |

> 💬 <b>Why settle for less?</b> BARTOZ-AI is designed for researchers, engineers, and enthusiasts who demand transparency, extensibility, and top-tier AI knowledge.
</details>

---

<details open>
<summary>🚀 <strong>Features</strong></summary>

> <img src="https://img.shields.io/badge/-AI%20Research%20Assistant-blueviolet?style=flat-square&logo=ai" align="left" />
> 
> <b>BARTOZ-AI</b> offers a modern async RAG pipeline, beautiful UI, and up-to-date, source-cited answers about AI, LLMs, agents, and companies. 
> 
> <span style="color:#43a047;"><b>✨ Scalable, extensible, and open source.</b></span>

- **Async Data Loader**: Ingests 1000+ docs from arXiv, company blogs, news, and more (see `data_sources_config.py`).
- **Modern RAG Pipeline**: Unified context for Gemini & DeepSeek; scalable vectorstore (FAISS).
- **Beautiful Streamlit UI**: Responsive, theme toggle, live model health, database preview.
- **Extensible Sources**: Add any RSS/news/blog/research feed in `data_sources_config.py`.
- **Automated Scheduler**: (Optional) Schedule daily/weekly re-indexing with `scheduler.py`.
- **FastAPI Backend**: Robust API for querying, health, preview, and source listing.
- **Open Source & Easy to Extend**: Add new models, sources, or UI features easily.

</details>

---

<details>
<summary>⚡ <strong>Quickstart</strong></summary>

```sh
# 1. Clone & Install
$ git clone https://github.com/Chirag-S-Kotian/BARTOZ-AI.git
$ cd BARTOZ-AI
$ python3 -m venv venv && source venv/bin/activate
$ pip install -r requirements.txt

# 2. Set API Keys (.env)
OPENROUTER_API_KEY=your-openrouter-key
GEMINI_API_KEY=your-gemini-key

# 3. Ingest & Index
$ python rag_pipeline.py

# 4. Start Backend
$ uvicorn main:app --reload --port 8000

# 5. Launch Frontend
$ streamlit run frontend/app.py
```

</details>

---

<details>
<summary>🏗️ <strong>Architecture Overview</strong></summary>

```
[ User (Streamlit UI) ]
     ↓
[ FastAPI Backend ]
     ↓
[ RAG Pipeline: async_data_loader.py + rag_pipeline.py ]
     ↓
[ FAISS Vectorstore ]
     ↓
[ Gemini / DeepSeek Model ]
     ↓
[ Answer + Sources ]
```

**Key Components:**
- `async_data_loader.py`: Async ingestion, deduplication, scalable document fetching
- `rag_pipeline.py`: Indexing, context building, vectorstore management
- `frontend/app.py`: Streamlit UI (theme toggle, health check, preview, query)
- `main.py`: FastAPI backend (API endpoints)
- `gemini_client.py`, `openrouter_client.py`: Model adapters
- `data_sources_config.py`: All news/blog/company/research sources

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

</details>

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

## ✨ Features
- **Unified RAG pipeline:** Consistent context for Gemini & DeepSeek
- **Strict topic focus:** Only AI/ML/LLM/Agents/Companies
- **Live sources:** OpenAI, DeepMind, Anthropic, Cohere, Hugging Face, Stability, arXiv, PubMed, SSRN, The Batch, and more
- **Company/LLM metadata:** Founders, HQ, year, website, latest blog, and more
- **Modern Streamlit UI:** Beautiful landing page, GitHub star button, open source branding
- **Automated daily re-indexing**
- **Easy to extend**: Add new models, sources, or UI features easily.

---

<details>
<summary>🛠️ <strong>Setup</strong></summary>

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

- Set your API keys in `.env`:
  - `OPENROUTER_API_KEY` for DeepSeek
  - `GEMINI_API_KEY` for Gemini

</details>

---

<details>
<summary>🛠️ <strong>Setup & Usage</strong></summary>

Follow the Quickstart above, or see below for advanced configuration.

- **Add Sources:** Edit `data_sources_config.py` to plug in new RSS/news/blog feeds.
- **Extend Models:** Add new adapters in `gemini_client.py` or `openrouter_client.py`.
- **Automate:** Use `scheduler.py` for scheduled ingestion.

</details>

---

1. **Clone and Install**
   ```bash
   git clone https://github.com/Chirag-S-Kotian/BARTOZ-AI.git
   cd BARTOZ-AI
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Set API Keys**
   - Create `.env` in project root:
     ```
     OPENROUTER_API_KEY=your-openrouter-key
     GEMINI_API_KEY=your-gemini-key
     ```
3. **Ingest & Index**
   ```bash
   python rag_pipeline.py
   # (Optional: schedule with python scheduler.py)
   ```
4. **Start Backend**
   ```bash
   uvicorn main:app --reload --port 8000
   ```
5. **Launch Frontend**
   ```bash
   streamlit run frontend/app.py
   ```

---

<details>
<summary>💡 <strong>Advanced Usage</strong></summary>

> 💡 <b>Tip:</b> To maximize document coverage, increase <code>max_docs</code> in <code>fetch_all_sources()</code> or add sources in <code>data_sources_config.py</code>. Use <code>scheduler.py</code> for automation.

- **API Endpoints:**
  - `/query`, `/model_health`, `/db_size`, `/docs_preview`, `/sources`
- **Change UI Theme:** Use the theme toggle in the sidebar.
- **Preview DB:** Use the sidebar "Preview Database" button.

</details>

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

### 4. Query Gemini or DeepSeek Directly
```python
from openrouter_client import openrouter_query
from gemini_client import gemini_query

print(openrouter_query("What is the latest breakthrough by OpenAI?"))
# or
import asyncio
print(asyncio.run(gemini_query("Who are the leading AI agents in 2025?")))
```

---

<details>
<summary>🗂️ <strong>Project Structure</strong></summary>

```text
bartoz-ai/
├── async_data_loader.py   # Async fetch, deduplication, scalable ingestion
├── data_loader.py        # Company/agent/LLM metadata
├── rag_pipeline.py       # Indexing, context, embeddings, FAISS
├── data_sources_config.py# All RSS/news/blog sources
├── main.py               # FastAPI backend
├── frontend/
│   └── app.py            # Streamlit UI
├── gemini_client.py      # Gemini API client
├── openrouter_client.py  # DeepSeek/OpenRouter API client
├── requirements.txt
├── scheduler.py          # (Optional) Automated re-indexing
├── .env                  # API keys
├── faiss_index/          # Vectorstore
└── README.md
```

</details>

---

<details>
<summary>🤝 <strong>Contributing</strong></summary>

- Star ⭐ the repo and open issues/PRs for bugs, features, or new sources
- Suggest new sources or models (see `data_sources_config.py`)
- All contributions welcome!

</details>

---

<details>
<summary>🧩 <strong>Troubleshooting & FAQ</strong></summary>

- **Streamlit duplicate key error?**
  - Ensure every `st.button` or widget in `app.py` uses a unique `key` (especially in the sidebar).
- **How do I add more sources?**
  - Add new dicts to `AI_SOURCES` in `data_sources_config.py`.
- **How fresh is the data?**
  - Data is refreshed every time you run `rag_pipeline.py` (or via `scheduler.py`).
- **Can I use my own LLM?**
  - Yes! Add your API adapter and plug into the pipeline.
- **How do I cite sources in answers?**
  - All answers are cited with titles and URLs from the ingested context.

</details>

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.

---

## 🆘 Getting Help

- 💬 [GitHub Discussions](https://github.com/Chirag-S-Kotian/BARTOZ-AI/discussions) — Ask questions, get support, share ideas
- 🐞 [Issues](https://github.com/Chirag-S-Kotian/BARTOZ-AI/issues) — Report bugs or request features

---

## 🚧 Roadmap

- [ ] 🔄 Real-time ingestion with WebSockets
- [ ] 🌍 Multi-language support
- [ ] 🧑‍💻 Plugin system for custom data loaders
- [ ] 📊 Analytics dashboard for usage and data freshness
- [ ] 🧪 More LLM integrations (Claude, Llama, etc)
- [ ] 🛡️ Enhanced security & auth for enterprise use

---

## 👥 Contributors

<p align="left">
  <a href="https://github.com/Chirag-S-Kotian">
    <img src="https://avatars.githubusercontent.com/u/54731736?v=4" width="60px;" alt="Chirag S Kotian"/>
    <br /><sub><b>Chirag S Kotian</b></sub>
  </a>
  &nbsp;
  <a href="https://github.com/Chirag-S-Kotian/BARTOZ-AI/graphs/contributors">
    <img src="https://contrib.rocks/image?repo=Chirag-S-Kotian/BARTOZ-AI" alt="All Contributors"/>
  </a>
</p>

---

**Made with ❤️ by [Chirag S Kotian](https://github.com/Chirag-S-Kotian) — [Star us on GitHub!](https://github.com/Chirag-S-Kotian/BARTOZ-AI)**