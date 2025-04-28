import aiohttp
import asyncio
import feedparser
from newspaper import Article
from datetime import datetime
from data_sources_config import AI_SOURCES

async def fetch_rss(session, source):
    try:
        async with session.get(source['url']) as resp:
            text = await resp.text()
        feed = feedparser.parse(text)
        items = []
        for entry in feed.entries:
            items.append({
                'title': entry.title,
                'summary': getattr(entry, 'summary', ''),
                'published_date': getattr(entry, 'published', ''),
                'url': entry.link,
                'source': source['name'],
                'company': source.get('company', ''),
                'type': source['type']
            })
        return items
    except Exception as e:
        print(f"Error fetching {source['name']}: {e}")
        return []

async def fetch_article_content(session, url):
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
