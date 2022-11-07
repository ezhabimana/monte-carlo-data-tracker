from database import db

class Currency(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  symbol = db.Column(db.String(10), unique=True, nullable=False)
  # Name is not unique for example British Pound has gbp and 6b
  name = db.Column(db.String(100), unique=False, nullable=False)

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