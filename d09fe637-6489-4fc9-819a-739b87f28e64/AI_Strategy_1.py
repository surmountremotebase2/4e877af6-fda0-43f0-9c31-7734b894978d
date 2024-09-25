from surmount.base_class import Strategy, TargetAllocation
from surmount.data import ohlcv  # Assuming ohlcv data includes open, high, low, close, volume data for each asset

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["SPY"]  # Example with SPY, can be replaced with any ticker

    @property
    def assets(self):
        return self.tickers

    @property
    def interval(self):
        # Daily interval for capturing end-of-day price drops
        return "1day"

    def run(self, data):
        allocation_dict = {}
        for ticker in self.tickers:
            if ticker in data["ohlcv"]:
                # Extracting the last two days of close prices
                recent_data = data["ohlcv"][ticker][-2:]
                if len(recent_data) == 2:
                    previous_close, current_close = recent_data[0]["close"], recent_data[1]["close"]
                    price_drop_percentage = ((current_close - previous_close) / previous_close) * 100
                    
                    # Check if the price drop is between 2% and 4%
                    if -4 < price_drop_percentage <= -2:
                        allocation_dict[ticker] = 1  # Allocate 100% to this asset
                    else:
                        allocation_dict[ticker] = 0  # Do not allocate if condition doesn't meet
                else:
                    # Log or handle cases where there isn't enough data
                    pass
            else:
                # Handle case where ticker data is not present
                pass
        
        return TargetAllocation(allocation_dict)