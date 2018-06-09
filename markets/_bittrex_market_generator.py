import urllib.request
import urllib.error
import urllib.parse
import json
from ._bittrex_base_market import BittrexBaseMarket

class BittrexMarketGenerator():
    def __init__(self):
        print("initialized bittrex market gen")

    def get_market_json(self):
        url = 'https://bittrex.com/api/v1.1/public/getmarkets'
        req = urllib.request.Request(url,
                                     headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "*/*",
            "User-Agent": "curl/7.24.0 (x86_64-apple-darwin12.0)"})
        res = urllib.request.urlopen(req)

        market_json = json.loads(res.read().decode('utf8'))
        
        return market_json
        
    def get_market_summary_json(self):
        url = 'https://bittrex.com/api/v1.1/public/getmarketsummaries'
        req = urllib.request.Request(url,
                                     headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "*/*",
            "User-Agent": "curl/7.24.0 (x86_64-apple-darwin12.0)"})
        res = urllib.request.urlopen(req)

        market_summary_json = json.loads(res.read().decode('utf8'))
        
        return market_summary_json

    def get_markets(self, market_json):
        markets = list()
        for market in market_json['result']:
            
            market_name = market['MarketName']
            curr1 = market['MarketCurrency']
            curr2 = market['BaseCurrency']
            
            markets.append(BittrexBaseMarket(curr1, curr2, market_name, 0.0025, 0.0025, 0))
        
        return markets
        
    def update_markets(self, markets):
        market_summary_json = self.get_market_summary_json()
        for market in markets:
            for i in market_summary_json['result']:
                if i['MarketName'] == market.code:
                    market.bid = i['Bid']
                    market.ask = i['Ask']
            
            