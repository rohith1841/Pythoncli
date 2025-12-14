"""
TWAP Strategy Logic (Bonus)
"""
import logging
from ..logging_config import setup_logging
import time
from binance import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException

setup_logging()

class TWAPBot:
    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        self.client = Client(api_key, api_secret)
        if testnet:
            self.client.FUTURES_URL = "https://testnet.binancefuture.com"
        logging.info("TWAPBot initialized | Testnet=%s", testnet)

    def validate_twap_order(self, symbol, side, total_quantity, interval, splits):
        if not symbol:
            raise ValueError("Symbol cannot be empty")
        if side not in ["BUY", "SELL"]:
            raise ValueError("Side must be BUY or SELL")
        if total_quantity <= 0:
            raise ValueError("Total quantity must be greater than 0")
        if interval <= 0:
            raise ValueError("Interval must be greater than 0")
        if splits <= 0:
            raise ValueError("Splits must be greater than 0")

    def place_twap_order(self, symbol, side, total_quantity, interval, splits):
        self.validate_twap_order(symbol, side, total_quantity, interval, splits)
        split_qty = total_quantity / splits
        order_ids = []
        for i in range(splits):
            try:
                logging.info(f"TWAP: Placing MARKET order {i+1}/{splits} | {symbol} {side} qty={split_qty}")
                order = self.client.futures_create_order(
                    symbol=symbol,
                    side=side,
                    type=Client.ORDER_TYPE_MARKET,
                    quantity=split_qty
                )
                logging.info(f"TWAP: Order {i+1} success | Response={order}")
                order_ids.append(order["orderId"])
                print(f"Order {i+1} placed: ID {order['orderId']} Status {order['status']}")
            except (BinanceAPIException, BinanceOrderException) as e:
                logging.error(f"TWAP: Order {i+1} failed | {e}")
                print(f"Order {i+1} failed: {e}")
            if i < splits - 1:
                time.sleep(interval)
        return order_ids

def main():
    print("\n=== Binance Futures Testnet TWAP Strategy ===\n")
    API_KEY = input("Enter API Key: ").strip()
    API_SECRET = input("Enter API Secret: ").strip()
    bot = TWAPBot(API_KEY, API_SECRET, testnet=True)
    while True:
        try:
            symbol = input("Symbol (e.g., BTCUSDT): ").upper().strip()
            side = input("Side (BUY/SELL): ").upper().strip()
            total_quantity = float(input("Total Quantity: "))
            interval = float(input("Interval between orders (seconds): "))
            splits = int(input("Number of splits: "))
            order_ids = bot.place_twap_order(symbol, side, total_quantity, interval, splits)
            print("\nTWAP Orders Placed Successfully!")
            print("Order IDs:", order_ids)
        except Exception as e:
            print("\nERROR:", e)
        cont = input("\nPlace another TWAP order? (y/n): ").lower()
        if cont != "y":
            break

if __name__ == "__main__":
    main()