"""
Binance Futures API client wrapper
Handles authentication and API communication with Binance Futures Testnet
"""

import os
from typing import Optional
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from dotenv import load_dotenv
from .logging_config import get_logger

# Load environment variables
load_dotenv()

logger = get_logger("client")


class BinanceFuturesClient:
    """
    Wrapper class for Binance Futures API client
    Configured for testnet environment
    """
    
    # Binance Futures Testnet URLs
    TESTNET_URL = "https://testnet.binancefuture.com"
    TESTNET_API_URL = "https://testnet.binancefuture.com/fapi"
    
    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None):
        """
        Initialize the Binance Futures client
        
        Args:
            api_key: Binance API key (if not provided, reads from .env)
            api_secret: Binance API secret (if not provided, reads from .env)
        
        Raises:
            ValueError: If API credentials are not provided
        """
        self.api_key = api_key or os.getenv("BINANCE_API_KEY")
        self.api_secret = api_secret or os.getenv("BINANCE_API_SECRET")
        
        if not self.api_key or not self.api_secret:
            error_msg = "API credentials not found. Please set BINANCE_API_KEY and BINANCE_API_SECRET in .env file"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        logger.info("Initializing Binance Futures client for testnet")
        
        try:
            # Initialize client with testnet configuration
            self.client = Client(
                api_key=self.api_key,
                api_secret=self.api_secret,
                testnet=False  # We'll manually set the testnet URL
            )
            
            # Set the testnet URLs for Futures
            self.client.FUTURES_URL = self.TESTNET_API_URL
            self.client.FUTURES_DATA_URL = self.TESTNET_API_URL
            
            logger.info("Binance Futures client initialized successfully")
            logger.info(f"Using Futures testnet URL: {self.TESTNET_API_URL}")
            
        except Exception as e:
            logger.error(f"Failed to initialize Binance client: {str(e)}")
            raise
    
    def test_connectivity(self) -> bool:
        """
        Test connectivity to Binance Futures API
        
        Returns:
            bool: True if connection is successful
        """
        try:
            logger.info("Testing API connectivity...")
            ping = self.client.futures_ping()
            logger.info("API connectivity test successful")
            return True
        except BinanceAPIException as e:
            logger.error(f"Binance API error during connectivity test: {e.message}")
            return False
        except BinanceRequestException as e:
            logger.error(f"Binance request error during connectivity test: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during connectivity test: {str(e)}")
            return False
    
    def get_account_info(self) -> dict:
        """
        Get futures account information
        
        Returns:
            dict: Account information including balances
        """
        try:
            logger.info("Fetching account information...")
            account = self.client.futures_account()
            logger.info("Account information retrieved successfully")
            return account
        except BinanceAPIException as e:
            logger.error(f"Binance API error getting account info: {e.message}")
            raise
        except Exception as e:
            logger.error(f"Error getting account info: {str(e)}")
            raise
    
    def get_symbol_info(self, symbol: str) -> dict:
        """
        Get trading rules and information for a specific symbol
        
        Args:
            symbol: Trading pair symbol (e.g., 'BTCUSDT')
        
        Returns:
            dict: Symbol information including filters and trading rules
        """
        try:
            logger.info(f"Fetching symbol info for {symbol}...")
            exchange_info = self.client.futures_exchange_info()
            
            for s in exchange_info['symbols']:
                if s['symbol'] == symbol:
                    logger.info(f"Symbol info for {symbol} retrieved successfully")
                    return s
            
            logger.warning(f"Symbol {symbol} not found in exchange info")
            return None
            
        except BinanceAPIException as e:
            logger.error(f"Binance API error getting symbol info: {e.message}")
            raise
        except Exception as e:
            logger.error(f"Error getting symbol info: {str(e)}")
            raise
    
    def get_current_price(self, symbol: str) -> float:
        """
        Get current price for a symbol
        
        Args:
            symbol: Trading pair symbol (e.g., 'BTCUSDT')
        
        Returns:
            float: Current price
        """
        try:
            logger.info(f"Fetching current price for {symbol}...")
            ticker = self.client.futures_symbol_ticker(symbol=symbol)
            price = float(ticker['price'])
            logger.info(f"Current price for {symbol}: {price}")
            return price
        except BinanceAPIException as e:
            logger.error(f"Binance API error getting price: {e.message}")
            raise
        except Exception as e:
            logger.error(f"Error getting price: {str(e)}")
            raise
    
    def place_order(self, **params) -> dict:
        """
        Place an order on Binance Futures
        
        Args:
            **params: Order parameters (symbol, side, type, quantity, price, etc.)
        
        Returns:
            dict: Order response from Binance
        """
        try:
            logger.info(f"Placing order with params: {params}")
            order = self.client.futures_create_order(**params)
            logger.info(f"Order placed successfully. Order ID: {order.get('orderId')}")
            return order
        except BinanceAPIException as e:
            logger.error(f"Binance API error placing order: {e.message} (Code: {e.code})")
            raise
        except BinanceRequestException as e:
            logger.error(f"Binance request error placing order: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error placing order: {str(e)}")
            raise
    
    def get_order(self, symbol: str, order_id: int) -> dict:
        """
        Get order information
        
        Args:
            symbol: Trading pair symbol
            order_id: Order ID
        
        Returns:
            dict: Order information
        """
        try:
            logger.info(f"Fetching order info for order ID {order_id} on {symbol}...")
            order = self.client.futures_get_order(symbol=symbol, orderId=order_id)
            logger.info(f"Order info retrieved successfully")
            return order
        except BinanceAPIException as e:
            logger.error(f"Binance API error getting order: {e.message}")
            raise
        except Exception as e:
            logger.error(f"Error getting order: {str(e)}")
            raise
    
    def cancel_order(self, symbol: str, order_id: int) -> dict:
        """
        Cancel an open order
        
        Args:
            symbol: Trading pair symbol
            order_id: Order ID to cancel
        
        Returns:
            dict: Cancellation response
        """
        try:
            logger.info(f"Cancelling order {order_id} on {symbol}...")
            result = self.client.futures_cancel_order(symbol=symbol, orderId=order_id)
            logger.info(f"Order cancelled successfully")
            return result
        except BinanceAPIException as e:
            logger.error(f"Binance API error cancelling order: {e.message}")
            raise
        except Exception as e:
            logger.error(f"Error cancelling order: {str(e)}")
            raise
