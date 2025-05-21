import os
from google import genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch
from agents import function_tool # Assuming this is from your OpenAI Agent SDK
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


@function_tool
async def search(query: str) -> str:
    """
    Search for information using the native Gemini API with Google Search grounding.

    This function queries a Gemini model (via the native Python SDK),
    instructing it to answer based on information retrieved from Google Search.
    It attempts to extract and format citation information from the response.
    """
    print(f"Native Gemini search tool invoked with query: '{query}'")
    try:
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        model_id = "gemini-2.0-flash"

        google_search_tool = Tool(
            google_search = GoogleSearch()
        )

        response = client.models.generate_content(
            model=model_id,
            contents=query,
            config=GenerateContentConfig(
                tools=[google_search_tool],
                response_modalities=["TEXT"],
            )
        )
        return response.candidates[0].content.parts[0].text
    except Exception as e:
        print(f"Error during Native Gemini grounded search for query '{query}': {e}")
        import traceback
        traceback.print_exc()
        return f"An error occurred while searching with Native Gemini for '{query}'. Details: {str(e)}"