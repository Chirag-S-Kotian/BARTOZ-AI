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
        {
            "name": "OpenAI",
            "description": "OpenAI is an AI research and deployment company, creator of GPT-3, GPT-4, ChatGPT, and DALL·E.",
            "founded": 2015,
            "founders": ["Sam Altman", "Elon Musk", "Greg Brockman", "Ilya Sutskever", "Wojciech Zaremba", "John Schulman"],
            "headquarters": "San Francisco, CA, USA",
            "website": "https://openai.com",
            "source": "openai_company",
            "rss": "https://openai.com/blog/rss.xml"
        },
        {
            "name": "DeepMind",
            "description": "DeepMind, a subsidiary of Alphabet, is known for AlphaGo, AlphaFold, and pioneering deep RL research.",
            "founded": 2010,
            "founders": ["Demis Hassabis", "Shane Legg", "Mustafa Suleyman"],
            "headquarters": "London, UK",
            "website": "https://deepmind.com",
            "source": "deepmind_company",
            "rss": "https://deepmind.com/blog/feed/basic/"
        },
        {
            "name": "Anthropic",
            "description": "Anthropic is an AI safety and research company, creator of Claude LLMs, focused on alignment and reliability.",
            "founded": 2021,
            "founders": ["Dario Amodei", "Daniela Amodei", "Tom Brown", "Sam McCandlish", "Jared Kaplan"],
            "headquarters": "San Francisco, CA, USA",
            "website": "https://www.anthropic.com",
            "source": "anthropic_company",
            "rss": "https://www.anthropic.com/news/rss.xml"
        },
        {
            "name": "Cohere",
            "description": "Cohere builds large language models and NLP APIs for enterprises, focusing on retrieval-augmented generation and multilingual AI.",
            "founded": 2019,
            "founders": ["Aidan Gomez", "Ivan Zhang", "Nick Frosst", "Sasha Luccioni"],
            "headquarters": "Toronto, Canada",
            "website": "https://cohere.com",
            "source": "cohere_company",
            "rss": "https://txt.cohere.com/rss/"
        },
        {
            "name": "Hugging Face",
            "description": "Hugging Face is an open-source AI platform and community, home to the Transformers library and Model Hub.",
            "founded": 2016,
            "founders": ["Clément Delangue", "Julien Chaumond", "Thomas Wolf"],
            "headquarters": "New York, NY, USA",
            "website": "https://huggingface.co",
            "source": "huggingface_company",
            "rss": "https://huggingface.co/blog/feed.xml"
        },
        {
            "name": "Stability AI",
            "description": "Stability AI is the creator of Stable Diffusion and other open generative models for images, language, and audio.",
            "founded": 2020,
            "founders": ["Emad Mostaque"],
            "headquarters": "London, UK",
            "website": "https://stability.ai",
            "source": "stabilityai_company",
            "rss": "https://stability.ai/blog/rss.xml"
        },
        {
            "name": "Google Research",
            "description": "Google Research advances the state of the art in AI, ML, and LLMs, including BERT, PaLM, and Gemini.",
            "founded": 2006,
            "founders": ["Google Inc."],
            "headquarters": "Mountain View, CA, USA",
            "website": "https://research.google",
            "source": "google_company",
            "rss": "https://blog.research.google/atom.xml"
        },
        {
            "name": "Microsoft Research",
            "description": "Microsoft Research is a global leader in AI and ML, collaborating on OpenAI and developing Azure AI services.",
            "founded": 1991,
            "founders": ["Bill Gates"],
            "headquarters": "Redmond, WA, USA",
            "website": "https://www.microsoft.com/en-us/research/",
            "source": "microsoft_company",
            "rss": "https://www.microsoft.com/en-us/research/feed/"
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

def fetch_openai_blog(max_results=10):
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

def fetch_the_batch_newsletter(max_results=10):
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