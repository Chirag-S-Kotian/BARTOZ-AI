from openai import OpenAI
import os
import requests # Import requests for better error handling

# Initialize the OpenAI client pointing to OpenRouter API
# Ensure OPENROUTER_API_KEY is set in your environment
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY") # Get API key from environment variables
)

def openrouter_query(prompt: str) -> str:
    """
    Queries the DeepSeek model via OpenRouter API.

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