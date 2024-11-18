import streamlit as st
import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import requests
from urllib.parse import quote_plus
import openai
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Retrieve the API keys from the environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SCRAPERAPI_API_KEY = os.getenv("SCRAPERAPI_API_KEY")

# Initialize OpenAI API
openai.api_key = OPENAI_API_KEY

# Dashboard Title
st.title("Querylize Dashboard")

# File Upload Section
st.header("Upload Your Dataset")
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

# Google Sheets Section
st.header("Connect to Google Sheets")
sheet_url = st.text_input("Enter Google Sheets URL")

# DataFrame placeholder
df = None

# Display the uploaded file if it's not None
if uploaded_file is not None:
    try:
        # Read CSV file
        df = pd.read_csv(uploaded_file)
        st.write("Preview of the Uploaded File:")
        st.dataframe(df)
    except Exception as e:
        st.error(f"Error reading the file: {str(e)}")

# Google Sheets Integration
if sheet_url:
    try:
        # Check if the URL contains a valid Google Sheets link format
        if "/d/" not in sheet_url or "/edit" not in sheet_url:
            st.error("Please enter a valid Google Sheets URL.")
        else:
            # Load credentials from the service account JSON file
            credentials = Credentials.from_service_account_file('credentials.json')
            # Extract the Spreadsheet ID from the URL
            spreadsheet_id = sheet_url.split("/d/")[1].split("/")[0]

            # Access the Google Sheets API
            service = build('sheets', 'v4', credentials=credentials)
            sheet = service.spreadsheets()
            result = sheet.values().get(spreadsheetId=spreadsheet_id, range='Sheet1').execute()
            values = result.get('values', [])

            # Convert data to DataFrame and display it
            if values:
                df = pd.DataFrame(values[1:], columns=values[0])  # Skip header row and assign columns
                st.write("Preview of the Google Sheets Data:")
                st.dataframe(df)
            else:
                st.warning("No data found in the provided sheet.")
    except Exception as e:
        st.error(f"Error accessing Google Sheets: {str(e)}")

# Prompt Input Section for LLM Query
st.header("Enter Your Prompt")
user_prompt = st.text_input("Write your prompt for data extraction:")

# Function to process query based on user prompt
def process_query(prompt, data_frame):
    # Example: Let's assume the user wants to find information about a specific company
    if "company" in prompt.lower() and data_frame is not None:
        # Extract company names from the dataset and search for the requested company
        company_column = 'Company Name'  # Replace with the actual column name from your dataset
        if company_column in data_frame.columns:
            # Find the company (case-insensitive search)
            company_name = prompt.lower().split("company")[-1].strip()
            result_row = data_frame[data_frame[company_column].str.contains(company_name, case=False, na=False)]
            if not result_row.empty:
                # Return the first matching result
                return result_row.iloc[0].to_string()  # Convert the row to a string for display
            else:
                return f"No information found for company: {company_name}"
        else:
            return f"Column '{company_column}' not found in the dataset."
    elif "search" in prompt.lower():
        # If the prompt asks for a web search
        search_results = search_web(prompt)
        return format_search_results(search_results)
    else:
        return "Sorry, I didn't understand the query."

# Function to format search results for display
def format_search_results(results):
    if results and 'organic_results' in results:
        formatted_results = ""
        for result in results['organic_results']:
            title = result.get('title')
            snippet = result.get('snippet')
            url = result.get('url')
            formatted_results += f"**{title}**\n{snippet}\n[Link]({url})\n\n"
        return formatted_results
    else:
        return "No results found from web search."

# Display Result from LLM or Search
if user_prompt:
    try:
        if df is not None:
            # If dataset is available (CSV or Google Sheets), process the query
            result = process_query(user_prompt, df)
        else:
            result = "No data loaded. Please upload a file or connect Google Sheets."
        st.write("Processed Result:")
        st.text(result)  # Display result as plain text
    except Exception as e:
        st.error(f"Error processing the prompt: {str(e)}")

# Example Web Search Integration using ScraperAPI
def search_web(query):
    encoded_query = quote_plus(query)
    url = f'https://api.scraperapi.com?api_key={SCRAPERAPI_API_KEY}&url=https://www.google.com/search?q={encoded_query}'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Will raise an error for non-200 status codes
        return response.json()  # Assuming the response is in JSON format
    except requests.exceptions.RequestException as e:
        st.error(f"Error during web search: {str(e)}")
        return None
