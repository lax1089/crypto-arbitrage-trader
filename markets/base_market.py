import time
import urllib.request
import urllib.error
import urllib.parse
import logging
import sys
#import gdax_base_market

#exchangemarkets = {"GDAX": gdax_base_market.gdaxmarkets}


class BaseMarket(object):
    def __init__(self, exchange, sourceCurrency, destCurrency, takerFee, makerFee, priceOffset):
        self.name = self.__class__.__name__
        self.exchange = exchange
        self.sourceCurrency = sourceCurrency
        self.destCurrency = destCurrency
        self.takerFee = takerFee
        self.makerFee = makerFee
        self.priceOffset = priceOffset
        self.depth_updated = 0
        self.update_rate = 1
        self.currencies = [sourceCurrency, destCurrency]

    def get_depth(self):
        timediff = time.time() - self.depth_updated
        if timediff > self.update_rate:
            self.ask_update_depth()
        timediff = time.time() - self.depth_updated
        if timediff > 60:
            logging.warn('Market: %s order book is expired' % self.name)
            self.depth = {'asks': [{'price': 0, 'amount': 0}], 'bids': [
                {'price': 0, 'amount': 0}]}
        return self.depth

    def ask_update_depth(self):
        try:
            self.update_depth()
            self.depth_updated = time.time()
        except (urllib.error.HTTPError, urllib.error.URLError) as e:
            logging.error("HTTPError, can't update market: %s" % self.name)
            log_exception(logging.DEBUG)
        except Exception as e:
            logging.error("Can't update market: %s - %s" % (self.name, str(e)))
            #log_exception(logging.DEBUG)
    
    def get_depth_no_update(self):
        return self.depth
    
    def get_bid(self):
        return self.bid
        
    def get_ask(self):
        return self.ask
        
    def get_sourceCurrency(self):
        return self.sourceCurrency
        
    def get_destCurrency(self):
        return self.destCurrency
    
    def print_market(self):
        print('exchange: ' +self.exchange 
            + ' | code: ' +self.code 
            + ' | srcCurr: ' +self.sourceCurrency
            + ' | destCurr: ' +self.destCurrency
            + ' | takerFee: ' +str(self.takerFee)
            + ' | makerFee: ' +str(self.makerFee)
            )
    
    def update_depth(self):
        pass

    def buy(self, price, amount):
        pass

    def sell(self, price, amount):
        pass
