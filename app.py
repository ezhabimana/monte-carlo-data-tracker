from flask import Flask, request, jsonify, make_response
import os
import urllib.request, json
from database import db
from db_utils import insert_currency, insert_currency_pair, update_price
from models import Currency, CurrencyPair, PriceHistory
from datetime import datetime, timedelta
from flask_apscheduler import APScheduler
from jobs import update_price_history
import statistics

app = Flask(__name__)

def run_price_history_job():
    '''Updates currency pair prices'''
    with app.app_context():
        update_price_history(db)

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
scheduler.add_job(id='price-history-job', func=run_price_history_job,  trigger='interval', minutes=1)

if __name__ == '__main__':
    app.run(debug=True)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/currencies', methods=['GET'])
def get_currencies():
  currencies = []
  for currency in db.session.query(Currency).all():
    del currency.__dict__['_sa_instance_state']
    currencies.append(currency.__dict__)
  return jsonify(currencies)

@app.route('/currencies/pairs/<symbol>', methods=['GET'])
def get_pair(symbol):
  pair = db.session.query(CurrencyPair).filter_by(symbol=symbol).first()
  if pair is None:
    return make_response(jsonify('Symbol not found'), 404)

  del pair.__dict__['_sa_instance_state']
  return jsonify(pair.__dict__)

@app.route('/currencies/pairs', methods=['GET'])
def get_pairs():
  pairs = []
  for pair in db.session.query(CurrencyPair).all():
    del pair.__dict__['_sa_instance_state']
    pairs.append(pair.__dict__)
  return jsonify(pairs)

@app.route('/currencies', methods=['POST'])
def insert_pairs():
    '''Insert a list of available currency pairs'''
    #url = "https://api.cryptowat.ch/pairs?api_key={}".format(os.environ.get("TMDB_API_KEY"))
    url = "https://api.cryptowat.ch/pairs?api_key=W8DKTQYARYQMLNFYUGZK&limit=1"

    response = json.loads(urllib.request.urlopen(url).read())
    pairs = response["result"]
    for pair in pairs:
        base = pair["base"]
        base_currency = insert_currency(db, Currency(base["symbol"], base["name"]))

        quote = pair["quote"]
        quote_currency = insert_currency(db, Currency(quote["symbol"], quote["name"]))

        currencyPair = CurrencyPair(pair["symbol"], base_currency.id, quote_currency.id)
        insert_currency_pair(db, currencyPair)

    return jsonify(response)

@app.route('/prices', methods=['GET'])
def get_prices():
  currencies = []
  for currency in db.session.query(PriceHistory).all():
    del currency.__dict__['_sa_instance_state']
    currencies.append(currency.__dict__)
  return jsonify(currencies)

@app.route('/prices/<exchange>/<symbol>', methods=['GET'])
def get_symbol_prices(exchange,symbol):
    filters = (
        PriceHistory.exchange == exchange,
        PriceHistory.symbol == symbol,
        PriceHistory.updated_at > (datetime.now() - timedelta(hours=24)),
    )

    prices_query = db.session.query(PriceHistory)\
        .filter(*filters)\
        .order_by(PriceHistory.updated_at)
    if prices_query.count() == 0 :
        return make_response('', 404)

    history_records = []
    for price in prices_query:
        del price.__dict__['_sa_instance_state']
        history_records.append(price.__dict__)
    return jsonify({"stdv": get_standard_deviation(history_records), "prices":history_records})

def get_standard_deviation(history_records):
    '''https://www.forex.com/en/market-analysis/latest-research/what-is-deviation-in-forex/'''
   
    if len(history_records) < 2:
        '''Variance requires at least 2 data points'''
        return None
    
    prices = map(lambda x : x['price'], history_records)
    return statistics.stdev(prices)