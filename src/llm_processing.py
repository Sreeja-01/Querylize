import openai
import os
from dotenv import load_dotenv

# Load environment variables from a .env file (for security purposes)
load_dotenv()

# Function to initialize OpenAI API with your key
def initialize_openai_api(api_key=None):
    """Initialize the OpenAI API with the given API key."""
    if api_key:
        openai.api_key = api_key
    elif os.getenv('OPENAI_API_KEY'):
        openai.api_key = os.getenv('OPENAI_API_KEY')
    else:
        raise ValueError("API key is missing. Please set the OPENAI_API_KEY environment variable.")
    print("OpenAI API Initialized")

# Function to generate insights from the data using LLM
def generate_insights(data, model="gpt-3.5-turbo"):
    """Generate insights from the provided data using an OpenAI LLM."""
    try:
        prompt = f"Analyze the following data and provide insights:\n\n{data}"

        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an insightful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,  # Adjust based on the desired response length
            temperature=0.7  # Creativity in the response
        )

        insights = response['choices'][0]['message']['content'].strip()
        return insights

    except openai.error.RateLimitError:
        return "Rate limit exceeded, please try again later."
    except openai.error.OpenAIError as e:
        return f"OpenAI error occurred: {str(e)}"
    except Exception as e:
        return f"Error generating insights: {str(e)}"

# Function to parse search results using LLM
def parse_results_with_llm(search_results, query):
    """
    This function processes the search results with OpenAI's GPT-3 to extract specific information.
    
    Parameters:
    - search_results (str): The raw search results or text to parse.
    - query (str): The specific information you want to extract from the search results.

    Returns:
    - str: The extracted data from the search results.
    """
    # Create a prompt for GPT-3 to extract specific information
    prompt = f"Extract {query} from the following text: {search_results}. Provide the most relevant information."
    
    # Make the API call to OpenAI's GPT-3 (using ChatCompletion)
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Using the more cost-effective model
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,  # Limit the number of tokens (words) in the output
            temperature=0.5  # More focused responses
        )

        # Extract and return the LLM's response
        return response['choices'][0]['message']['content'].strip()

    except openai.error.RateLimitError:
        return "Rate limit exceeded, please try again later."
    except openai.error.OpenAIError as e:
        return f"OpenAI error occurred: {str(e)}"
    except Exception as e:
        print(f"Error in LLM processing: {e}")
        return f"Error processing search results: {str(e)}"
# src/llm_processing.py

def process_query(prompt, data_frame):
    """
    Process the query based on the user prompt and the provided data frame.
    
    Parameters:
    - prompt (str): The user-defined prompt for data extraction.
    - data_frame (pd.DataFrame): The data frame containing the data to process.
    
    Returns:
    - str: The result of processing the query.
    """
    # Check if the prompt contains the word "company" and if the data frame is not None
    if "company" in prompt.lower() and data_frame is not None:
        # Define the column name that contains company names
        company_column = 'Company Name'  # Replace with the actual column name
        
        # Check if the specified company column exists in the data frame
        if company_column in data_frame.columns:
            # Extract the company name from the prompt
            company_name = prompt.lower().split("company")[-1].strip()
            
            # Search for rows in the data frame where the company column contains the specified company name
            result_row = data_frame[data_frame[company_column].str.contains(company_name, case=False, na=False)]
            
            # If a matching row is found, return it as a string
            if not result_row.empty:
                return result_row.iloc[0].to_string()
            else:
                # Return a message if no matching company is found
                return f"No information found for company: {company_name}"
        else:
            # Return a message if the company column is not found in the data frame
            return f"Column '{company_column}' not found in the dataset."
    else:
        # Return a message if the query does not contain "company" or if the data frame is None
        return "Sorry, I didn't understand the query."
