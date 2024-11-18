import streamlit as st
import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import openai
from dotenv import load_dotenv
import os
from src.data_processing import clean_data, preprocess_data
from src.llm_processing import process_query, generate_insights
from src.web_search import search_web
from googleapiclient.discovery import build

credentials_info = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
# Path to your credentials.json file
credentials = Credentials.from_service_account_file('D:\MY PROJECTS\Querylize\credentials.json')

# Use the credentials for API calls
# Use previously loaded credentials, no need to reload
service = build('sheets', 'v4', credentials=credentials)

import requests
from urllib.parse import quote_plus

# Load environment variables from the .env file
load_dotenv()

# Retrieve the API keys from the environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SCRAPERAPI_API_KEY = os.getenv("SCRAPERAPI_API_KEY")

# Check if API keys are loaded
if not OPENAI_API_KEY:
    st.error("OPENAI_API_KEY is not set in the environment variables.")
if not SCRAPERAPI_API_KEY:
    st.error("SCRAPERAPI_API_KEY is not set in the environment variables.")

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
        
        # Clean and preprocess the data
        df_cleaned = clean_data(df)
        df_preprocessed = preprocess_data(df_cleaned)
        st.write("Cleaned and Preprocessed Data:")
        st.dataframe(df_preprocessed)

        # Select the Primary Column dynamically
        column_choice = st.selectbox('Select the Primary Column', df_preprocessed.columns)
        st.write(f'Primary Column Selected: {column_choice}')
        
        # Enter Custom Prompt for LLM
        prompt_template = st.text_input('Enter Custom Prompt (e.g., "Find the average of {column_name}")')
        
        if prompt_template:
            prompt = prompt_template.replace("{column_name}", column_choice)
            if st.button("Generate Insights with Custom Prompt"):
                insights = generate_insights(df_preprocessed.to_string(), prompt)
                st.subheader("LLM Generated Insights:")
                st.write(insights)
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

# Example OpenAI API Call with Proper Error Handling
try:
    # Example call to OpenAI API
    response = openai.Completion.create(  # Corrected API call for GPT model
        model="gpt-3.5-turbo",  # Use the correct model
        prompt="You are a helpful assistant.",
        max_tokens=100,
        temperature=0.5
    )
    st.write(response.choices[0].text)  # Display the response
except openai.error.RateLimitError:
    st.error("Rate limit exceeded, please try again later.")
except openai.OpenAIError as e:
    st.error(f"OpenAI error occurred: {str(e)}")
except Exception as e:
    st.error(f"An unexpected error occurred: {str(e)}")

# Adding Web Search as an Optional Feature
st.header("Web Search Integration")
search_query = st.text_input("Enter a query to search the web:")
if search_query:
    try:
        search_results = search_web(search_query)
        st.write("Web Search Results:")
        st.write(search_results)
    except Exception as e:
        st.error(f"Error searching the web: {str(e)}")
