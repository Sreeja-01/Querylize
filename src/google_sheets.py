import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def load_credentials(credentials_file='credentials.json'):
    """Load Google API credentials from a JSON file."""
    try:
        credentials = Credentials.from_service_account_file(credentials_file)
        logging.info("Credentials loaded successfully.")
        return credentials
    except Exception as e:
        logging.error(f"Error loading credentials: {e}")
        return None

def get_sheet_data(spreadsheet_id, range_name='Sheet1', credentials_file='credentials.json'):
    """Retrieve data from a Google Sheets document."""
    credentials = load_credentials(credentials_file)
    
    if not credentials:
        return None
    
    try:
        service = build('sheets', 'v4', credentials=credentials)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        values = result.get('values', [])
        
        if values:
            df = pd.DataFrame(values[1:], columns=values[0])  # Skip first row (headers)
            logging.info("Data retrieved successfully from Google Sheets.")
            return df
        else:
            logging.warning("No data found in the sheet.")
            return None
    except HttpError as err:
        logging.error(f"HTTP error occurred: {err}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    return None
