import urllib.request
import urllib.error
import urllib.parse
import json
from ._kraken_base_market import KrakenBaseMarket

class KrakenMarketGenerator():
    def __init__(self):
        print("initialized kraken market gen")

    def get_market_json(self):
        url = 'https://api.kraken.com/0/public/AssetPairs'
        req = urllib.request.Request(url,
                                     headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "*/*",
            "User-Agent": "curl/7.24.0 (x86_64-apple-darwin12.0)"})
        res = urllib.request.urlopen(req)

        market_json = json.loads(res.read().decode('utf8'))
        
        return market_json

    def get_markets(self, market_json):
        market_names = list()
        for i in market_json['result']:
            #don't want to include 'dark pool' markets for now, which are denoted with .d extension
            if ".d" not in i:
                market_names.append(i)
    
        markets = list()
        for market_name in market_names:
            taker_fee = market_json['result'][market_name]['fees'][0][1]/100
            if 'fees_maker' not in market_json['result'][market_name]:
                maker_fee = taker_fee
            else:
                maker_fee = market_json['result'][market_name]['fees_maker'][0][1]/100
            
            curr1 = market_json['result'][market_name]['base']
            curr2 = market_json['result'][market_name]['quote']
            
            markets.append(KrakenBaseMarket(curr1, curr2, market_name, taker_fee, maker_fee, 0))
        
        return markets