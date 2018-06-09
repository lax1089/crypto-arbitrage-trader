from ._gdax_base_market import GDAXBaseMarket


class GDAXLTCBTC(GDAXBaseMarket):
    def __init__(self):
        super().__init__("LTC", "BTC", "LTC-BTC", 0.003, 0, .00001)
