from ._gdax_base_market import GDAXBaseMarket


class GDAXLTCUSD(GDAXBaseMarket):
    def __init__(self):
        super().__init__("LTC", "USD", "LTC-USD", 0.003, 0, .01)
