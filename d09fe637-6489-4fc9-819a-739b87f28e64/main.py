from surmount.base_class import Strategy, TargetAllocation
from surmount.data import InstitutionalOwnership, Dividend, Ratios
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Define tickers of interest in the S&P 500 (example tickers used here)
        self.tickers = ["JNJ", "PG", "KO", "PEP", "WMT"]  # Example defensive stocks
        self.data_list = []
        # Add data sources
        self.data_list += [Dividend(i) for i in self.tickers]
        self.data_list += [Ratios(i) for i in self.tickers]
    
    @property
    def interval(self):
        # Use daily data for analysis
        return "1day"

    @property
    def assets(self):
        # Return the list of tickers
        return self.tickers
    
    @property
    def data(self):
        # Return the list of data sources utilized
        return self.data_list
    
    def run(self, data):
        allocation_dict = {}
        for ticker in self.tickers:
            # Assume a low beta threshold (for less volatility) & a minimum dividend yield
            low_beta_threshold = 1  # Beta less than 1 is considered low risk compared to the market
            min_dividend_yield = 2.5  # Minimum dividend yield percent
            
            # Data accessibility checks
            ratios_data = data.get(("ratios", ticker))
            dividend_data = data.get(("dividend", ticker))

            if ratios_data and dividend_data:
                # Extract latest available beta and dividend yield
                beta = ratios_data[-1].get("beta", 0)
                dividend_yield = dividend_data[-1].get("dividendYield", 0) * 100  # Convert to percentage

                # Invest in the stock only if it meets the criteria
                if beta < low_beta_threshold and dividend_yield >= min_dividend_yield:
                    allocation_dict[ticker] = 1.0 / len(self.tickers)
                else:
                    allocation_dict[ticker] = 0
            else:
                # If data is missing for a ticker, skip allocation to it
                log(f"Missing data for {ticker}, skipping allocation.")
                allocation_dict[ticker] = 0

        # Normalize allocations to ensure they sum up to 1 or less
        total_allocation = sum(allocation_dict.values())
        if total_allocation > 1:
            allocation_dict = {ticker: weight / total_allocation for ticker, weight in allocation_dict.items()}

        return TargetAllocation(allocation_dict)