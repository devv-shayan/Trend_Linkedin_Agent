import os
from agents import function_tool
from linkup import LinkupClient
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


@function_tool
def search(query: str) -> str:
    """
    Search for information using the Linkup API.

    This function performs a web search using Linkup's search API to find relevant information
    based on the provided query.
    """
    linkup_api_key = os.getenv("LINKUP_API_KEY")
    if not linkup_api_key:
        raise ValueError(
            "LINKUP_API_KEY is not set. Please ensure it is defined in your .env file "
            "for the search tool to work."
        )

    client = LinkupClient(api_key=linkup_api_key)
    try:
        response = client.search(
            query=query,
            depth="standard",
            output_type="sourcedAnswer",
            include_images=False,
        )
        # Ensuring the response is stringified for consistent output format.
        return f"Search results for '{query}': {str(response)}"
    except Exception as e:
        # Log the exception (in a real app, use proper logging) and return an error message.
        print(f"Error during Linkup search for query '{query}': {e}")
        return f"An error occurred while searching for '{query}'. Please try a different query or check the tool configuration." 