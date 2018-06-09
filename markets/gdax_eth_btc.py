from ._gdax_base_market import GDAXBaseMarket


class GDAXETHBTC(GDAXBaseMarket):
    def __init__(self):
        super().__init__("ETH", "BTC", "ETH-BTC", 0.003, 0, .00001)
