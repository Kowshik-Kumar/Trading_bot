"""
Input validation utilities for trading parameters
Validates symbols, quantities, prices, order types, and sides
"""

import re
from typing import Tuple
from .logging_config import get_logger

logger = get_logger("validators")


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


def validate_symbol(symbol: str) -> str:
    """
    Validate trading symbol format
    
    Args:
        symbol: Trading pair symbol (e.g., 'BTCUSDT')
    
    Returns:
        str: Uppercase symbol
    
    Raises:
        ValidationError: If symbol format is invalid
    """
    if not symbol or not isinstance(symbol, str):
        raise ValidationError("Symbol must be a non-empty string")
    
    symbol = symbol.upper().strip()
    
    # Basic validation - alphanumeric only
    if not re.match(r'^[A-Z0-9]+$', symbol):
        raise ValidationError(f"Symbol '{symbol}' contains invalid characters. Use only letters and numbers.")
    
    # Most futures symbols end with USDT
    if len(symbol) < 5:
        raise ValidationError(f"Symbol '{symbol}' is too short. Expected format: BTCUSDT")
    
    logger.debug(f"Symbol validated: {symbol}")
    return symbol


def validate_side(side: str) -> str:
    """
    Validate order side
    
    Args:
        side: Order side ('BUY' or 'SELL')
    
    Returns:
        str: Uppercase side
    
    Raises:
        ValidationError: If side is invalid
    """
    if not side or not isinstance(side, str):
        raise ValidationError("Side must be a non-empty string")
    
    side = side.upper().strip()
    
    valid_sides = ['BUY', 'SELL']
    if side not in valid_sides:
        raise ValidationError(f"Invalid side '{side}'. Must be one of: {', '.join(valid_sides)}")
    
    logger.debug(f"Side validated: {side}")
    return side


def validate_order_type(order_type: str) -> str:
    """
    Validate order type
    
    Args:
        order_type: Order type ('MARKET' or 'LIMIT')
    
    Returns:
        str: Uppercase order type
    
    Raises:
        ValidationError: If order type is invalid
    """
    if not order_type or not isinstance(order_type, str):
        raise ValidationError("Order type must be a non-empty string")
    
    order_type = order_type.upper().strip()
    
    valid_types = ['MARKET', 'LIMIT']
    if order_type not in valid_types:
        raise ValidationError(f"Invalid order type '{order_type}'. Must be one of: {', '.join(valid_types)}")
    
    logger.debug(f"Order type validated: {order_type}")
    return order_type


def validate_quantity(quantity: str) -> float:
    """
    Validate order quantity
    
    Args:
        quantity: Order quantity as string or number
    
    Returns:
        float: Validated quantity
    
    Raises:
        ValidationError: If quantity is invalid
    """
    try:
        qty = float(quantity)
    except (ValueError, TypeError):
        raise ValidationError(f"Quantity '{quantity}' is not a valid number")
    
    if qty <= 0:
        raise ValidationError(f"Quantity must be greater than 0, got {qty}")
    
    # Check for reasonable limits (not too small, not astronomically large)
    if qty < 0.00001:
        raise ValidationError(f"Quantity {qty} is too small (minimum: 0.00001)")
    
    if qty > 1000000:
        raise ValidationError(f"Quantity {qty} exceeds maximum limit (1,000,000)")
    
    logger.debug(f"Quantity validated: {qty}")
    return qty


def validate_price(price: str) -> float:
    """
    Validate order price (for limit orders)
    
    Args:
        price: Order price as string or number
    
    Returns:
        float: Validated price
    
    Raises:
        ValidationError: If price is invalid
    """
    try:
        prc = float(price)
    except (ValueError, TypeError):
        raise ValidationError(f"Price '{price}' is not a valid number")
    
    if prc <= 0:
        raise ValidationError(f"Price must be greater than 0, got {prc}")
    
    # Check for reasonable limits
    if prc < 0.01:
        raise ValidationError(f"Price {prc} is too small (minimum: 0.01)")
    
    if prc > 10000000:
        raise ValidationError(f"Price {prc} exceeds maximum limit (10,000,000)")
    
    logger.debug(f"Price validated: {prc}")
    return prc


def validate_order_params(symbol: str, side: str, order_type: str, 
                         quantity: str, price: str = None) -> Tuple[str, str, str, float, float]:
    """
    Validate all order parameters at once
    
    Args:
        symbol: Trading symbol
        side: Order side
        order_type: Order type
        quantity: Order quantity
        price: Order price (required for LIMIT orders)
    
    Returns:
        Tuple containing validated (symbol, side, order_type, quantity, price)
    
    Raises:
        ValidationError: If any parameter is invalid
    """
    logger.info("Validating order parameters...")
    
    # Validate each parameter
    validated_symbol = validate_symbol(symbol)
    validated_side = validate_side(side)
    validated_type = validate_order_type(order_type)
    validated_quantity = validate_quantity(quantity)
    
    # Price validation
    validated_price = None
    if validated_type == 'LIMIT':
        if price is None:
            raise ValidationError("Price is required for LIMIT orders")
        validated_price = validate_price(price)
    elif price is not None:
        logger.warning(f"Price provided for {validated_type} order but will be ignored")
    
    logger.info("All order parameters validated successfully")
    return validated_symbol, validated_side, validated_type, validated_quantity, validated_price


def format_quantity(quantity: float, precision: int = 8) -> str:
    """
    Format quantity to remove trailing zeros
    
    Args:
        quantity: Quantity value
        precision: Number of decimal places (default: 8)
    
    Returns:
        str: Formatted quantity string
    """
    return f"{quantity:.{precision}f}".rstrip('0').rstrip('.')


def format_price(price: float, precision: int = 2) -> str:
    """
    Format price to appropriate decimal places
    
    Args:
        price: Price value
        precision: Number of decimal places (default: 2)
    
    Returns:
        str: Formatted price string
    """
    return f"{price:.{precision}f}".rstrip('0').rstrip('.')
