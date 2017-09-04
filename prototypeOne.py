from scapy.all import *
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = '' # UserContent.json
APPLICATION_NAME = '' # Project name

def get_credentials():
    
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def todo():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '' # Spread sheed ID
    rangeName = 'A1:A'
    values = {'values':[['Text',],]} # Text = msg for Spread Sheet
    
    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheetId, range=rangeName, valueInputOption='RAW',
        body=values).execute()

def arp_display(pkt):
    if pkt.haslayer(ARP):
        if pkt[ARP].op == 1:
            if pkt[ARP].hwsrc == '': # MAC-Adress from Dash-Button
                    print "Dash Button pressed"
                    todo()

print sniff(prn=arp_display, filter="arp", store=0, count=0)


