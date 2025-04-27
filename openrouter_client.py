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
            # Corrected model ID for DeepSeek chat on OpenRouter
            model="deepseek/deepseek-chat", # Using the potentially correct model ID
            messages=[{"role": "user", "content": prompt}], # User message
            extra_headers={
                "HTTP-Referer": "https://yourdomain.com", # Replace with your domain
                "X-Title": "AI Research Assistant" # Title for logging purposes
            }
        )
        # Extract and return the model's response
        return response.choices[0].message.content
    except Exception as e:
        # Log the specific error for debugging
        print(f"Error in openrouter_query: {e}")
        # Re-raise the exception or return an error message
        raise # Re-raising to be caught by the FastAPI error handler
        # return f"Error querying OpenRouter (DeepSeek): {e}" # Alternative: return error message