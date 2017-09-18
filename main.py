""" Import required libraries """
import os

from oauth2client.service_account import ServiceAccountCredentials
from apiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/drive']
CREDENTIALS_PATH = '/tmp/credentials.json'


def get_credentials(credentials):
    """
        We have to write it to a file because gcs
        library only accepts a file path.
    """
    with open(CREDENTIALS_PATH, "w") as credentials_file:
        credentials_file.write(credentials)

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_PATH, SCOPES)

    return credentials


def renameSheet(sheet_id, new_name):
    return {
        "updateSheetProperties": {
            "properties": {
                "sheetId": sheet_id,
                "title": new_name,
            },
            "fields": "title",
        }
    }


def main(sheet_id, copy_to, service_account_json, new_name="", tab_id=0):
    """ Copy a single sheet to another spreadsheet """

    credentials = get_credentials(service_account_json)
    service = build('sheets', 'v4', credentials=credentials)

    body = {
        "destinationSpreadsheetId": copy_to
    }

    result = {}
    try:
        request = service.spreadsheets().sheets().copyTo(
            spreadsheetId=sheet_id, sheetId=tab_id,
            body=body)

        result = request.execute()
        result["success"] = True
        result["description"] = "Successfully copied sheet tab."
    except Exception:
        result["success"] = False
        result["description"] = "Something went wrong with the request, try again."

    # rename the new sheet tab
    if result and new_name:
        tab_id = result.get("sheetId")
        body = {
            "requests": renameSheet(tab_id, new_name)
        }
        try:
            new_result = service.spreadsheets().batchUpdate(
                spreadsheetId=copy_to,
                body=body).execute()

            new_result["title"] = new_name
            result.update(new_result)
        except Exception:
            pass

    os.remove(CREDENTIALS_PATH)
    return result
