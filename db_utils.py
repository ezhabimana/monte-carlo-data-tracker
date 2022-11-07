
from models import Currency, CurrencyPair

def insert_currency(db, currency):
    ''' Insert a currency if not exists. Do nothing otherwise '''
    matchingCurrency = db.session.query(Currency).filter_by(symbol=currency.symbol).first()
    
    if matchingCurrency is None:
        db.session.add(currency)
        db.session.commit()
        return currency

    return matchingCurrency

def insert_currency_pair(db, currencyPair):
    ''' Insert a currency pair if not exists. Do nothing otherwise '''
    matchingCurrencyPair = db.session.query(CurrencyPair).filter_by(symbol=currencyPair.symbol).first()
    
    if matchingCurrencyPair is None:
        db.session.add(currencyPair)
        db.session.commit()
        return currencyPair

    return matchingCurrencyPair
