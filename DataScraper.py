import pytz
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
#from google.cloud import bigquery
import pyarrow
#from google.cloud import storage
import string
import time

def daily_equity_quotes(event, context):
    # Gets the api key from cloud storage
    #storage_client = storage.Client()
    #bucket = storage_client.get_bucket('Name of your bucked storage bucket')
    #blob = bucket.blob('name of your secret file')
    #api_key = blob.download_as_string()
    api_key = 'GW39VSIUIWPTDINZAPHMKJRY0CSMZ7MG'

    # Check if the market was open today
    today = datetime.today().astimezone(pytz.timezone("Australia/Perth"))
    today_fmt = today.strftime('%Y-%m-%d')

    # Calling td ameritrade hours endpoint for equities to see if it is open
    market_url = 'https://api.tdameritrade.com/v1/marketdata/equity/hours'

    params = {
        'apikey': api_key,
        'date': today_fmt
        }

    request = requests.get(
        url=market_url,
        params=params
        ).json()

    try:
        if request['equity']['EQ']['isOpen'] is True:
            alpha = list(string.ascii_uppercase)

            symbols = []

            for each in alpha:
                url = f'http://eoddata.com/stocklist/NYSE/{each}.htm'
                resp = requests.get(url)
                site = resp.content
                soup = BeautifulSoup(site, 'html.parser')
                table = soup.find('table', {'class': 'quotes'})
                for row in table.findAll('tr')[1:]:
                    symbols.append(row.findAll('td')[0].text.rstrip())
            
            print(symbols)

    except:
        pass

daily_equity_quotes("","")
