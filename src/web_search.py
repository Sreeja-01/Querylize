import requests
import time
import os
from dotenv import load_dotenv
import requests
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

SCRAPERAPI_API_KEY = os.getenv("SCRAPERAPI_API_KEY")

def search_web(query):
    """Perform a web search using ScraperAPI."""
    encoded_query = quote_plus(query)
    url = f'https://api.scraperapi.com?api_key={SCRAPERAPI_API_KEY}&url=https://www.google.com/search?q={encoded_query}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return f"Error during web search: {str(e)}"


# Load ScraperAPI key from .env
load_dotenv()
SCRAPERAPI_API_KEY = os.getenv('SCRAPERAPI_API_KEY')

def search_query(entity, prompt_template):
    """
    Search query using ScraperAPI for automated web search.
    Args:
    - entity (str): The entity to search for (e.g., company name).
    - prompt_template (str): The prompt containing placeholders for the search query.
    
    Returns:
    - search_results (dict): A dictionary containing the search results from the API.
    """
    query = prompt_template.replace('{company}', entity)
    
    # Construct the URL for ScraperAPI request
    url = f'https://api.scraperapi.com?api_key={SCRAPERAPI_API_KEY}&url=https://www.google.com/search?q={query}'
    
    while True:
        try:
            # Send the request to ScraperAPI
            response = requests.get(url)
            
            if response.status_code == 200:
                # Return the JSON response (search results)
                return response.json()
            else:
                # Handle rate limits or other errors
                if handle_rate_limit(response.json()):
                    continue
                print(f"Error: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

def handle_rate_limit(response):
    """
    Handle API rate limits and retry the request if necessary.
    """
    if 'error' in response and response['error'] == 'quota_exceeded':
        print("Quota exceeded. Retrying in 30 seconds...")
        time.sleep(30)
        return True  # Indicate that we need to retry the request
    return False