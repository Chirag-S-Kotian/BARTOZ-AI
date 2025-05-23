### data_loader.py

import requests
from bs4 import BeautifulSoup
import feedparser
from datetime import datetime

# --- Enriched AI/ML/LLM Company Info Loader ---
def fetch_ai_companies():
    """
    Returns a list of major AI/ML/LLM companies and labs with enriched metadata for accurate context.
    """
    # Example static data; in production, you can scrape or use APIs for live updates
    companies = [
        # --- AI Agent Projects/Frameworks ---
        {
            "name": "Auto-GPT",
            "description": "Auto-GPT is an experimental open-source application demonstrating the capabilities of the GPT-4 language model to autonomously achieve goals.",
            "founded": 2023,
            "founders": ["Significant Gravitas (Toran Bruce Richards)"],
            "headquarters": "Remote/Open Source",
            "website": "https://github.com/Significant-Gravitas/Auto-GPT",
            "category": "agent",
            "source": "ai_agent",
            "rss": "https://github.com/Significant-Gravitas/Auto-GPT/releases.atom",
            "active_years": "2023-2025",
            "top_in_year": [2023, 2024, 2025]
        },
        {
            "name": "BabyAGI",
            "description": "BabyAGI is a simple AI-powered task management system inspired by the concept of an AI agent that can create, prioritize, and execute tasks.",
            "founded": 2023,
            "founders": ["Yohei Nakajima"],
            "headquarters": "Remote/Open Source",
            "website": "https://github.com/yoheinakajima/babyagi",
            "category": "agent",
            "source": "ai_agent",
            "rss": "https://github.com/yoheinakajima/babyagi/releases.atom",
            "active_years": "2023-2025",
            "top_in_year": [2024, 2025]
        },
        {
            "name": "AgentGPT",
            "description": "AgentGPT allows you to configure and deploy autonomous AI agents in your browser.",
            "founded": 2023,
            "founders": ["Reworkd"],
            "headquarters": "Remote/Open Source",
            "website": "https://agentgpt.reworkd.ai/",
            "category": "agent",
            "source": "ai_agent",
            "rss": "",
            "active_years": "2023-2025",
            "top_in_year": [2025]
        },
        {
            "name": "LangChain Agents",
            "description": "LangChain Agents enable LLMs to make decisions and take actions autonomously, integrating with tools and APIs.",
            "founded": 2022,
            "founders": ["Harrison Chase"],
            "headquarters": "Remote/Open Source",
            "website": "https://python.langchain.com/docs/modules/agents",
            "category": "agent",
            "source": "ai_agent",
            "rss": "https://langchain.com/blog/rss.xml",
            "active_years": "2022-2025",
            "top_in_year": [2023, 2024, 2025]
        },
        {
            "name": "CrewAI",
            "description": "CrewAI is a framework for orchestrating collaborative multi-agent LLM systems to solve complex tasks.",
            "founded": 2024,
            "founders": ["CrewAI Community"],
            "headquarters": "Remote/Open Source",
            "website": "https://crewai.com/",
            "category": "agent",
            "source": "ai_agent",
            "rss": "https://github.com/joaomdmoura/crewAI/releases.atom",
            "active_years": "2024-2025",
            "top_in_year": [2025]
        },
        # --- Major Companies ---
        {
            "name": "OpenAI",
            "description": "OpenAI is an AI research and deployment company, creator of GPT-3, GPT-4, ChatGPT, and DALL·E.",
            "founded": 2015,
            "founders": ["Sam Altman", "Elon Musk", "Greg Brockman", "Ilya Sutskever", "Wojciech Zaremba", "John Schulman"],
            "headquarters": "San Francisco, CA, USA",
            "website": "https://openai.com",
            "category": "company",
            "source": "openai_company",
            "rss": "https://openai.com/blog/rss.xml",
            "products": ["GPT-3", "GPT-4", "ChatGPT", "DALL·E 2", "DALL·E 3", "Whisper"],
            "ceo": "Sam Altman",
            "notable_projects": ["ChatGPT", "DALL·E", "Codex", "OpenAI Gym"],
            "valuation": "$80-90B (2023)",
            "funding": "$11.3B+",
            "twitter": "https://twitter.com/openai",
            # Defensive: only call fetch_openai_blog(1) once and check for result
            "latest_blog": (lambda blogs: blogs[0] if blogs else {"title": "See OpenAI blog", "url": "https://openai.com/blog"})(fetch_openai_blog(1) if 'fetch_openai_blog' in globals() else [])
        },
        {
            "name": "DeepMind",
            "description": "DeepMind, a subsidiary of Alphabet, is known for AlphaGo, AlphaFold, and pioneering deep RL research.",
            "founded": 2010,
            "founders": ["Demis Hassabis", "Shane Legg", "Mustafa Suleyman"],
            "headquarters": "London, UK",
            "website": "https://deepmind.com",
            "category": "company",
            "source": "deepmind_company",
            "rss": "https://deepmind.com/blog/feed/basic/",
            "products": ["AlphaGo", "AlphaFold", "AlphaStar", "Gato", "Gemini (with Google)"],
            "ceo": "Demis Hassabis",
            "notable_projects": ["AlphaGo", "AlphaFold", "WaveNet", "Gemini"],
            "valuation": "Acquired by Google for ~$500M (2014)",
            "funding": "Acquired by Google",
            "twitter": "https://twitter.com/DeepMind",
            "latest_blog": {"title": "See DeepMind blog", "url": "https://deepmind.com/blog"}
        },
        {
            "name": "Anthropic",
            "description": "Anthropic is an AI safety and research company, creator of Claude LLMs, focused on alignment and reliability.",
            "founded": 2021,
            "founders": ["Dario Amodei", "Daniela Amodei", "Tom Brown", "Sam McCandlish", "Jared Kaplan"],
            "headquarters": "San Francisco, CA, USA",
            "website": "https://www.anthropic.com",
            "category": "company",
            "source": "anthropic_company",
            "rss": "https://www.anthropic.com/news/rss.xml",
            "products": ["Claude 2", "Claude 3", "Claude 3.5 Sonnet", "Claude 3.5 Haiku", "Claude Instant"],
            "ceo": "Dario Amodei",
            "notable_projects": ["Claude", "Claude 3", "Claude 2", "Claude Instant", "Claude Pro"],
            "valuation": "$18B (2024)",
            "funding": "$7.3B+",
            "twitter": "https://twitter.com/AnthropicAI",
            "latest_blog": {"title": "See Anthropic news", "url": "https://www.anthropic.com/news"},
            "resources": [
                {"title": "Detecting and Countering Malicious Uses of Claude: March 2025", "url": "https://www.anthropic.com/news/detecting-and-countering-malicious-uses-of-claude-march-2025"},
                {"title": "Our Approach to Understanding and Addressing AI Harms", "url": "https://www.anthropic.com/news/our-approach-to-understanding-and-addressing-ai-harms"},
                {"title": "Claude takes research to new places", "url": "https://www.anthropic.com/news/research"},
                {"title": "Anthropic Economic Index: Insights from Claude 3.7 Sonnet", "url": "https://www.anthropic.com/news/anthropic-economic-index-insights-from-claude-sonnet-3-7"},
                {"title": "Claude 3.7 Sonnet and Claude Code", "url": "https://www.anthropic.com/news/claude-3-7-sonnet"},
                {"title": "Claude’s extended thinking", "url": "https://www.anthropic.com/research/visible-extended-thinking"},
                {"title": "Anthropic achieves ISO 42001 certification for responsible AI", "url": "https://www.anthropic.com/news/anthropic-achieves-iso-42001-certification-for-responsible-ai"},
                {"title": "Alignment faking in large language models", "url": "https://www.anthropic.com/research/alignment-faking"},
                {"title": "Claude 3.5 Haiku on AWS Trainium2 and model distillation in Amazon Bedrock", "url": "https://www.anthropic.com/news/trainium2-and-distillation"},
                {"title": "Introducing Citations on the Anthropic API", "url": "https://www.anthropic.com/news/introducing-citations-api"},
                {"title": "Claude 3.5 Sonnet on GitHub Copilot", "url": "https://www.anthropic.com/news/github-copilot"},
                {"title": "Introducing Claude for Education", "url": "https://www.anthropic.com/news/introducing-claude-for-education"},
                {"title": "Claude can now search the web", "url": "https://www.anthropic.com/news/web-search"},
                {"title": "Claude 3 models on Vertex AI", "url": "https://www.anthropic.com/news/google-vertex-general-availability"},
                {"title": "Claude 3 Haiku: our fastest model yet", "url": "https://www.anthropic.com/news/claude-3-haiku"},
                {"title": "Introducing the next generation of Claude", "url": "https://www.anthropic.com/news/claude-3-family"},
                {"title": "Long context prompting for Claude 2.1", "url": "https://www.anthropic.com/news/claude-2-1-prompting"},
                {"title": "Introducing Claude 2.1", "url": "https://www.anthropic.com/news/claude-2-1"},
                {"title": "Claude on Amazon Bedrock now available to every AWS customer", "url": "https://www.anthropic.com/news/amazon-bedrock-general-availability"},
                {"title": "Introducing Claude Pro", "url": "https://www.anthropic.com/news/claude-pro"},
                {"title": "Claude 2 on Amazon Bedrock", "url": "https://www.anthropic.com/news/claude-2-amazon-bedrock"},
                {"title": "Releasing Claude Instant 1.2", "url": "https://www.anthropic.com/news/releasing-claude-instant-1-2"},
                {"title": "Frontier Threats Red Teaming for AI Safety", "url": "https://www.anthropic.com/news/frontier-threats-red-teaming-for-ai-safety"},
                {"title": "Claude’s Constitution", "url": "https://www.anthropic.com/news/claudes-constitution"},
                {"title": "Introducing 100K Context Windows", "url": "https://www.anthropic.com/news/100k-context-windows"},
                {"title": "Claude, now in Slack", "url": "https://www.anthropic.com/news/claude-now-in-slack"},
                {"title": "Introducing Claude", "url": "https://www.anthropic.com/news/introducing-claude"},
                {"title": "Core Views on AI Safety: When, Why, What, and How", "url": "https://www.anthropic.com/news/core-views-on-ai-safety"},
                {"title": "Anthropic Partners with Google Cloud", "url": "https://www.anthropic.com/news/anthropic-partners-with-google-cloud"},
                {"title": "Anthropic Raises Series B to Build Steerable, Interpretable, Robust AI Systems", "url": "https://www.anthropic.com/news/anthropic-raises-series-b-to-build-safe-reliable-ai"},
                {"title": "Anthropic raises $124 million to build more reliable, general AI systems", "url": "https://www.anthropic.com/news/anthropic-raises-124-million-to-build-more-reliable-general-ai-systems"}
            ]
        },
        {
            "name": "Cohere",
            "description": "Cohere builds large language models and NLP APIs for enterprises, focusing on retrieval-augmented generation and multilingual AI.",
            "founded": 2019,
            "founders": ["Aidan Gomez", "Ivan Zhang", "Nick Frosst", "Sasha Luccioni"],
            "headquarters": "Toronto, Canada",
            "website": "https://cohere.com",
            "category": "company",
            "source": "cohere_company",
            "rss": "https://txt.cohere.com/rss/",
            "products": ["Command R", "Embed", "Generate"],
            "ceo": "Aidan Gomez",
            "notable_projects": ["Command R", "Multilingual Embeddings"],
            "valuation": "$2.2B (2023)",
            "funding": "$445M+",
            "twitter": "https://twitter.com/cohere",
            "latest_blog": {"title": "See Cohere blog", "url": "https://txt.cohere.com/"}
        },
        {
            "name": "Hugging Face",
            "description": "Hugging Face is an open-source AI platform and community, home to the Transformers library and Model Hub.",
            "founded": 2016,
            "founders": ["Clément Delangue", "Julien Chaumond", "Thomas Wolf"],
            "headquarters": "New York, NY, USA",
            "website": "https://huggingface.co",
            "category": "company",
            "source": "huggingface_company",
            "rss": "https://huggingface.co/blog/feed.xml",
            "products": ["Transformers", "Diffusers", "Datasets", "Spaces"],
            "ceo": "Clément Delangue",
            "notable_projects": ["Transformers Library", "Model Hub", "Spaces"],
            "valuation": "$4.5B (2023)",
            "funding": "$395M+",
            "twitter": "https://twitter.com/huggingface",
            "latest_blog": {"title": "See Hugging Face blog", "url": "https://huggingface.co/blog"}
        },
        {
            "name": "Stability AI",
            "description": "Stability AI is the creator of Stable Diffusion and other open generative models for images, language, and audio.",
            "founded": 2020,
            "founders": ["Emad Mostaque"],
            "headquarters": "London, UK",
            "website": "https://stability.ai",
            "category": "company",
            "source": "stabilityai_company",
            "rss": "https://stability.ai/blog/rss.xml",
            "products": ["Stable Diffusion", "StableLM", "Stable Audio"],
            "ceo": "Emad Mostaque (as of 2023)",
            "notable_projects": ["Stable Diffusion", "StableLM"],
            "valuation": "$1B+ (2023)",
            "funding": "$125M+",
            "twitter": "https://twitter.com/StabilityAI",
            "latest_blog": {"title": "See Stability AI blog", "url": "https://stability.ai/blog"}
        },
        {
            "name": "Google Research",
            "description": "Google Research advances the state of the art in AI, ML, and LLMs, including BERT, PaLM, and Gemini.",
            "founded": 2006,
            "founders": ["Google Inc."],
            "headquarters": "Mountain View, CA, USA",
            "website": "https://research.google",
            "category": "company",
            "source": "google_company",
            "rss": "https://blog.research.google/atom.xml",
            "products": ["BERT", "PaLM", "Gemini", "Imagen"],
            "ceo": "Sundar Pichai (Alphabet)",
            "notable_projects": ["BERT", "PaLM", "Gemini"],
            "valuation": "Part of Alphabet ($1.7T+)",
            "funding": "Public company",
            "twitter": "https://twitter.com/GoogleAI",
            "latest_blog": {"title": "See Google Research blog", "url": "https://blog.research.google/"}
        },
        {
            "name": "Microsoft Research",
            "description": "Microsoft Research is a global leader in AI and ML, collaborating on OpenAI and developing Azure AI services.",
            "founded": 1991,
            "founders": ["Bill Gates"],
            "headquarters": "Redmond, WA, USA",
            "website": "https://www.microsoft.com/en-us/research/",
            "source": "microsoft_company",
            "rss": "https://www.microsoft.com/en-us/research/feed/",
            "products": ["Azure AI", "Copilot", "Turing-NLG"],
            "ceo": "Satya Nadella (Microsoft)",
            "notable_projects": ["OpenAI Partnership", "Azure AI", "Copilot"],
            "valuation": "$2.8T+ (Microsoft, 2024)",
            "funding": "Public company",
            "twitter": "https://twitter.com/msftresearch",
            "latest_blog": {"title": "See Microsoft Research blog", "url": "https://www.microsoft.com/en-us/research/blog/"}
        }
    ]

    # Optionally, fetch and enrich with latest blog/news headlines
    enriched = []
    for comp in companies:
        # Try to fetch latest blog title
        latest_title = ""
        try:
            feed = feedparser.parse(comp["rss"])
            if feed.entries:
                latest_title = feed.entries[0].title
        except Exception:
            pass
        comp["latest_blog_title"] = latest_title
        enriched.append(comp)
    return enriched

def fetch_arxiv(keyword="AI", max_results=10):
    url = f"http://export.arxiv.org/api/query?search_query=all:{keyword}&start=0&max_results={max_results}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "xml")
    entries = soup.find_all("entry")
    papers = []
    for entry in entries:
        papers.append({
            "title": entry.title.text.strip(),
            "summary": entry.summary.text.strip(),
            "source": "arxiv"
        })
    return papers

def fetch_pubmed(keyword="AI", max_results=10):
    search_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    search_params = {
        "db": "pubmed",
        "term": keyword,
        "retmax": max_results,
        "retmode": "json"
    }
    search_res = requests.get(search_url, params=search_params).json()
    ids = ",".join(search_res["esearchresult"]["idlist"])

    fetch_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    fetch_params = {
        "db": "pubmed",
        "id": ids,
        "retmode": "json"
    }
    fetch_res = requests.get(fetch_url, params=fetch_params).json()
    papers = []
    for uid in fetch_res["result"]["uids"]:
        doc = fetch_res["result"][uid]
        papers.append({
            "title": doc.get("title", ""),
            "summary": doc.get("source", ""),
            "source": "pubmed"
        })
    return papers

def fetch_ssrn(keyword="AI"):
    search_url = f"https://papers.ssrn.com/sol3/results.cfm?txtKey_Words={keyword}"
    res = requests.get(search_url)
    soup = BeautifulSoup(res.text, "html.parser")
    papers = []
    for div in soup.select(".title")[:10]:
        papers.append({
            "title": div.get_text(strip=True),
            "summary": "Abstract not available via HTML scraping",
            "source": "ssrn"
        })
    return papers

def fetch_openai_blog(max_results=200):
    """Fetch latest posts from OpenAI blog RSS feed."""
    feed_url = "https://openai.com/blog/rss.xml"
    feed = feedparser.parse(feed_url)
    posts = []
    for entry in feed.entries[:max_results]:
        posts.append({
            "title": entry.title,
            "summary": entry.summary if hasattr(entry, 'summary') else '',
            "published_date": entry.published if hasattr(entry, 'published') else '',
            "source": "openai_blog",
            "url": entry.link
        })
    return posts

def fetch_the_batch_newsletter(max_results=200):
    """Fetch latest posts from The Batch (deeplearning.ai) newsletter RSS feed."""
    feed_url = "https://www.deeplearning.ai/the-batch/feed/rss/"
    feed = feedparser.parse(feed_url)
    posts = []
    for entry in feed.entries[:max_results]:
        posts.append({
            "title": entry.title,
            "summary": entry.summary if hasattr(entry, 'summary') else '',
            "published_date": entry.published if hasattr(entry, 'published') else '',
            "source": "the_batch_newsletter",
            "url": entry.link
        })
    return posts