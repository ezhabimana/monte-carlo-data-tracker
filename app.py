from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

# class Item(db.Model):
#   id = db.Column(db.Integer, primary_key=True)
#   title = db.Column(db.String(80), unique=True, nullable=False)
#   content = db.Column(db.String(120), unique=True, nullable=False)

#   def __init__(self, title, content):
#     self.title = title
#     self.content = content

class Currency(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  symbol = db.Column(db.String(10), unique=True, nullable=False)
  name = db.Column(db.String(100), unique=True, nullable=False)

  def __init__(self, symbol, name):
    self.symbol = symbol
    self.name = name


class CurrencyPair(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  symbol = db.Column(db.String(10), unique=True, nullable=False)
  base_currency_id = db.Column(db.Integer, nullable=False)
  quote_currency_id = db.Column(db.Integer, nullable=False)

  def __init__(self, symbol, base_currency_id, quote_currency_id):
    self.symbol = symbol
    self.base_currency_id = base_currency_id
    self.quote_currency_id = quote_currency_id

class PriceHistory(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  symbol = db.Column(db.String(10), unique=True, nullable=False)
  currency_pair_id = db.Column(db.Integer, nullable=False)
  price = db.Column(db.Float, nullable=True)
  updated_at = db.Column(db.DateTime, nullable=True)

  def __init__(self, symbol, currency_pair_id, price, updated_at):
    self.symbol = symbol
    self.currency_pair_id = currency_pair_id
    self.price = price
    self.updated_at = updated_at

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