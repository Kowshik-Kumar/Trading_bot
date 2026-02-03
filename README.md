# Binance Futures Trading Bot

A Python application for placing orders on Binance Futures Testnet (USDT-M) with a clean, reusable structure, proper logging, and comprehensive error handling.

## 🚀 Features

- ✅ Place **Market** and **Limit** orders on Binance Futures Testnet
- ✅ Support for both **BUY** and **SELL** sides
- ✅ **CLI interface** with argument validation
- ✅ **Structured code** with separation of concerns
- ✅ **Comprehensive logging** to file with timestamps
- ✅ **Error handling** for API errors, network failures, and invalid inputs
- ✅ Account information and price checking utilities
- ✅ Clean output formatting with order summaries

## 📁 Project Structure

```
trading_bot/
├── trading_bot/
│   ├── __init__.py
│   └── bot/
│       ├── __init__.py
│       ├── client.py          # Binance API client wrapper
│       ├── orders.py           # Order placement logic
│       ├── validators.py       # Input validation
│       └── logging_config.py   # Logging configuration
├── cli.py                      # CLI entry point
├── requirements.txt            # Python dependencies
├── .env.example                # Example environment variables
├── .gitignore                  # Git ignore file
└── README.md                   # This file
```

## 🛠️ Setup

### Prerequisites

- Python 3.8 or higher
- Binance Futures Testnet account
- API credentials from Binance Futures Testnet

### Step 1: Register on Binance Futures Testnet

1. Visit [Binance Futures Testnet](https://testnet.binancefuture.com)
2. Register and activate your testnet account
3. Generate API credentials (API Key and Secret Key)

### Step 2: Clone or Download the Project

```bash
# If using Git
git clone <repository-url>
cd intern app

# Or download and extract the ZIP file
```

### Step 3: Install Dependencies

```bash
# Create a virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### Step 4: Configure API Credentials

1. Copy the `.env.example` file to `.env`:
   ```bash
   copy .env.example .env
   ```

2. Edit the `.env` file and add your API credentials:
   ```
   BINANCE_API_KEY=your_actual_api_key_here
   BINANCE_API_SECRET=your_actual_api_secret_here
   ```

## 📖 Usage

### Basic Commands

#### Test API Connectivity
```bash
python cli.py --test
```

#### Check Account Information
```bash
python cli.py --account
```

#### Get Current Price for a Symbol
```bash
python cli.py --get-price BTCUSDT
```

### Placing Orders

#### Market Order (BUY)
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

#### Market Order (SELL)
```bash
python cli.py --symbol ETHUSDT --side SELL --type MARKET --quantity 0.01
```

#### Limit Order (BUY)
```bash
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001 --price 30000
```

#### Limit Order (SELL)
```bash
python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.05 --price 2500
```

### Command-Line Arguments

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `--symbol` | Yes* | Trading pair symbol | `BTCUSDT`, `ETHUSDT` |
| `--side` | Yes* | Order side | `BUY`, `SELL` |
| `--type` | Yes* | Order type | `MARKET`, `LIMIT` |
| `--quantity` | Yes* | Order quantity | `0.001`, `0.05` |
| `--price` | For LIMIT | Limit price | `30000`, `2500` |
| `--account` | No | Show account info | - |
| `--get-price` | No | Get current price | `BTCUSDT` |
| `--test` | No | Test connectivity | - |
| `--verbose` | No | Enable verbose logging | - |

*Required for placing orders

## 📊 Output Examples

### Market Order Output
```
============================================================
ORDER REQUEST SUMMARY
============================================================
Symbol:        BTCUSDT
Side:          BUY
Type:          MARKET
Quantity:      0.001
============================================================

============================================================
ORDER RESPONSE
============================================================
Order ID:      12345678
Status:        FILLED
Symbol:        BTCUSDT
Side:          BUY
Type:          MARKET
Quantity:      0.001
Executed Qty:  0.001
Avg Price:     42350.50
Time in Force: N/A
Client Order ID: web_xxxxxxxxxxxxxxxx

✓ Order placed successfully!
```

### Limit Order Output
```
============================================================
ORDER REQUEST SUMMARY
============================================================
Symbol:        ETHUSDT
Side:          SELL
Type:          LIMIT
Quantity:      0.05
Price:         2500
============================================================

============================================================
ORDER RESPONSE
============================================================
Order ID:      87654321
Status:        NEW
Symbol:        ETHUSDT
Side:          SELL
Type:          LIMIT
Quantity:      0.05
Limit Price:   2500.00
Time in Force: GTC
Client Order ID: web_xxxxxxxxxxxxxxxx

✓ Order placed successfully!
```

## 📝 Logging

All operations are logged to files in the `logs/` directory with the following format:
- **Filename**: `trading_bot_YYYYMMDD_HHMMSS.log`
- **Content**: API requests, responses, errors, and debug information
- **Console**: Simplified output for user visibility
- **File**: Detailed logging with function names and line numbers

Example log entry:
```
2026-02-02 14:30:45 - trading_bot.orders - INFO - place_market_order:45 - Preparing MARKET order: BUY 0.001 BTCUSDT
2026-02-02 14:30:45 - trading_bot.orders - INFO - place_market_order:55 - Order Request: {'symbol': 'BTCUSDT', 'side': 'BUY', 'type': 'MARKET', 'quantity': 0.001}
2026-02-02 14:30:46 - trading_bot.orders - INFO - place_market_order:63 - Order executed successfully!
```

## 🔒 Security Best Practices

1. **Never commit** your `.env` file to version control
2. **Use Testnet only** for development and testing
3. **Keep API credentials secure** and rotate them regularly
4. **Enable IP restrictions** on your API keys in Binance settings
5. **Use read-only keys** when possible (for testing)

## ⚠️ Error Handling

The application handles various error scenarios:

- ✅ **Invalid credentials**: Clear error message about missing/invalid API keys
- ✅ **Network errors**: Timeout and connection error handling
- ✅ **API errors**: Binance API error codes and messages
- ✅ **Validation errors**: Input validation with helpful error messages
- ✅ **Invalid symbols**: Symbol format and existence validation
- ✅ **Insufficient balance**: Balance check error handling

## 🧪 Testing

### Test Checklist

1. ✅ Test API connectivity: `python cli.py --test`
2. ✅ Check account info: `python cli.py --account`
3. ✅ Get current price: `python cli.py --get-price BTCUSDT`
4. ✅ Place market order: `python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001`
5. ✅ Place limit order: `python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001 --price 30000`
6. ✅ Check log files in `logs/` directory

## 📋 Requirements

- Python 3.8+
- python-binance==1.0.19
- python-dotenv==1.0.0
- requests==2.31.0
- colorama==0.4.6 (optional, for colored output on Windows)

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## 📄 License

This project is provided as-is for educational and testing purposes.

## ⚡ Quick Start Guide

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure API credentials
copy .env.example .env
# Edit .env with your credentials

# 3. Test connection
python cli.py --test

# 4. Place your first order
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

## 🐛 Troubleshooting

### "API credentials not found"
- Ensure `.env` file exists in the project root
- Check that `BINANCE_API_KEY` and `BINANCE_API_SECRET` are properly set

### "Connection refused" or timeout errors
- Check your internet connection
- Verify testnet is accessible: https://testnet.binancefuture.com
- Check if your API keys are valid

### "Invalid symbol" error
- Verify the symbol exists on Binance Futures
- Use correct format: `BTCUSDT`, `ETHUSDT` (no spaces)
- Symbols are case-insensitive but will be converted to uppercase

### Module import errors
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again
- Check Python version (3.8+ required)

## 📞 Support

For issues related to:
- **Binance API**: [Binance API Documentation](https://binance-docs.github.io/apidocs/futures/en/)
- **Testnet**: [Binance Futures Testnet](https://testnet.binancefuture.com)

## 🎯 Assumptions

1. Users have basic knowledge of cryptocurrency trading
2. API credentials are obtained from Binance Futures Testnet
3. The application is used for testing purposes only
4. Users understand the risks of trading and API usage
5. Python 3.8+ is installed on the system
6. Users have internet connectivity to access Binance API

## 📈 Future Enhancements (Bonus Features)

Possible extensions to this project:
- Stop-Limit and OCO orders
- TWAP (Time-Weighted Average Price) execution
- Grid trading strategy
- Interactive CLI menu with prompts
- Web-based UI using Flask/FastAPI
- Real-time position monitoring
- Trade history and analytics

---

**Note**: This application is designed for the Binance Futures Testnet environment. Do not use production API keys with this application.
