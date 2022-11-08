from database import db

class PriceHistory(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  symbol = db.Column(db.String(100), nullable=False)
  exchange = db.Column(db.String(100), nullable=False)
  price = db.Column(db.Float, nullable=True)
  updated_at = db.Column(db.DateTime, nullable=True)

  def __init__(self, symbol, exchange, price, updated_at):
    self.symbol = symbol
    self.exchange =  exchange
    self.price = price
    self.updated_at = updated_at

def update_price(db, history_item):
    ''' Insert a new price history record '''
    db.session.add(history_item)
    db.session.commit()
    return history_item