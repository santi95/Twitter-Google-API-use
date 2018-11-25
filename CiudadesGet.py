from __future__ import print_function
import httplib2
import os
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import collections
import shutil
from config import SCOPES, CLIENT_SECRET_FILE, APPLICATION_NAME

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json


def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        # shutil.rmtree(credential_dir)
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def main(url1):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    link = url1
    fin = link.index('/edit')
    inicio = link.index('/d/')
    spreadsheetId = link[inicio + 3:fin]
    rangeName = 'Hoja 1'
    try:
        # Escribir la nueva hoja
        batch_update_spreadsheet_request_body = {
            'requests': [{
                'addSheet': {
                    "properties": {
                        "title": "Logger",
                        "gridProperties": {
                            "rowCount": 20,
                            "columnCount": 12
                        },
                        "tabColor": {
                            "red": 1.0,
                            "green": 0.3,
                            "blue": 0.4
                        }
                    }
                }
            }]
        }

        hoja_nueva = service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheetId,
            body=batch_update_spreadsheet_request_body)
        response = hoja_nueva.execute()["replies"][0]['addSheet']["properties"]
        print(response["sheetId"])
    except:
        print('Esa Sheet ya está creada')

    # Hasta acá es escritura de hoja
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    Country = collections.namedtuple('Country', 'pais ciudades')
    datos = []

    if not values:
        print('No data found.')
    else:
        for row in values[1:]:
            a = Country(row[0], row[1:])
            datos.append(a)
    return datos


def append_to_sheet_logger(url1, msge):
    msge[0] = "[{}]".format(msge[0])
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)
    link = url1
    fin = link.index('/edit')
    inicio = link.index('/d/')
    spreadsheetId = link[inicio + 3:fin]
    rangeName = 'Logger'
    values = [msge]
    body = {"values": values}
    value_input_option = "RAW"
    insert_data_option = "INSERT_ROWS"

    service.spreadsheets().values().append(
        spreadsheetId=spreadsheetId,
        valueInputOption=value_input_option,
        body=body,
        range=rangeName,
        insertDataOption=insert_data_option
    ).execute()
