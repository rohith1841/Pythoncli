"""
Market Orders Logic for Binance Futures Testnet Bot
"""
import logging
from .logging_config import setup_logging
from binance import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException

setup_logging()

class BasicBot:
    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        self.client = Client(api_key, api_secret)
        if testnet:
            self.client.FUTURES_URL = "https://testnet.binancefuture.com"
        logging.info("Bot initialized | Testnet=%s", testnet)

    def validate_order(self, symbol, side, quantity):
        if not symbol:
            raise ValueError("Symbol cannot be empty")
        if side not in ["BUY", "SELL"]:
            raise ValueError("Side must be BUY or SELL")
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")

    def place_market_order(self, symbol, side, quantity):
        self.validate_order(symbol, side, quantity)
        try:
            logging.info("Placing MARKET order | %s %s qty=%s", symbol, side, quantity)
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type=Client.ORDER_TYPE_MARKET,
                quantity=quantity
            )
            logging.info("Order success | Response=%s", order)
            return order
        except (BinanceAPIException, BinanceOrderException) as e:
            logging.error("Order failed | %s", e)
            raise

def main():
    print("\n=== Binance Futures Testnet MARKET Order ===\n")
    API_KEY = input("Enter API Key: ").strip()
    API_SECRET = input("Enter API Secret: ").strip()
    bot = BasicBot(API_KEY, API_SECRET, testnet=True)
    while True:
        try:
            symbol = input("Symbol (e.g., BTCUSDT): ").upper().strip()
            side = input("Side (BUY/SELL): ").upper().strip()
            quantity = float(input("Quantity: "))
            order = bot.place_market_order(symbol, side, quantity)
            print("\nOrder Placed Successfully!")
            print("Order ID:", order.get("orderId"))
            print("Status:", order.get("status"))
        except Exception as e:
            print("\nERROR:", e)
        cont = input("\nPlace another order? (y/n): ").lower()
        if cont != "y":
            break

if __name__ == "__main__":
    main()
