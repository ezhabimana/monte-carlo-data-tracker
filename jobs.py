import urllib.request, json
from db_utils import  update_price
from models import  PriceHistory
from datetime import datetime

# narrowing down to specific markets
supported_exchanges = [ 'binance-us' ]

def update_price_history(db):
    '''Updates currency pair prices'''
    hasMore = True
    last_cursor = None
    while(hasMore):
        url = f'https://api.cryptowat.ch/markets/prices?api_key=W8DKTQYARYQMLNFYUGZK'
        if(last_cursor):
            url = f'{url}&cursor={last_cursor}'

        response = json.loads(urllib.request.urlopen(url).read())
        results = response['result']
        
        for symbol in results:
            # symbol looks something like  "market:binance-us:1inchusd" where the actual symbol is the last portion
            symbols_details = symbol.split(':')
            exchange = symbols_details [1]
            parsed_symbol = symbols_details [2]
            if exchange in supported_exchanges:
                '''Exclude exchanges we don't care about'''
                history_item = PriceHistory(parsed_symbol, exchange, results[symbol], datetime.now())
                update_price(db, history_item)

        cursor = response['cursor']
        hasMore = cursor["hasMore"]
        last_cursor = cursor["last"]

        print(f'Last cursor is {last_cursor}', flush="True")
        print(f'Completed updating prices at { str(datetime.now())}', flush="True")