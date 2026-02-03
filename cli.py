#!/usr/bin/env python3
"""
Binance Futures Trading Bot - CLI Interface
Command-line interface for placing orders on Binance Futures Testnet
"""

import argparse
import sys
from typing import Optional
from trading_bot.bot.client import BinanceFuturesClient
from trading_bot.bot.orders import OrderManager
from trading_bot.bot.validators import ValidationError
from trading_bot.bot.logging_config import setup_logging, get_logger


def create_parser() -> argparse.ArgumentParser:
    """
    Create and configure the argument parser
    
    Returns:
        argparse.ArgumentParser: Configured parser
    """
    parser = argparse.ArgumentParser(
        description='Binance Futures Trading Bot - Place orders on Binance Futures Testnet',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Place a market buy order
  python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
  
  # Place a limit sell order
  python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.05 --price 2000
  
  # Check account information
  python cli.py --account
  
  # Get current price for a symbol
  python cli.py --price BTCUSDT
  
  # Test API connectivity
  python cli.py --test

For more information, visit: https://testnet.binancefuture.com
        """
    )
    
    # Order parameters
    parser.add_argument(
        '--symbol',
        type=str,
        help='Trading symbol (e.g., BTCUSDT, ETHUSDT)'
    )
    
    parser.add_argument(
        '--side',
        type=str,
        choices=['BUY', 'SELL', 'buy', 'sell'],
        help='Order side: BUY or SELL'
    )
    
    parser.add_argument(
        '--type',
        type=str,
        choices=['MARKET', 'LIMIT', 'market', 'limit'],
        help='Order type: MARKET or LIMIT'
    )
    
    parser.add_argument(
        '--quantity',
        type=str,
        help='Order quantity (e.g., 0.001 for BTC)'
    )
    
    parser.add_argument(
        '--price',
        type=str,
        help='Limit price (required for LIMIT orders)'
    )
    
    # Utility commands
    parser.add_argument(
        '--account',
        action='store_true',
        help='Display account information'
    )
    
    parser.add_argument(
        '--get-price',
        type=str,
        metavar='SYMBOL',
        help='Get current price for a symbol'
    )
    
    parser.add_argument(
        '--test',
        action='store_true',
        help='Test API connectivity'
    )
    
    # Logging options
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    return parser


def display_banner():
    """Display application banner"""
    banner = """
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║        BINANCE FUTURES TRADING BOT                         ║
║        Testnet Environment (USDT-M)                        ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
"""
    print(banner)


def display_account_info(client: BinanceFuturesClient):
    """
    Display account information
    
    Args:
        client: BinanceFuturesClient instance
    """
    try:
        account = client.get_account_info()
        
        print("\n" + "="*60)
        print("ACCOUNT INFORMATION")
        print("="*60)
        
        # Display balances
        print("\nBalances:")
        print("-" * 60)
        
        assets_with_balance = [
            asset for asset in account.get('assets', [])
            if float(asset.get('walletBalance', 0)) > 0
        ]
        
        if assets_with_balance:
            for asset in assets_with_balance:
                asset_name = asset.get('asset')
                balance = float(asset.get('walletBalance', 0))
                available = float(asset.get('availableBalance', 0))
                
                print(f"{asset_name:10} | Balance: {balance:>15.8f} | Available: {available:>15.8f}")
        else:
            print("No assets with balance found.")
        
        # Display positions if any
        positions = account.get('positions', [])
        open_positions = [p for p in positions if float(p.get('positionAmt', 0)) != 0]
        
        if open_positions:
            print("\nOpen Positions:")
            print("-" * 60)
            for pos in open_positions:
                symbol = pos.get('symbol')
                position_amt = float(pos.get('positionAmt', 0))
                entry_price = float(pos.get('entryPrice', 0))
                unrealized_pnl = float(pos.get('unrealizedProfit', 0))
                
                print(f"{symbol:10} | Amount: {position_amt:>12.8f} | "
                      f"Entry: {entry_price:>10.2f} | PnL: {unrealized_pnl:>10.2f}")
        
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n✗ Error fetching account information: {str(e)}\n")
        logger = get_logger("cli")
        logger.error(f"Error fetching account info: {str(e)}")


def get_symbol_price(client: BinanceFuturesClient, symbol: str):
    """
    Get and display current price for a symbol
    
    Args:
        client: BinanceFuturesClient instance
        symbol: Trading symbol
    """
    try:
        price = client.get_current_price(symbol)
        
        print("\n" + "="*60)
        print(f"CURRENT PRICE: {symbol}")
        print("="*60)
        print(f"{price:,.2f} USDT")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n✗ Error fetching price: {str(e)}\n")
        logger = get_logger("cli")
        logger.error(f"Error fetching price: {str(e)}")


def test_connectivity(client: BinanceFuturesClient):
    """
    Test API connectivity
    
    Args:
        client: BinanceFuturesClient instance
    """
    print("\nTesting API connectivity...")
    
    if client.test_connectivity():
        print("✓ API connectivity test successful!\n")
    else:
        print("✗ API connectivity test failed!\n")


def main():
    """Main CLI entry point"""
    parser = create_parser()
    args = parser.parse_args()
    
    # Display banner
    display_banner()
    
    # Setup logging
    import logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logger = setup_logging(log_level)
    
    try:
        # Initialize client
        logger.info("Initializing Binance Futures client...")
        client = BinanceFuturesClient()
        
        # Handle utility commands
        if args.test:
            test_connectivity(client)
            return 0
        
        if args.account:
            display_account_info(client)
            return 0
        
        if args.get_price:
            get_symbol_price(client, args.get_price.upper())
            return 0
        
        # Validate order parameters
        if not all([args.symbol, args.side, args.type, args.quantity]):
            parser.print_help()
            print("\n✗ Error: To place an order, you must provide: --symbol, --side, --type, and --quantity\n")
            return 1
        
        # Check if price is required for limit orders
        if args.type.upper() == 'LIMIT' and not args.price:
            print("\n✗ Error: --price is required for LIMIT orders\n")
            return 1
        
        # Initialize order manager and execute order
        order_manager = OrderManager(client)
        
        try:
            order_response = order_manager.execute_order(
                symbol=args.symbol,
                side=args.side,
                order_type=args.type,
                quantity=args.quantity,
                price=args.price
            )
            
            logger.info(f"Order completed successfully. Order ID: {order_response.get('orderId')}")
            return 0
            
        except ValidationError as e:
            print(f"\n✗ Validation Error: {str(e)}\n")
            logger.error(f"Validation error: {str(e)}")
            return 1
        
    except ValueError as e:
        print(f"\n✗ Configuration Error: {str(e)}")
        print("Please ensure your .env file contains valid BINANCE_API_KEY and BINANCE_API_SECRET\n")
        logger.error(f"Configuration error: {str(e)}")
        return 1
    
    except KeyboardInterrupt:
        print("\n\n✗ Operation cancelled by user\n")
        return 1
    
    except Exception as e:
        print(f"\n✗ Unexpected Error: {str(e)}\n")
        logger.exception("Unexpected error in main")
        return 1


if __name__ == '__main__':
    sys.exit(main())
