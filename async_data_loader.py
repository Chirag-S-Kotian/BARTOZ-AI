import aiohttp
import asyncio
import feedparser
from newspaper import Article
from datetime import datetime
from data_sources_config import AI_SOURCES

import hashlib
import os

CACHE_DIR = 'cache'
os.makedirs(CACHE_DIR, exist_ok=True)

async def fetch_article_content(session, url, timeout=10):
    # Use a simple file cache to avoid refetching content
    cache_key = hashlib.md5(url.encode()).hexdigest()
    cache_path = os.path.join(CACHE_DIR, cache_key + '.txt')
    if os.path.exists(cache_path):
        with open(cache_path, 'r', encoding='utf-8') as f:
            return f.read()
    try:
        article = Article(url)
        article.download()
        article.parse()
        text = article.text[:2000]
        with open(cache_path, 'w', encoding='utf-8') as f:
            f.write(text)
        return text
    except Exception:
        return ''

async def fetch_rss(session, source):
    try:
        async with session.get(source['url'], timeout=10) as resp:
            text = await resp.text()
        feed = feedparser.parse(text)
        items = []
        # Limit to top 25 items for speed
        entries = feed.entries[:25]
        # Fetch article content concurrently for all entries
        tasks = [fetch_article_content(session, entry.link, timeout=10) for entry in entries]
        contents = await asyncio.gather(*tasks, return_exceptions=True)
        for entry, content in zip(entries, contents):
            if isinstance(content, Exception):
                content = ''
            items.append({
                'title': entry.title,
                'summary': getattr(entry, 'summary', ''),
                'published_date': getattr(entry, 'published', ''),
                'url': entry.link,
                'source': source['name'],
                'company': source.get('company', ''),
                'type': source['type'],
                'content': content
            })
        return items
    except Exception as e:
        print(f"Error fetching {source['name']}: {e}")
        return []

    # Try to fetch and extract full article content using newspaper3k
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text[:2000]  # Limit to 2000 chars
    except Exception:
        return ''

async def fetch_all_sources():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_rss(session, source) for source in AI_SOURCES]
        all_results = await asyncio.gather(*tasks)
        # Flatten and deduplicate by URL
        all_items = {}
        for items in all_results:
            for item in items:
                all_items[item['url']] = item
        return list(all_items.values())

if __name__ == "__main__":
    results = asyncio.run(fetch_all_sources())
    print(f"Fetched {len(results)} resources from {len(AI_SOURCES)} sources.")
    for r in results[:5]:
        print(r['title'], r['url'])
