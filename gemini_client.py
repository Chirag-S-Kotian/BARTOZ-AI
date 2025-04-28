import os
import asyncio # Required for async functions and async for
import collections
# Import necessary components from the google.generativeai library
# This is the correct library for using API keys from Google AI Studio
# You need to install this library: pip install google-generativeai
from google.generativeai import GenerativeModel, configure
from google.generativeai.types import GenerateContentResponse # Import the type for inspection
# Import exceptions for specific error handling
from google.api_core import exceptions
import logging # Import logging for better error reporting

# Configure logging
logging.basicConfig(level=logging.INFO)

# Configure Gemini API Key from environment variables
# This uses the configure function specific to google.generativeai
# Ensure GEMINI_API_KEY is set in your environment
if os.getenv("GEMINI_API_KEY"):
    configure(api_key=os.getenv("GEMINI_API_KEY"))
else:
    logging.error("GEMINI_API_KEY environment variable not set. Gemini queries will fail.")


# This is an async function to support streaming
async def gemini_query(prompt: str) -> str:
    """
    Queries the gemini-2.5-flash-preview-04-17 model using the google.generativeai library
    in a streaming fashion, with a prompt suitable for a RAG researcher,
    emphasizing AI/Agents/ML topics and source citation.

    Args:
        prompt: The user's query combined with retrieved context from the RAG pipeline.

    Returns:
        The generated response from the model, or an error message string.
    """
    # Check if API key is configured before making the call
    if not os.getenv("GEMINI_API_KEY"):
        return "Error: GEMINI_API_KEY is not configured."

    model = None # Initialize model outside try for error handling scope
    stream_response = None # Initialize stream_response outside try

    try:
        # Initialize the Generative Model with the specific model name
        # This library correctly uses the generativelanguage.googleapis.com endpoint
        # Using the model name from your provided code
        model = GenerativeModel("gemini-2.5-flash-preview-04-17")
        logging.info(f"Initialized Gemini model: {model.model_name}")

        # --- Refined Prompt for RAG Researcher ---
        # This prompt guides the model to focus on specific topics and cite sources.
        # The 'prompt' argument passed to this function *must* contain the user's
        # original query combined with the relevant context retrieved by your RAG pipeline,
        # and the context should ideally include source titles and URLs.
        # Truncate context if too long (Gemini supports ~16k tokens; be conservative)
        max_chars = 20000
        safe_prompt = prompt if len(prompt) < max_chars else prompt[:max_chars] + "\n[Context truncated due to length limit]"

        formatted_prompt = f"""
You are an expert AI/ML/LLM research assistant.
STRICT INSTRUCTIONS:
- ONLY answer using the information provided in the [RESEARCH CONTEXT] below.
- NEVER use prior knowledge, training data, or make up answers. If the answer is not found, say: 'Sorry, the answer was not found in the provided research context.'
- Provide a concise, focused summary (max 5 sentences, only essential facts).
- For every fact, always cite the source title and URL from the context.

[RESEARCH CONTEXT]
{safe_prompt}
[END OF CONTEXT]

[USER QUESTION IS INCLUDED ABOVE]

Answer:"""
        # --- End Refined Prompt ---

        logging.info("Sending prompt to Gemini API...")
        # Make the streaming API call
        # Use generate_content with stream=True, which is the correct method
        # in google.generativeai for streaming.
        # This call *should* return an asynchronous iterator.
        stream_response = model.generate_content(
            [{"role": "user", "parts": [{"text": formatted_prompt}]}],
            stream=True # Enable streaming
        )
        logging.info(f"Received object from Gemini API. Type: {type(stream_response)}") # Log the type received

        result = ""
        logging.info("Attempting to iterate over Gemini stream...")
        # Robustly handle async iterator, sync iterator, or plain response
        if hasattr(stream_response, "__aiter__"):
            logging.info("Gemini stream_response is an async iterator.")
            async for chunk in stream_response:
                if hasattr(chunk, 'text') and chunk.text:
                    result += chunk.text
                else:
                    logging.debug(f"Received a chunk with no text. Chunk: {chunk}")
            logging.info("Finished iterating over Gemini async stream.")
        elif isinstance(stream_response, collections.abc.Iterator):
            logging.info("Gemini stream_response is a sync iterator.")
            for chunk in stream_response:
                if hasattr(chunk, 'text') and chunk.text:
                    result += chunk.text
                else:
                    logging.debug(f"Received a chunk with no text. Chunk: {chunk}")
            logging.info("Finished iterating over Gemini sync stream.")
        else:
            logging.info("Gemini stream_response is a single response object.")
            try:
                stream_response.resolve()  # Ensure all content is available
                if hasattr(stream_response, 'text') and stream_response.text:
                    result = stream_response.text
                else:
                    logging.warning("Gemini API returned a response with no text.")
            except Exception as e:
                logging.error(f"Error resolving Gemini response: {e}", exc_info=True)
                result = ""

        # --- Handle cases where no text was generated ---
        if not result:
            logging.warning("Gemini API generated an empty response.")
            finish_reason = "Unknown"
            safety_ratings = "N/A"
            if isinstance(stream_response, GenerateContentResponse) and stream_response.candidates:
                try:
                    finish_reason = stream_response.candidates[0].finish_reason.name
                    logging.warning(f"Gemini finish reason: {finish_reason}")
                    if stream_response.candidates[0].safety_ratings:
                        safety_ratings = ", ".join([
                            f"{sr.category.name}: {sr.probability.name}"
                            for sr in stream_response.candidates[0].safety_ratings
                        ])
                        logging.warning(f"Gemini safety ratings: {safety_ratings}")
                except Exception as e:
                    logging.warning(f"Could not get finish reason or safety ratings from response object: {e}")
            # User-friendly error message
            return (f"❌ Gemini API generated no content. This may be due to safety filters, irrelevant context, or model limitations. "
                    f"Finish Reason: {finish_reason}. Safety Ratings: {safety_ratings}")
        # --- End handling empty response ---

        # If finish_reason is not STOP, warn user
        if isinstance(stream_response, GenerateContentResponse) and stream_response.candidates:
            try:
                finish_reason = stream_response.candidates[0].finish_reason.name
                if finish_reason != 'STOP':
                    logging.warning(f"Gemini did not finish normally: {finish_reason}")
                    return f"❌ Gemini did not finish normally. Finish Reason: {finish_reason}"
            except Exception:
                pass

        return result

    # Add specific exception handling for API errors from google-generativeai
    except exceptions.GoogleAPIError as e:
        logging.error(f"Google API Error in gemini_query: {e}", exc_info=True)
        # Return a user-friendly error message including the error details
        return f"Error communicating with Gemini API: {e}"
    except Exception as e:
        # Catch any other unexpected errors
        logging.error(f"An unexpected error occurred in gemini_query: {e}", exc_info=True)
        # Return a user-friendly error message
        return f"An unexpected error occurred with Gemini API: {e}"