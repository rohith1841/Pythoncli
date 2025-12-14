import logging
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
LOG_PATH = os.path.join(PROJECT_ROOT, "bot.log")


def setup_logging():
    """Configure project-wide logging to a single bot.log in project root."""
    logger = logging.getLogger()
    if not logger.handlers:
        logging.basicConfig(
            filename=LOG_PATH,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
