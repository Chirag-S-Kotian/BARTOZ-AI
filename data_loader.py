### data_loader.py

import requests
from bs4 import BeautifulSoup
import feedparser
from datetime import datetime

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