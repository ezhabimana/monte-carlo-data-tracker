from flask import Flask, jsonify, make_response
import os
from database import db
from models import  PriceHistory
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

@app.route('/prices/<exchange>/<symbol>', methods=['GET'])
def get_symbol_prices(exchange,symbol):
    '''Returns the historical prices of a given symbol and the price standard deviation for the past 24 hours'''
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