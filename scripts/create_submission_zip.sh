#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR=$(dirname "$0")/..
cd "$ROOT_DIR"

ZIP_NAME="${USER:-candidate}_binance_bot.zip"
echo "Creating $ZIP_NAME from project root $ROOT_DIR"

zip -r "$ZIP_NAME" README.md src requirements.txt report.md bot.log
echo "Created $ZIP_NAME"
