import os
import sys
import json
from typing import Optional, Dict

from flask import Flask, render_template, request, jsonify

# Ensure we can import existing bot modules from src/
CURRENT_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
ADV_DIR = os.path.abspath(os.path.join(SRC_DIR, "advanced"))
sys.path.insert(0, SRC_DIR)
sys.path.insert(0, ADV_DIR)

from market_orders import BasicBot as MarketBot  # type: ignore
from limit_orders import BasicBot as LimitBot  # type: ignore
try:
    from oco import AdvancedBot as AdvancedBot  # type: ignore
except Exception:
    AdvancedBot = None  # Advanced bot optional
try:
    from twap import TWAPBot as TWAPBot  # type: ignore
except Exception:
    TWAPBot = None

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


def _safe_json(obj: Dict) -> Dict:
    try:
        json.dumps(obj)
        return obj
    except Exception:
        return {"message": "Non-serializable response", "repr": repr(obj)}


@app.route("/place_order", methods=["POST"])
def place_order():
    data = request.form
    api_key = data.get("api_key", "").strip()
    api_secret = data.get("api_secret", "").strip()
    symbol = data.get("symbol", "").upper().strip()
    side = data.get("side", "BUY").upper().strip()
    order_type = data.get("order_type", "MARKET").upper().strip()

    if not api_key or not api_secret:
        return jsonify({"ok": False, "error": "API credentials are required"}), 400
    if not symbol or side not in ("BUY", "SELL"):
        return jsonify({"ok": False, "error": "Invalid symbol or side"}), 400

    try:
        if order_type == "MARKET":
            quantity = float(data.get("quantity", "0"))
            bot = MarketBot(api_key, api_secret, testnet=True)
            resp = bot.place_market_order(symbol, side, quantity)
            return jsonify({"ok": True, "response": _safe_json(resp or {})})

        elif order_type == "LIMIT":
            quantity = float(data.get("quantity", "0"))
            price = float(data.get("price", "0"))
            bot = LimitBot(api_key, api_secret, testnet=True)
            resp = bot.place_limit_order(symbol, side, quantity, price)
            return jsonify({"ok": True, "response": _safe_json(resp or {})})

        elif order_type == "STOP_LIMIT":
            if AdvancedBot is None:
                return jsonify({"ok": False, "error": "Advanced order module not available"}), 400
            quantity = float(data.get("quantity", "0"))
            stop_price = float(data.get("stop_price", "0"))
            limit_price = float(data.get("limit_price", "0"))
            bot = AdvancedBot(api_key, api_secret, testnet=True)
            resp = bot.place_stop_limit_order(symbol, side, quantity, stop_price, limit_price)
            return jsonify({"ok": True, "response": _safe_json(resp or {})})

        elif order_type == "OCO":
            if AdvancedBot is None:
                return jsonify({"ok": False, "error": "Advanced order module not available"}), 400
            quantity = float(data.get("quantity", "0"))
            take_profit_price = float(data.get("take_profit_price", "0"))
            stop_price = float(data.get("stop_price", "0"))
            stop_limit_price = float(data.get("stop_limit_price", "0"))
            bot = AdvancedBot(api_key, api_secret, testnet=True)
            resp = bot.place_oco_order(symbol, side, quantity, take_profit_price, stop_price, stop_limit_price)
            return jsonify({"ok": True, "response": _safe_json(resp or {})})

        elif order_type == "TWAP":
            if TWAPBot is None:
                return jsonify({"ok": False, "error": "TWAP module not available"}), 400
            total_qty = float(data.get("total_qty", "0"))
            splits = int(data.get("splits", "1"))
            interval_sec = int(data.get("interval_sec", "1"))
            bot = TWAPBot(api_key, api_secret, testnet=True)
            resp = bot.place_twap_orders(symbol, side, total_qty, splits, interval_sec)
            return jsonify({"ok": True, "response": _safe_json({"orders": resp or []})})

        else:
            return jsonify({"ok": False, "error": f"Unsupported order type: {order_type}"}), 400

    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/logs")
def logs():
    log_path = os.path.abspath(os.path.join(SRC_DIR, "..", "bot.log"))
    if not os.path.exists(log_path):
        return jsonify({"lines": ["bot.log not found"]})
    try:
        with open(log_path, "r") as f:
            lines = f.readlines()[-50:]
        return jsonify({"lines": [l.rstrip("\n") for l in lines]})
    except Exception as e:
        return jsonify({"lines": [f"Failed to read log: {e}"]})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

