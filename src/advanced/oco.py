"""
OCO and Stop-Limit Order Logic (Bonus)
"""
import logging
from ..logging_config import setup_logging
from binance import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException

setup_logging()

class AdvancedBot:
    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        self.client = Client(api_key, api_secret)
        if testnet:
            self.client.FUTURES_URL = "https://testnet.binancefuture.com"
        logging.info("AdvancedBot initialized | Testnet=%s", testnet)

    def validate_stop_limit_order(self, symbol, side, quantity, price, stop_price):
        if not symbol:
            raise ValueError("Symbol cannot be empty")
        if side not in ["BUY", "SELL"]:
            raise ValueError("Side must be BUY or SELL")
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        if price is None or price <= 0:
            raise ValueError("Limit price must be greater than 0")
        if stop_price is None or stop_price <= 0:
            raise ValueError("Stop price must be greater than 0")

    def place_stop_limit_order(self, symbol, side, quantity, price, stop_price):
        self.validate_stop_limit_order(symbol, side, quantity, price, stop_price)
        try:
            logging.info("Placing STOP-LIMIT order | %s %s qty=%s price=%s stop_price=%s", symbol, side, quantity, price, stop_price)
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type=Client.ORDER_TYPE_STOP,
                quantity=quantity,
                price=price,
                stopPrice=stop_price,
                timeInForce=Client.TIME_IN_FORCE_GTC
            )
            logging.info("Stop-Limit Order success | Response=%s", order)
            return order
        except (BinanceAPIException, BinanceOrderException) as e:
            logging.error("Stop-Limit Order failed | %s", e)
            raise

    def validate_oco_order(self, symbol, side, quantity, price, stop_price, stop_limit_price):
        if not symbol:
            raise ValueError("Symbol cannot be empty")
        if side not in ["BUY", "SELL"]:
            raise ValueError("Side must be BUY or SELL")
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        if price is None or price <= 0:
            raise ValueError("Take profit price must be greater than 0")
        if stop_price is None or stop_price <= 0:
            raise ValueError("Stop price must be greater than 0")
        if stop_limit_price is None or stop_limit_price <= 0:
            raise ValueError("Stop-limit price must be greater than 0")

    def place_oco_order(self, symbol, side, quantity, price, stop_price, stop_limit_price):
        self.validate_oco_order(symbol, side, quantity, price, stop_price, stop_limit_price)
        try:
            logging.info("Placing OCO order | %s %s qty=%s price=%s stop_price=%s stop_limit_price=%s", symbol, side, quantity, price, stop_price, stop_limit_price)
            # Binance Futures API does not natively support OCO, so we simulate by placing two orders
            take_profit_order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type=Client.ORDER_TYPE_LIMIT,
                quantity=quantity,
                price=price,
                timeInForce=Client.TIME_IN_FORCE_GTC
            )
            stop_limit_order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type=Client.ORDER_TYPE_STOP,
                quantity=quantity,
                price=stop_limit_price,
                stopPrice=stop_price,
                timeInForce=Client.TIME_IN_FORCE_GTC
            )
            logging.info("OCO Orders placed | TP=%s | SL=%s", take_profit_order, stop_limit_order)
            return {"take_profit_order": take_profit_order, "stop_limit_order": stop_limit_order}
        except (BinanceAPIException, BinanceOrderException) as e:
            logging.error("OCO Order failed | %s", e)
            raise

def main():
    print("\n=== Binance Futures Testnet ADVANCED Orders ===\n")
    API_KEY = input("Enter API Key: ").strip()
    API_SECRET = input("Enter API Secret: ").strip()
    bot = AdvancedBot(API_KEY, API_SECRET, testnet=True)
    while True:
        print("\nChoose order type:")
        print("1. Stop-Limit Order")
        print("2. OCO Order")
        choice = input("Enter choice (1/2): ").strip()
        try:
            symbol = input("Symbol (e.g., BTCUSDT): ").upper().strip()
            side = input("Side (BUY/SELL): ").upper().strip()
            quantity = float(input("Quantity: "))
            if choice == "1":
                price = float(input("Limit Price: "))
                stop_price = float(input("Stop Price: "))
                order = bot.place_stop_limit_order(symbol, side, quantity, price, stop_price)
                print("\nStop-Limit Order Placed Successfully!")
                print("Order ID:", order["orderId"])
                print("Status:", order["status"])
            elif choice == "2":
                price = float(input("Take Profit Price: "))
                stop_price = float(input("Stop Price: "))
                stop_limit_price = float(input("Stop-Limit Price: "))
                orders = bot.place_oco_order(symbol, side, quantity, price, stop_price, stop_limit_price)
                print("\nOCO Orders Placed Successfully!")
                print("Take Profit Order ID:", orders["take_profit_order"]["orderId"])
                print("Stop-Limit Order ID:", orders["stop_limit_order"]["orderId"])
            else:
                print("Invalid choice.")
        except Exception as e:
            print("\nERROR:", e)
        cont = input("\nPlace another advanced order? (y/n): ").lower()
        if cont != "y":
            break

if __name__ == "__main__":
    main()