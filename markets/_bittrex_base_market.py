import urllib.request
import urllib.error
import urllib.parse
import json
from .base_market import BaseMarket


class BittrexBaseMarket(BaseMarket):
    def __init__(self, sourceCurrency, destCurrency, code, takerFee, makerFee, priceOffset):
        super().__init__("Bittrex", sourceCurrency, destCurrency, takerFee, makerFee, priceOffset)
        self.code = code
        self.update_rate = 1

    def update_depth(self):
        url = 'https://bittrex.com/api/v1.1/public/getorderbook'
        req = urllib.request.Request(url, b"market=" + bytes(self.code, "ascii")+b"&type=both"+b"&depth=10",
                                     headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "*/*",
            "User-Agent": "curl/7.24.0 (x86_64-apple-darwin12.0)"})
        res = urllib.request.urlopen(req)
        depth = json.loads(res.read().decode('utf8'))
        self.depth = self.format_depth(depth)

    #def sort_and_format(self, l, reverse=False):
        #r = []
        #r.append({'price': float(l['Rate']), 'amount': float(l['Quantity'])})
        #return r
        
    def sort_and_format(self, l, reverse=False):
        l.sort(key=lambda x: float(x['Rate']), reverse=reverse)
        r = []
        r.append({'price': float(l[0]['Rate']), 'amount': float(l[0]['Quantity'])})
        return r

    def format_depth(self, depth):
        try:
            #print('Bid - %s' % depth['result']['buy'][0])
            #print('Ask - %s' % depth['result']['sell'][0])
            bids = self.sort_and_format(depth['result']['buy'], True)
            asks = self.sort_and_format(depth['result']['sell'], False)
            return {'asks': asks, 'bids': bids}
        except:
            print('uh oh! had a problem while getting bid/ask for %s' % self.code)
            return None
        
    def get_code(self):
        return self.code
    
#    def get_bid(self):
#        ticker = self.get_ticker()
#        return ticker['result']['Bid']
#    
#    def get_ask(self):
#        ticker = self.get_ticker()
#        return ticker['result']['Ask']
#    
#    def get_ticker(self):
#        url = 'https://bittrex.com/api/v1.1/public/getticker'
#        req = urllib.request.Request(url, b"market=" + bytes(self.code, "ascii"),
#                                     headers={
#            "Content-Type": "application/x-www-form-urlencoded",
#            "Accept": "*/*",
#            "User-Agent": "curl/7.24.0 (x86_64-apple-darwin12.0)"})
#        res = urllib.request.urlopen(req)
#        return json.loads(res.read().decode('utf8'))
