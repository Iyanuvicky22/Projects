"""
Importing libraries
"""
import sys
import gspread
from google.oauth2.service_account import Credentials


def export_to_sheets(sheetname: str, data: dict):
    """
    This function connects to gspread api,
    access a worksheet already connected to the
    service account created.

    It then uploads a specified data
    to the first sheet.

    Args:
        sheetname (str): Name of sheet connected to service account
                         credentials email.

        data (dict): Dictionary of data to be uploaded to the sheet.
    """

    try:
        scopes = ['https://www.googleapis.com/auth/drive',
                  'https://www.googleapis.com/auth/spreadsheets']

        json_file = "C:/Users/APIN PC/OneDrive/Documents/DS/DE_Inter/web-scraping-api/credentials.json"
        credentials = Credentials.from_service_account_file(json_file,
                                                            scopes=scopes)

        client = gspread.authorize(credentials)
        ws = client.open(sheetname).sheet1

        header = ws.row_values(1)
        headers = ['Location', 'Current Date',
                   'Pressure', 'Humidity', 'Dew Point'
                   ]

        if header != headers:
            ws.insert_row(headers, index=1)

        # prevent duplicates
        if 
        ws.append_row([data['Location'], data['Current Date'],
                      data['Pressure'], data['Humidity'], data['Dew Point']]
                      )
    except gspread.exceptions.APIError:
        print("Failed to connect to Google Sheets API, \
            - check whether all APIs have been enabled,\
            - check network availability.")
        sys.exit(1)
    except gspread.exceptions.SpreadsheetNotFound:
        print("Spread sheet not found or not shared with the service account.")
        print("Use an existing sheet name \n\
        or connect worksheet with service account.")
        sys.exit(1)
    except FileNotFoundError:
        print("Json credential file not found")
        sys.exit(1)

    else:
        print("Data Upload Successful!!")
