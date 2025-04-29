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
    import logging
    from bs4 import BeautifulSoup
    # Use a simple file cache to avoid refetching content
    cache_key = hashlib.md5(url.encode()).hexdigest()
    cache_path = os.path.join(CACHE_DIR, cache_key + '.txt')
    if os.path.exists(cache_path):
        with open(cache_path, 'r', encoding='utf-8') as f:
            return f.read()
    # Try newspaper3k first
    try:
        article = Article(url)
        article.download()
        article.parse()
        text = article.text.strip()
        # If text is too short, try fallback
        if len(text) < 200:
            raise Exception("Too short, fallback to BS4")
        with open(cache_path, 'w', encoding='utf-8') as f:
            f.write(text)
        logging.info(f"[Article Extraction] {url} | newspaper3k | length: {len(text)}")
        return text[:2000]
    except Exception:
        # Fallback: fetch raw HTML and parse with BeautifulSoup
        try:
            async with session.get(url, timeout=timeout) as resp:
                html = await resp.text()
            soup = BeautifulSoup(html, 'html.parser')
            # Try <article>, then <main>, then <body>
            main_content = ''
            for tag in ['article', 'main', 'body']:
                found = soup.find(tag)
                if found and found.get_text(strip=True):
                    main_content = found.get_text(separator=' ', strip=True)
                    break
            # Always extract metadata if possible
            title = (soup.title.string.strip() if soup.title else '')
            author = ''
            pubdate = ''
            summary = ''
            # Try Open Graph/meta tags for better metadata
            og_title = soup.find('meta', property='og:title')
            if og_title and og_title.get('content'): title = og_title['content']
            og_desc = soup.find('meta', property='og:description')
            if og_desc and og_desc.get('content'): summary = og_desc['content']
            meta_author = soup.find('meta', attrs={'name':'author'})
            if meta_author and meta_author.get('content'): author = meta_author['content']
            meta_date = soup.find('meta', attrs={'property':'article:published_time'}) or soup.find('meta', attrs={'name':'pubdate'})
            if meta_date and meta_date.get('content'): pubdate = meta_date['content']
            # Compose fallback text
            fallback_text = f"Title: {title}\nAuthor: {author}\nPublished: {pubdate}\nSummary: {summary}\nContent: {main_content[:2000]}"
            with open(cache_path, 'w', encoding='utf-8') as f:
                f.write(fallback_text)
            logging.info(f"[Article Extraction] {url} | BeautifulSoup | length: {len(main_content)}")
            return fallback_text
        except Exception as e:
            logging.warning(f"[Article Extraction] {url} | Extraction failed: {e}")
            return ''

async def fetch_rss(session, source, max_entries=200):
    import logging
    try:
        url = source['url']
        # Special handling for arXiv API: paginate to get more than 100 docs
        if 'arxiv.org/api' in url:
            items = []
            batch_size = 200
            total_to_fetch = max_entries
            for start in range(0, total_to_fetch, batch_size):
                paged_url = url.replace('start=0', f'start={start}').replace('max_results=100', f'max_results={batch_size}')
                async with session.get(paged_url, timeout=15) as resp:
                    text = await resp.text()
                feed = feedparser.parse(text)
                entries = feed.entries
                logging.info(f"Fetched {len(entries)} entries from arXiv (batch {start}-{start+batch_size})")
                tasks = [fetch_article_content(session, entry.link, timeout=12) for entry in entries]
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
                if len(items) >= max_entries:
                    break
            return items[:max_entries]
        # For other RSS feeds
        async with session.get(url, timeout=15) as resp:
            text = await resp.text()
        feed = feedparser.parse(text)
        items = []
        entries = feed.entries[:max_entries]
        logging.info(f"Fetched {len(entries)} entries from {source['name']}")
        tasks = [fetch_article_content(session, entry.link, timeout=12) for entry in entries]
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


# NOTE: On low-memory deployments (e.g., Render free tier), keep max_docs low (e.g., 30). Increase for production as needed.
async def fetch_all_sources(max_docs=30):
    import logging
    async with aiohttp.ClientSession() as session:
        # Distribute max_docs across sources (e.g., 12 sources × 3 each)
        per_source = max(3, max_docs // max(1, len(AI_SOURCES)))
        tasks = [fetch_rss(session, source, max_entries=per_source) for source in AI_SOURCES]
        all_results = await asyncio.gather(*tasks)
        # Flatten and deduplicate by URL
        all_items = {}
        total = 0
        for items in all_results:
            for item in items:
                if item['url'] not in all_items:
                    all_items[item['url']] = item
                    total += 1
        logging.info(f"Fetched and deduplicated total {total} documents from {len(AI_SOURCES)} sources.")
        # Limit to max_docs
        return list(all_items.values())[:max_docs]


if __name__ == "__main__":
    results = asyncio.run(fetch_all_sources())
    print(f"Fetched {len(results)} resources from {len(AI_SOURCES)} sources.")
    for r in results[:5]:
        print(r['title'], r['url'])
