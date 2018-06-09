from ._gdax_base_market import GDAXBaseMarket


class GDAXETHUSD(GDAXBaseMarket):
    def __init__(self):
        super().__init__("ETH", "USD", "ETH-USD", 0.003, 0, .01)
