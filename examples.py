"""
Example usage scripts for the Binance Futures Trading Bot
Run these after setting up your .env file with API credentials
"""

# Example 1: Test API Connectivity
# python cli.py --test

# Example 2: Check Account Information
# python cli.py --account

# Example 3: Get Current Price
# python cli.py --get-price BTCUSDT
# python cli.py --get-price ETHUSDT

# Example 4: Place Market Buy Order
# python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

# Example 5: Place Market Sell Order
# python cli.py --symbol ETHUSDT --side SELL --type MARKET --quantity 0.01

# Example 6: Place Limit Buy Order
# python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001 --price 30000

# Example 7: Place Limit Sell Order
# python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.05 --price 2500

# Example 8: Verbose Logging
# python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001 --verbose

# Common Trading Pairs on Binance Futures:
# - BTCUSDT (Bitcoin)
# - ETHUSDT (Ethereum)
# - BNBUSDT (Binance Coin)
# - ADAUSDT (Cardano)
# - SOLUSDT (Solana)
# - DOTUSDT (Polkadot)
# - MATICUSDT (Polygon)

# Notes:
# 1. Always start with small quantities for testing
# 2. MARKET orders execute immediately at current market price
# 3. LIMIT orders wait for the specified price to be reached
# 4. Check logs/ directory for detailed execution logs
# 5. Use --test to verify API connectivity before trading
