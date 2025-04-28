# List of pluggable RSS/news/blog sources for AI/ML/LLM companies and research
AI_SOURCES = [
    # Company blogs
    {"name": "OpenAI Blog", "url": "https://openai.com/blog/rss.xml", "type": "blog", "company": "OpenAI"},
    {"name": "Google AI Blog", "url": "https://ai.googleblog.com/feeds/posts/default?alt=rss", "type": "blog", "company": "Google"},
    {"name": "Meta AI Blog", "url": "https://ai.facebook.com/blog/rss/", "type": "blog", "company": "Meta"},
    {"name": "Microsoft Research Blog", "url": "https://www.microsoft.com/en-us/research/feed/", "type": "blog", "company": "Microsoft"},
    {"name": "Hugging Face Blog", "url": "https://huggingface.co/blog/feed.xml", "type": "blog", "company": "Hugging Face"},
    {"name": "Stability AI Blog", "url": "https://stability.ai/blog/rss.xml", "type": "blog", "company": "Stability AI"},
    # Newsletters
    {"name": "The Batch (deeplearning.ai)", "url": "https://www.deeplearning.ai/the-batch/feed/rss/", "type": "newsletter", "company": "deeplearning.ai"},
    {"name": "The Gradient", "url": "https://thegradient.pub/rss/", "type": "newsletter", "company": "The Gradient"},
    {"name": "VentureBeat AI", "url": "https://venturebeat.com/category/ai/feed/", "type": "news", "company": "VentureBeat"},
    # Research
    {"name": "arXiv AI", "url": "http://export.arxiv.org/api/query?search_query=cat:cs.AI&start=0&max_results=100", "type": "research", "company": "arXiv"},
    # Add more sources as needed
]
