# Python_cli — Binance Futures Testnet Trading Bot

A small CLI and optional web UI for placing Binance USDT-M Futures orders against the Testnet.

## Features
- Market and Limit order support
- USDT-M Futures Testnet
- CLI input and validation
- Logging to `bot.log`
- Modular structure for advanced orders (Stop-Limit, OCO, TWAP)

## Setup
1. Install dependencies:
   ```bash
   source .venv/bin/activate
   pip install python-binance Flask
   ```
2. Set up your Binance Testnet API keys.

## Usage
- **Market Orders:**
  ```bash
  python src/market_orders.py
  ```
- **Limit Orders:**
  ```bash
  python src/limit_orders.py
  ```
- **Advanced Orders (Stop-Limit / OCO):**
  ```bash
  python src/advanced/oco.py
  ```
- **TWAP Strategy:**
  ```bash
  python src/advanced/twap.py
  ```

## Logs
All actions, errors, and executions are logged to `bot.log` in the project root.

## Advanced Orders
Add or improve advanced order types in `/src/advanced/` for extra credit. OCO is simulated by placing two orders; monitor & cancel counterpart on fill to implement true OCO behavior.

## Web UI (optional)
1. Ensure venv is active:
   ```bash
   source .venv/bin/activate
   ```
2. Start the server:
   ```bash
   python src/web/app.py
   ```
3. Open `http://127.0.0.1:5000/` in your browser.

The web form supports MARKET, LIMIT, STOP-LIMIT, OCO, and TWAP. Responses are shown as JSON and the latest 50 lines of `bot.log` are displayed.
