from ._gdax_base_market import GDAXBaseMarket


class GDAXBTCUSD(GDAXBaseMarket):
    def __init__(self):
        super().__init__("BTC", "USD", "BTC-USD", 0.0025, 0, .01)
