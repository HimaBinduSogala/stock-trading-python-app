import requests
import os
from dotenv import load_dotenv
import time
import csv

load_dotenv()

POLYGON_API_KEY = os.getenv('POLYGON_API_KEY')

LIMIT = 1000

def run_stock_job():
    url = f'https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={POLYGON_API_KEY}'
    response = requests.get(url)

    # Initialize the list
    tickers = []
    data = response.json()

    # Loop through the results and append the ticker to the list
    for ticker in data['results']:
        tickers.append(ticker)

    # Loop through the next url and append the ticker to the list


    while data.get('next_url'):
        print('requesting next url', data['next_url'])
        response = requests.get(data['next_url'] + f'&apiKey={POLYGON_API_KEY}')
        data = response.json()
        #print(data)
        for ticker in data['results']:
            tickers.append(ticker)
        # wait 12 seconds to avoid rate limit on polygon api
        time.sleep(12)

    example_ticker =  {'ticker': 'ZJUL', 
                        'name': 'Innovtor Equity Defined Protection ETF - 1 Yr July', 
                        'market': 'stocks', 
                        'locale': 'us', 
                        'primary_exchange': 'BATS', 
                        'type': 'ETF', 
                        'active': True, 
                        'currency_name': 'usd', 
                        'cik': '0001415726', 
                        'composite_figi': 'BBG01NJ1YH91', 
                        'share_class_figi': 'BBG01NJ1YJ42', 
                        'last_updated_utc': '2025-09-17T15:54:25.563997059Z'}

    print(len(tickers))


    # Write tickers to CSV with the same schema/order as example_ticker
    fieldnames = [
        'ticker',
        'name',
        'market',
        'locale',
        'primary_exchange',
        'type',
        'active',
        'currency_name',
        'cik',
        'composite_figi',
        'share_class_figi',
        'last_updated_utc',
    ]
    output_csv = 'tickers.csv'
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for t in tickers:
            # Ensure only the expected fields are written; fill missing with empty string
            row = {key: t.get(key, '') for key in fieldnames}
            writer.writerow(row)
    print(f'Wrote {len(tickers)} rows to {output_csv}')

if __name__ == '__main__':
    run_stock_job()