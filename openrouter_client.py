from openai import OpenAI
import os
import requests # Import requests for better error handling
import aiohttp

# Initialize the OpenAI client pointing to OpenRouter API
# Ensure OPENROUTER_API_KEY is set in your environment
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY") # Get API key from environment variables
)

def openrouter_query(prompt: str) -> str:
    """
    Queries the DeepSeek model via OpenRouter API (sync version).
    Args:
        prompt: The user's prompt.
    Returns:
        The generated response from the model.
    """
    try:
        # Create a chat completion request
        response = client.chat.completions.create(
            model="deepseek/deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            extra_headers={
                "HTTP-Referer": "https://yourdomain.com",
                "X-Title": "AI Research Assistant"
            }
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error in openrouter_query: {e}")
        return f"Error querying OpenRouter (DeepSeek): {e}"

async def openrouter_query_async(prompt: str) -> str:
    """
    Async version of DeepSeek (OpenRouter) query for use in async pipelines.
    Args:
        prompt: The user's prompt.
    Returns:
        The generated response from the model.
    """
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return "Error: OPENROUTER_API_KEY is not configured."
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://yourdomain.com",
        "X-Title": "AI Research Assistant",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek/deepseek-chat",
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload, timeout=60) as resp:
                if resp.status != 200:
                    return f"Error: OpenRouter API returned status {resp.status}"
                data = await resp.json()
                if "choices" in data and data["choices"] and "message" in data["choices"][0]:
                    return data["choices"][0]["message"]["content"]
                return f"Error: Unexpected OpenRouter API response: {data}"
    except Exception as e:
        return f"Error querying OpenRouter (DeepSeek, async): {e}"