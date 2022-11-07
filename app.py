from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import urllib.request, json
from database import db
from db_utils import insert_currency, insert_currency_pair
from models import Currency, CurrencyPair, PriceHistory

app = Flask(__name__)

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
  pair = db.session.query(CurrencyPair).filter_by(symbol=symbol)
  del pair.__dict__['_sa_instance_state']
  return jsonify(pair.__dict__)

@app.route('/currencies/pairs', methods=['GET'])
def get_pairs():
  pairs = []
  for pair in db.session.query(CurrencyPair).all():
    del pair.__dict__['_sa_instance_state']
    pairs.append(pair.__dict__)
  return jsonify(pairs)

@app.route('/currencies/initialize', methods=['POST'])
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

    # dict = json.loads(pairs)

    # movies = []

    # for movie in dict["result"]:
    #     movie = {
    #         "title": movie["title"],
    #         "overview": movie["overview"],
    #     }
        
    #     movies.append(movie)

    # return {"results": movies}
    return jsonify(response)

# @app.route('/items/<id>', methods=['GET'])
# def get_item(id):
#   item = Item.query.get(id)
#   del item.__dict__['_sa_instance_state']
#   return jsonify(item.__dict__)

# @app.route('/items', methods=['GET'])
# def get_items():
#   items = []
#   for item in db.session.query(Item).all():
#     del item.__dict__['_sa_instance_state']
#     items.append(item.__dict__)
#   return jsonify(items)

# @app.route('/items', methods=['POST'])
# def create_item():
#   body = request.get_json()
#   db.session.add(Item(body['title'], body['content']))
#   db.session.commit()
#   return "item created"

# @app.route('/items/<id>', methods=['PUT'])
# def update_item(id):
#   body = request.get_json()
#   db.session.query(Item).filter_by(id=id).update(
#     dict(title=body['title'], content=body['content']))
#   db.session.commit()
#   return "item updated"

# @app.route('/items/<id>', methods=['DELETE'])
# def delete_item(id):
#   db.session.query(Item).filter_by(id=id).delete()
#   db.session.commit()
#   return "item deleted"

