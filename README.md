 HEAD
# Querylize

# Querylize - AI Agent for Information Retrieval

Querylize is a dashboard that allows users to upload datasets (CSV or Google Sheets), perform web searches based on a user-defined prompt, and display the results. The app integrates with Google Sheets and uses LLMs (Large Language Models) to extract specific information from the search results.

## Setup Instructions

1. Clone the repository:
    ```bash
    git clone https://github.com/Sreeja-01/Querylize.git
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up Google API credentials:
    - Follow the instructions on [Google Sheets API Setup](https://developers.google.com/sheets/api/quickstart/python) to get your `credentials.json` file.
    - Place the `credentials.json` file in the project directory.

4. Run the app:
    ```bash
    streamlit run app.py
    ```

## Usage

- Upload your CSV file or enter the Google Sheets URL.
- Define a query prompt using placeholders like `{company}` to fetch information.
- View the retrieved data and download it in CSV format.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
 8765caa (Initial commit)
