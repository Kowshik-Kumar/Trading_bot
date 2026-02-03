"""
Order placement logic for Binance Futures
Handles market and limit orders with proper error handling
"""

from typing import Dict, Optional
from binance.exceptions import BinanceAPIException
from .client import BinanceFuturesClient
from .validators import validate_order_params, format_quantity, format_price
from .logging_config import get_logger

logger = get_logger("orders")


class OrderManager:
    """
    Manages order placement and tracking for Binance Futures
    """
    
    def __init__(self, client: BinanceFuturesClient):
        """
        Initialize OrderManager
        
        Args:
            client: BinanceFuturesClient instance
        """
        self.client = client
        logger.info("OrderManager initialized")
    
    def place_market_order(self, symbol: str, side: str, quantity: float) -> Dict:
        """
        Place a market order
        
        Args:
            symbol: Trading symbol (e.g., 'BTCUSDT')
            side: Order side ('BUY' or 'SELL')
            quantity: Order quantity
        
        Returns:
            dict: Order response
        """
        logger.info(f"Preparing MARKET order: {side} {quantity} {symbol}")
        
        # Prepare order parameters
        order_params = {
            'symbol': symbol,
            'side': side,
            'type': 'MARKET',
            'quantity': quantity
        }
        
        # Log order request
        logger.info(f"Order Request: {order_params}")
        
        try:
            # Place the order
            order_response = self.client.place_order(**order_params)
            
            # Log successful order
            logger.info(f"Order executed successfully!")
            logger.info(f"Order ID: {order_response.get('orderId')}")
            logger.info(f"Status: {order_response.get('status')}")
            
            return order_response
            
        except BinanceAPIException as e:
            logger.error(f"Binance API error: {e.message} (Code: {e.code})")
            raise
        except Exception as e:
            logger.error(f"Unexpected error placing market order: {str(e)}")
            raise
    
    def place_limit_order(self, symbol: str, side: str, quantity: float, 
                         price: float, time_in_force: str = 'GTC') -> Dict:
        """
        Place a limit order
        
        Args:
            symbol: Trading symbol (e.g., 'BTCUSDT')
            side: Order side ('BUY' or 'SELL')
            quantity: Order quantity
            price: Limit price
            time_in_force: Time in force (default: 'GTC' - Good Till Cancel)
        
        Returns:
            dict: Order response
        """
        logger.info(f"Preparing LIMIT order: {side} {quantity} {symbol} @ {price}")
        
        # Prepare order parameters
        order_params = {
            'symbol': symbol,
            'side': side,
            'type': 'LIMIT',
            'quantity': quantity,
            'price': price,
            'timeInForce': time_in_force
        }
        
        # Log order request
        logger.info(f"Order Request: {order_params}")
        
        try:
            # Place the order
            order_response = self.client.place_order(**order_params)
            
            # Log successful order
            logger.info(f"Order placed successfully!")
            logger.info(f"Order ID: {order_response.get('orderId')}")
            logger.info(f"Status: {order_response.get('status')}")
            
            return order_response
            
        except BinanceAPIException as e:
            logger.error(f"Binance API error: {e.message} (Code: {e.code})")
            raise
        except Exception as e:
            logger.error(f"Unexpected error placing limit order: {str(e)}")
            raise
    
    def execute_order(self, symbol: str, side: str, order_type: str, 
                     quantity: str, price: Optional[str] = None) -> Dict:
        """
        Execute an order with validation
        
        Args:
            symbol: Trading symbol
            side: Order side
            order_type: Order type ('MARKET' or 'LIMIT')
            quantity: Order quantity (as string)
            price: Order price (as string, required for LIMIT)
        
        Returns:
            dict: Order response with additional formatted information
        """
        # Validate all parameters
        validated_symbol, validated_side, validated_type, validated_qty, validated_price = \
            validate_order_params(symbol, side, order_type, quantity, price)
        
        # Print order summary
        print("\n" + "="*60)
        print("ORDER REQUEST SUMMARY")
        print("="*60)
        print(f"Symbol:        {validated_symbol}")
        print(f"Side:          {validated_side}")
        print(f"Type:          {validated_type}")
        print(f"Quantity:      {format_quantity(validated_qty)}")
        if validated_price:
            print(f"Price:         {format_price(validated_price)}")
        print("="*60 + "\n")
        
        # Execute the appropriate order type
        try:
            if validated_type == 'MARKET':
                order_response = self.place_market_order(
                    validated_symbol, 
                    validated_side, 
                    validated_qty
                )
            else:  # LIMIT
                order_response = self.place_limit_order(
                    validated_symbol, 
                    validated_side, 
                    validated_qty, 
                    validated_price
                )
            
            # Print order response details
            self._print_order_response(order_response)
            
            return order_response
            
        except Exception as e:
            print("\n" + "="*60)
            print("ORDER FAILED")
            print("="*60)
            print(f"Error: {str(e)}")
            print("="*60 + "\n")
            raise
    
    def _print_order_response(self, order: Dict):
        """
        Print formatted order response
        
        Args:
            order: Order response dictionary
        """
        print("\n" + "="*60)
        print("ORDER RESPONSE")
        print("="*60)
        print(f"Order ID:      {order.get('orderId')}")
        print(f"Status:        {order.get('status')}")
        print(f"Symbol:        {order.get('symbol')}")
        print(f"Side:          {order.get('side')}")
        print(f"Type:          {order.get('type')}")
        print(f"Quantity:      {order.get('origQty', 'N/A')}")
        
        # Executed quantity (for market orders)
        executed_qty = order.get('executedQty', '0')
        if executed_qty and float(executed_qty) > 0:
            print(f"Executed Qty:  {executed_qty}")
        
        # Average price (for filled orders)
        avg_price = order.get('avgPrice')
        if avg_price and float(avg_price) > 0:
            print(f"Avg Price:     {avg_price}")
        
        # Limit price (for limit orders)
        if order.get('price'):
            print(f"Limit Price:   {order.get('price')}")
        
        print(f"Time in Force: {order.get('timeInForce', 'N/A')}")
        print(f"Client Order ID: {order.get('clientOrderId', 'N/A')}")
        print("="*60)
        
        # Success message
        status = order.get('status', '')
        if status in ['FILLED', 'NEW', 'PARTIALLY_FILLED']:
            print("\n✓ Order placed successfully!")
        else:
            print(f"\n⚠ Order status: {status}")
        
        print()
    
    def get_order_status(self, symbol: str, order_id: int) -> Dict:
        """
        Get status of an existing order
        
        Args:
            symbol: Trading symbol
            order_id: Order ID
        
        Returns:
            dict: Order information
        """
        try:
            logger.info(f"Fetching order status for {order_id} on {symbol}")
            order = self.client.get_order(symbol, order_id)
            self._print_order_response(order)
            return order
        except Exception as e:
            logger.error(f"Error fetching order status: {str(e)}")
            raise
    
    def cancel_order(self, symbol: str, order_id: int) -> Dict:
        """
        Cancel an open order
        
        Args:
            symbol: Trading symbol
            order_id: Order ID to cancel
        
        Returns:
            dict: Cancellation response
        """
        try:
            logger.info(f"Cancelling order {order_id} on {symbol}")
            result = self.client.cancel_order(symbol, order_id)
            
            print("\n" + "="*60)
            print("ORDER CANCELLED")
            print("="*60)
            print(f"Order ID:      {result.get('orderId')}")
            print(f"Symbol:        {result.get('symbol')}")
            print(f"Status:        {result.get('status')}")
            print("="*60 + "\n")
            
            return result
        except Exception as e:
            logger.error(f"Error cancelling order: {str(e)}")
            raise
