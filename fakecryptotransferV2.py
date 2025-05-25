#!/usr/bin/env python3
import os
import random
import json
from datetime import datetime, timedelta
from faker import Faker
import qrcode
from io import BytesIO
import base64
import hashlib
import time
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
    CallbackQueryHandler
)

# Enhanced Configuration
CONFIG_FILE = "crypto_prank_pro_config.json"
OUTPUT_FOLDER = "prank_receipts"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
fake = Faker()

# Enhanced Crypto Data with more details
CRYPTO_DATA = {
    "btc": {
        "name": "Bitcoin",
        "symbol": "BTC",
        "color": "#f7931a",
        "icon": "data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPCFET0NUWVBFIHN2ZyBQVUJMSUMgIi0vL1czQy8vRFREIFNWRyAxLjEvL0VOIiAiaHR0cDovL3d3dy53My5vcmcvR3JhcGhpY3MvU1ZHLzEuMS9EVEQvc3ZnMTEuZHRkIj4KPCEtLSBDcmVhdG9yOiBDb3JlbERSQVcgMjAxOSAoNjQtQml0KSAtLT4KPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbDpzcGFjZT0icHJlc2VydmUiIHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIHZlcnNpb249IjEuMSIgc2hhcGUtcmVuZGVyaW5nPSJnZW9tZXRyaWNQcmVjaXNpb24iIHRleHQtcmVuZGVyaW5nPSJnZW9tZXRyaWNQcmVjaXNpb24iIGltYWdlLXJlbmRlcmluZz0ib3B0aW1pemVRdWFsaXR5IiBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGNsaXAtcnVsZT0iZXZlbm9kZCIKdmlld0JveD0iMCAwIDQwOTEuMjcgNDA5MS43MyIKIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIgogeG1sbnM6eG9kbT0iaHR0cDovL3d3dy5jb3JlbC5jb20vY29yZWxkcmF3L29kbS8yMDAzIj4KIDxnIGlkPSJMYXllcl94MDAyMF8xIj4KICA8bWV0YWRhdGEgaWQ9IkNvcmVsQ29ycElEXzBDb3JlbC1MYXllciIvPgogIDxnIGlkPSJfMTQyMTM0NDAyMzMyOCI+CiAgIDxwYXRoIGZpbGw9IiNGNzkzMUEiIGZpbGwtcnVsZT0ibm9uemVybyIgZD0iTTQwMzAuMDYgMjU0MC43N2MtMjczLjI0LDEwOTYuMDEgLTEzODMuMzIsMTc2My4wMiAtMjQ3OS40NiwxNDg5LjcxIC0xMDk1LjY4LC0yNzMuMjQgLTE3NjIuNjksLTEzODMuMzkgLTE0ODkuMzMsLTI0NzkuMzEgMjczLjEyLC0xMDk2LjEzIDEzODMuMiwtMTc2My4xOSAyNDc5LC0xNDg5Ljk1IDEwOTYuMDYsMjczLjI0IDE3NjMuMDMsMTM4My41MSAxNDg5Ljc2LDI0NzkuNTdsMC4wMiAtMC4wMnoiLz4KICAgPHBhdGggZmlsbD0id2hpdGUiIGZpbGwtcnVsZT0ibm9uemVybyIgZD0iTTI5NDcuNzcgMTc1NC4zOGM0MC43MiwtMjcyLjI2IC0xNjYuNTYsLTQxOC42MSAtNDUwLC01MTYuMjRsOTEuOTUgLTM2OC44IC0yMjQuNSAtNTUuOTQgLTg5LjUxIDM1OS4wOWMtNTkuMDIsLTE0LjcyIC0xMTkuNjMsLTI4LjU5IC0xNzkuODcsLTQyLjM0bDkwLjE2IC0zNjEuNDYgLTIyNC4zNiAtNTUuOTQgLTkyIDM2OC42OGMtNDguODQsLTExLjEyIC05Ni44MSwtMjIuMTEgLTE0My4zNSwtMzMuNjlsMC4yNiAtMS4xNiAtMzA5LjU5IC03Ny4zMSAtNTkuNzIgMjM5Ljc4YzAsMCAxNjYuNTYsMzguMTggMTYzLjA1LDQwLjUzIDkwLjkxLDIyLjY5IDEwNy4zNSw4Mi44NyAxMDQuNjIsMTMwLjU3bC0xMDQuNzQgNDIwLjE1YzYuMjYsMS41OSAxNC4zOCwzLjg5IDIzLjM0LDcuNDkgLTcuNDksLTEuODYgLTE1LjQ2LC0zLjg5IC0yMy43MywtNS44N2wtMTQ2LjgxIDU4OC41N2MtMTEuMTEsMjcuNjIgLTM5LjMxLDY5LjA3IC0xMDIuODcsNTMuMzMgMi4yNSwzLjI2IC0xNjMuMTcsLTQwLjcyIC0xNjMuMTcsLTQwLjcybC0xMTEuNDYgMjU2Ljk4IDI5Mi4xNSA3Mi44M2M1NC4zNSwxMy42MyAxMDcuNjEsMjcuODkgMTYwLjA2LDQxLjNsLTkyLjkgMzczLjAzIDIyNC4yNCA1NS45NCA5MiAtMzY5LjA3YzYxLjI2LDE2LjYzIDEyMC43MSwzMS45NyAxNzguOTEsNDYuNDNsLTkxLjY5IDM2Ny4zMyAyMjQuNTEgNTUuOTQgOTIuODkgLTM3Mi4zM2MzODIuODIsNzIuNDUgNjcwLjY3LDQzLjI0IDc5MS44MywtMzAzLjAyIDk3LjYzLC0yNzguNzggLTQuODYsLTQzOS41OCAtMjA2LjI2LC01NDQuNDQgMTQ2LjY5LC0zMy44MyAyNTcuMTgsLTEzMC4zMSAyODYuNjQsLTMyOS42MWwtMC4wNyAtMC4wNXptLTUxMi45MyA3MTkuMjZjLTY5LjM4LDI3OC43OCAtNTM4Ljc2LDEyOC4wOCAtNjkwLjk0LDkwLjI5bDEyMy4yOCAtNDk0LjJjMTUyLjE3LDM3Ljk5IDY0MC4xNywxMTMuMTcgNTY3LjY3LDQwMy45MXptNjkuNDMgLTcyMy4zYy02My4yOSwyNTMuNTggLTQ1My45NiwxMjQuNzUgLTU4MC42OSw5My4xNmwxMTEuNzcgLTQ0OC4yMWMxMjYuNzMsMzEuNTkgNTM0Ljg1LDkwLjU1IDQ2OC45NCwzNTUuMDVsLTAuMDIgMHoiLz4KICA8L2c+CiA8L2c+Cjwvc3ZnPgo=",
        "explorer_url": "https://blockstream.info/tx/",
        "address_prefix": ["1", "3", "bc1"],
        "min_amount": 0.00001,
        "max_amount": 100,
        "decimals": 8
    },
    "eth": {
        "name": "Ethereum",
        "symbol": "ETH",
        "color": "#627eea",
        "icon": "data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz4KPCFET0NUWVBFIHN2ZyBQVUJMSUMgIi0vL1czQy8vRFREIFNWRyAxLjEvL0VOIiAiaHR0cDovL3d3dy53My5vcmcvR3JhcGhpY3MvU1ZHLzEuMS9EVEQvc3ZnMTEuZHRkIj4KPCEtLSBDcmVhdG9yOiBDb3JlbERSQVcgMjAxOSAoNjQtQml0KSAtLT4KPHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbDpzcGFjZT0icHJlc2VydmUiIHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIHZlcnNpb249IjEuMSIgc2hhcGUtcmVuZGVyaW5nPSJnZW9tZXRyaWNQcmVjaXNpb24iIHRleHQtcmVuZGVyaW5nPSJnZW9tZXRyaWNQcmVjaXNpb24iIGltYWdlLXJlbmRlcmluZz0ib3B0aW1pemVRdWFsaXR5IiBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGNsaXAtcnVsZT0iZXZlbm9kZCIKdmlld0JveD0iMCAwIDc4NC4zNyAxMjc3LjM5IgogeG1sbnM6eGxpbms9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkveGxpbmsiCiB4bWxuczp4b2RtPSJodHRwOi8vd3d3LmNvcmVsLmNvbS9jb3JlbGRyYXcvb2RtLzIwMDMiPgogPGcgaWQ9IkxheWVyX3gwMDIwXzEiPgogIDxtZXRhZGF0YSBpZD0iQ29yZWxDb3JwSURfMENvcmVsLUxheWVyIi8+CiAgPGcgaWQ9Il8xNDIxMzk0MzQyNDAwIj4KICAgPGc+CiAgICA8cG9seWdvbiBmaWxsPSIjMzQzNDM0IiBmaWxsLXJ1bGU9Im5vbnplcm8iIHBvaW50cz0iMzkyLjA3LDAgMzgzLjUsMjkuMTEgMzgzLjUsODczLjc0IDM5Mi4wNyw4ODIuMjkgNzg0LjEzLDY1MC41NCAiLz4KICAgIDxwb2x5Z29uIGZpbGw9IiM4QzhDOEMiIGZpbGwtcnVsZT0ibm9uemVybyIgcG9pbnRzPSIzOTIuMDcsMCAtMCw2NTAuNTQgMzkyLjA3LDg4Mi4yOSAzOTIuMDcsNDcyLjMzICIvPgogICAgPHBvbHlnb24gZmlsbD0iIzNDM0MzQiIgZmlsbC1ydWxlPSJub256ZXJvIiBwb2ludHM9IjM5Mi4wNyw5NTYuNTIgMzg3LjI0LDk2Mi40MSAzODcuMjQsMTI2My4yOCAzOTIuMDcsMTI3Ny4zOCA3ODQuMzcsNzI0Ljg5ICIvPgogICAgPHBvbHlnb24gZmlsbD0iIzhDOEM4QyIgZmlsbC1ydWxlPSJub256ZXJvIiBwb2ludHM9IjM5Mi4wNywxMjc3LjM4IDM5Mi4wNyw5NTYuNTIgLTAsNzI0Ljg5ICIvPgogICAgPHBvbHlnb24gZmlsbD0iIzE0MTQxNCIgZmlsbC1ydWxlPSJub256ZXJvIiBwb2ludHM9IjM5Mi4wNyw4ODIuMjkgNzg0LjEzLDY1MC41NCAzOTIuMDcsNDcyLjMzICIvPgogICAgPHBvbHlnb24gZmlsbD0iIzM5MzkzOSIgZmlsbC1ydWxlPSJub256ZXJvIiBwb2ludHM9IjAsNjUwLjU0IDM5Mi4wNyw4ODIuMjkgMzkyLjA3LDQ3Mi4zMyAiLz4KICAgPC9nPgogIDwvZz4KIDwvZz4KPC9zdmc+Cg==",
        "explorer_url": "https://etherscan.io/tx/0x",
        "address_prefix": "0x",
        "min_amount": 0.001,
        "max_amount": 1000,
        "decimals": 18
    },
    "usdt": {
        "name": "Tether (ERC20)",
        "symbol": "USDT",
        "color": "#26a17b",
        "icon": "data:image/svg+xml;base64,PHN2ZyBpZD0iTGF5ZXJfMSIgZGF0YS1uYW1lPSJMYXllciAxIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAzMzkuNDMgMjk1LjI3Ij48dGl0bGU+dGV0aGVyLXVzZHQtbG9nbzwvdGl0bGU+PHBhdGggZD0iTTYyLjE1LDEuNDVsLTYxLjg5LDEzMGEyLjUyLDIuNTIsMCwwLDAsLjU0LDIuOTRMMTY3Ljk1LDI5NC41NmEyLjU1LDIuNTUsMCwwLDAsMy41MywwTDMzOC42MywxMzQuNGEyLjUyLDIuNTIsMCwwLDAsLjU0LTIuOTRsLTYxLjg5LTEzMEEyLjUsMi41LDAsMCwwLDI3NSwwSDY0LjQ1YTIuNSwyLjUsMCwwLDAtMi4zLDEuNDVoMFoiIHN0eWxlPSJmaWxsOiM1MGFmOTU7ZmlsbC1ydWxlOmV2ZW5vZGQiLz48cGF0aCBkPSJNMTkxLjE5LDE0NC44djBjLTEuMi4wOS03LjQsMC40Ni0yMS4yMywwLjQ2LTExLDAtMTguODEtLjMzLTIxLjU1LTAuNDZ2MGMtNDIuNTEtMS44Ny03NC4yNC05LjI3LTc0LjI0LTE4LjEzczMxLjczLTE2LjI1LDc0LjI0LTE4LjE1djI4LjkxYzIuNzgsMC4yLDEwLjc0LjY3LDIxLjc0LDAuNjcsMTMuMiwwLDE5LjgxLS41NSwyMS0wLjY2di0yOC45YzQyLjQyLDEuODksNzQuMDgsOS4yOSw3NC4wOCwxOC4xM3MtMzEuNjUsMTYuMjQtNzQuMDgsMTguMTJoMFptMC0zOS4yNVY3OS42OGg1OS4yVjQwLjIzSDg5LjIxVjc5LjY4SDE0OC40djI1Ljg2Yy00OC4xMSwyLjIxLTg0LjI5LDExLjc0LTg0LjI5LDIzLjE2czM2LjE4LDIwLjk0LDg0LjI5LDIzLjE2djgyLjloNDIuNzhWMTUxLjgzYzQ4LTIuMjEsODQuMTItMTEuNzMsODQuMTItMjMuMTRzLTM2LjA5LTIwLjkzLTg0LjEyLTIzLjE1aDBabTAsMGgwWiIgc3R5bGU9ImZpbGw6I2ZmZjtmaWxsLXJ1bGU6ZXZlbm9kZCIvPjwvc3ZnPg==",
        "explorer_url": "https://etherscan.io/tx/0x",
        "address_prefix": "0x",
        "min_amount": 10,
        "max_amount": 100000,
        "decimals": 6
    },
    "doge": {
        "name": "Dogecoin",
        "symbol": "DOGE",
        "color": "#c2a633",
        "icon": "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyMDAwIDIwMDAiIHdpZHRoPSIyNTAwIiBoZWlnaHQ9IjI1MDAiPjxnIGZpbGw9IiNjMmE2MzMiPjxwYXRoIGQ9Ik0xMDI0IDY1OUg4ODEuMTJ2MjgxLjY5aDIyNC43OXYxMTcuOTRIODgxLjEydjI4MS42N0gxMDMxYzM4LjUxIDAgMzE2LjE2IDQuMzUgMzE1LjczLTMyNy43MlMxMDc3LjQ0IDY1OSAxMDI0IDY1OXoiLz48cGF0aCBkPSJNMTAwMCAwQzQ0Ny43MSAwIDAgNDQ3LjcxIDAgMTAwMHM0NDcuNzEgMTAwMCAxMDAwIDEwMDAgMTAwMC00NDcuNzEgMTAwMC0xMDAwUzE1NTIuMjkgMCAxMDAwIDB6bTM5LjI5IDE1NDAuMUg2NzcuMTR2LTQ4MS40Nkg1NDkuNDhWOTQwLjdoMTI3LjY1VjQ1OS4yMWgzMTAuODJjNzMuNTMgMCA1NjAuNTYtMTUuMjcgNTYwLjU2IDU0OS40OCAwIDU3NC4wOS01MDkuMjEgNTMxLjQxLTUwOS4yMSA1MzEuNDF6Ii8+PC9nPjwvc3ZnPg==",
        "explorer_url": "https://dogechain.info/tx/",
        "address_prefix": "D",
        "min_amount": 10,
        "max_amount": 1000000,
        "decimals": 8
    },
    "xmr": {
        "name": "Monero",
        "symbol": "XMR",
        "color": "#f26822",
        "icon": "data:image/svg+xml;base64,PHN2ZyBpZD0iTGF5ZXJfMSIgZGF0YS1uYW1lPSJMYXllciAxIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAzNzU2LjA5IDM3NTYuNDkiPjx0aXRsZT5tb25lcm88L3RpdGxlPjxwYXRoIGQ9Ik00MTI4LDIyNDkuODFDNDEyOCwzMjg3LDMyODcuMjYsNDEyNy44NiwyMjUwLDQxMjcuODZTMzcyLDMyODcsMzcyLDIyNDkuODEsMTIxMi43NiwzNzEuNzUsMjI1MCwzNzEuNzUsNDEyOCwxMjEyLjU0LDQxMjgsMjI0OS44MVoiIHRyYW5zZm9ybT0idHJhbnNsYXRlKC0zNzEuOTYgLTM3MS43NSkiIHN0eWxlPSJmaWxsOiNmZmYiLz48cGF0aCBpZD0iXzE0OTkzMTAzMiIgZGF0YS1uYW1lPSIgMTQ5OTMxMDMyIiBkPSJNMjI1MCwzNzEuNzVjLTEwMzYuODksMC0xODc5LjEyLDg0Mi4wNi0xODc3LjgsMTg3OCwwLjI2LDIwNy4yNiwzMy4zMSw0MDYuNjMsOTUuMzQsNTkzLjEyaDU2MS44OFYxMjYzTDIyNTAsMjQ4My41NywzNDcwLjUyLDEyNjN2MTU3OS45aDU2MmM2Mi4xMi0xODYuNDgsOTUtMzg1Ljg1LDk1LjM3LTU5My4xMkM0MTI5LjY2LDEyMTIuNzYsMzI4NywzNzIsMjI1MCwzNzJaIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgtMzcxLjk2IC0zNzEuNzUpIiBzdHlsZT0iZmlsbDojZjI2ODIyIi8+PHBhdGggaWQ9Il8xNDk5MzExNjAiIGRhdGEtbmFtZT0iIDE0OTkzMTE2MCIgZD0iTTE5NjkuMywyNzY0LjE3bC01MzIuNjctNTMyLjd2OTk0LjE0SDEwMjkuMzhsLTM4NC4yOS4wN2MzMjkuNjMsNTQwLjgsOTI1LjM1LDkwMi41NiwxNjA0LjkxLDkwMi41NlMzNTI1LjMxLDM3NjYuNCwzODU1LDMyMjUuNkgzMDYzLjI1VjIyMzEuNDdsLTUzMi43LDUzMi43LTI4MC42MSwyODAuNjEtMjgwLjYyLTI4MC42MWgwWiIgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoLTM3MS45NiAtMzcxLjc1KSIgc3R5bGU9ImZpbGw6IzRkNGQ0ZCIvPjwvc3ZnPg==",
        "explorer_url": "https://xmrchain.net/tx/",
        "address_prefix": "4",
        "min_amount": 0.01,
        "max_amount": 1000,
        "decimals": 12
    }
}

# Enhanced Transaction HTML Template with blockchain explorer link
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>{crypto_name} Transaction Receipt</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        :root {{
            --primary-color: {color};
            --secondary-color: {secondary_color};
        }}
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        body {{
            font-family: 'SF Pro Text', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background-color: #f8fafc;
            color: #1e293b;
            line-height: 1.5;
            padding: 20px;
        }}
        .receipt-container {{
            max-width: 480px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 10px 25px -5px rgba(0,0,0,0.1), 0 10px 10px -5px rgba(0,0,0,0.04);
            overflow: hidden;
            border: 1px solid #e2e8f0;
        }}
        .header {{
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 24px;
            text-align: center;
            position: relative;
        }}
        .crypto-icon {{
            width: 64px;
            height: 64px;
            margin: 0 auto 12px;
            display: block;
            filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1));
        }}
        .status-badge {{
            position: absolute;
            top: 20px;
            right: 20px;
            background: rgba(255,255,255,0.2);
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .tx-id {{
            background: #f1f5f9;
            padding: 16px;
            margin: 0;
            font-family: 'SF Mono', Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace;
            word-break: break-all;
            font-size: 14px;
            border-bottom: 1px solid #e2e8f0;
            display: flex;
            align-items: center;
        }}
        .tx-id a {{
            color: #3b82f6;
            text-decoration: none;
            margin-left: 8px;
        }}
        .tx-id a:hover {{
            text-decoration: underline;
        }}
        .details {{
            padding: 24px;
        }}
        .amount {{
            font-size: 32px;
            font-weight: 700;
            color: var(--primary-color);
            text-align: center;
            margin: 16px 0 24px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .amount small {{
            font-size: 16px;
            color: #64748b;
            margin-left: 8px;
            font-weight: 500;
        }}
        .detail-row {{
            display: flex;
            margin-bottom: 16px;
            align-items: flex-start;
        }}
        .label {{
            font-weight: 600;
            width: 120px;
            color: #64748b;
            font-size: 14px;
        }}
        .value {{
            flex: 1;
            font-family: 'SF Mono', Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace;
            word-break: break-all;
            font-size: 14px;
        }}
        .fiat-value {{
            text-align: center;
            color: #64748b;
            font-size: 14px;
            margin-bottom: 24px;
        }}
        .qr-code {{
            width: 180px;
            height: 180px;
            margin: 24px auto;
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 12px;
        }}
        .qr-code img {{
            width: 100%;
            height: 100%;
            object-fit: contain;
        }}
        .ref-id {{
            background: #f1f5f9;
            padding: 12px;
            border-radius: 8px;
            font-family: 'SF Mono', Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace;
            text-align: center;
            margin: 16px 0;
            font-size: 14px;
        }}
        .memo {{
            background: #f8fafc;
            padding: 12px;
            border-radius: 8px;
            border-left: 4px solid var(--primary-color);
            margin: 16px 0;
            font-size: 14px;
        }}
        .memo strong {{
            color: var(--primary-color);
        }}
        .footer {{
            background: #f1f5f9;
            padding: 16px;
            text-align: center;
            font-size: 12px;
            color: #64748b;
            border-top: 1px solid #e2e8f0;
        }}
        .progress-bar {{
            height: 6px;
            background: #e2e8f0;
            border-radius: 3px;
            margin: 16px 0;
            overflow: hidden;
        }}
        .progress {{
            height: 100%;
            background: var(--primary-color);
            width: {confirmations}%;
            transition: width 0.3s ease;
        }}
        .confirmations {{
            display: flex;
            justify-content: space-between;
            font-size: 12px;
            color: #64748b;
            margin-bottom: 8px;
        }}
        .network-info {{
            display: flex;
            justify-content: space-between;
            font-size: 12px;
            color: #64748b;
            margin-top: 8px;
        }}
        .badge {{
            display: inline-block;
            padding: 4px 8px;
            background: #e2e8f0;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 600;
            color: #475569;
            margin-left: 8px;
        }}
        .timestamp {{
            color: #64748b;
            font-size: 12px;
            margin-top: 4px;
        }}
    </style>
</head>
<body>
    <div class="receipt-container">
        <div class="header">
            <img src="{crypto_icon}" class="crypto-icon" alt="{crypto_name}">
            <h2>{crypto_name} Transaction</h2>
            <div class="status-badge">{status}</div>
        </div>
        
        <p class="tx-id">
            {tx_id_short}
            <a href="{explorer_url}{tx_id}" target="_blank" title="View on blockchain explorer">🔗</a>
        </p>
        
        <div class="details">
            <div class="amount">
                {amount} <small>{crypto_symbol}</small>
            </div>
            
            <div class="fiat-value">≈ {fiat_value} USD</div>
            
            <div class="confirmations">
                <span>Confirmations</span>
                <span>{confirmations_text}</span>
            </div>
            <div class="progress-bar">
                <div class="progress"></div>
            </div>
            
            <div class="ref-id">Reference ID: {ref_id}</div>
            
            <div class="detail-row">
                <div class="label">Status:</div>
                <div class="value">{status} <span class="badge">{network}</span></div>
            </div>
            <div class="detail-row">
                <div class="label">Date:</div>
                <div class="value">{timestamp}<div class="timestamp">{timestamp_relative}</div></div>
            </div>
            <div class="detail-row">
                <div class="label">From:</div>
                <div class="value">{sender}</div>
            </div>
            <div class="detail-row">
                <div class="label">To:</div>
                <div class="value">{receiver}</div>
            </div>
            <div class="detail-row">
                <div class="label">Network Fee:</div>
                <div class="value">{fee} {crypto_symbol} <small>(≈ {fee_fiat} USD)</small></div>
            </div>
            
            {memo_html}
            
            <div class="qr-code">
                <img src="data:image/png;base64,{qr_code}" alt="QR Code">
            </div>
            
            <div class="network-info">
                <span>Block Height: {block_height}</span>
                <span>Size: {tx_size} bytes</span>
            </div>
        </div>
        
        <div class="footer">
            This transaction receipt is generated for demonstration purposes only
        </div>
    </div>
</body>
</html>
"""

def init_config():
    if not os.path.exists(CONFIG_FILE):
        config = {
            "telegram_token": "",
            "chat_id": "",
            "last_ref_id": 100000,
            "exchange_rates": {
                "btc": 50000,
                "eth": 3000,
                "usdt": 1,
                "doge": 0.15,
                "xmr": 200
            },
            "network_fees": {
                "btc": 0.0005,
                "eth": 0.01,
                "usdt": 0.01,
                "doge": 2.0,
                "xmr": 0.01
            },
            "networks": {
                "btc": "Bitcoin Mainnet",
                "eth": "Ethereum Mainnet",
                "usdt": "ERC20",
                "doge": "Dogecoin Mainnet",
                "xmr": "Monero Mainnet"
            }
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)
        return config
    with open(CONFIG_FILE) as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def generate_tx_id(crypto):
    """Generate a realistic transaction ID"""
    if crypto == "btc":
        return hashlib.sha256(str(random.getrandbits(256)).encode()).hexdigest()
    elif crypto == "eth":
        return "0x" + hashlib.sha256(str(random.getrandbits(256)).encode()).hexdigest()[:64]
    elif crypto == "xmr":
        return hashlib.sha256(str(random.getrandbits(256)).encode()).hexdigest()[:64]
    else:
        return hashlib.md5(str(random.getrandbits(128)).encode()).hexdigest()

def generate_qr(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def generate_fake_address(crypto):
    """Generate realistic-looking crypto addresses"""
    if crypto == "btc":
        prefixes = CRYPTO_DATA[crypto]["address_prefix"]
        prefix = random.choice(prefixes)
        return prefix + hashlib.sha256(str(random.getrandbits(256)).encode()).hexdigest()[:33]
    elif crypto in ["eth", "usdt"]:
        return "0x" + hashlib.sha256(str(random.getrandbits(256)).encode()).hexdigest()[:40]
    elif crypto == "doge":
        return "D" + hashlib.sha256(str(random.getrandbits(256)).encode()).hexdigest()[:33]
    elif crypto == "xmr":
        return "4" + hashlib.sha256(str(random.getrandbits(256)).encode()).hexdigest()[:95]

def generate_receipt(crypto, sender, receiver, amount, fee, ref_id, memo=""):
    crypto_data = CRYPTO_DATA[crypto]
    config = init_config()
    
    # Generate realistic transaction data
    tx_id = generate_tx_id(crypto)
    tx_id_short = tx_id[:12] + "..." + tx_id[-12:]
    qr_code = generate_qr(f"{crypto_data['symbol']}:{receiver}?amount={amount}&memo={memo}")
    
    # Calculate fiat values
    exchange_rate = config["exchange_rates"][crypto]
    fiat_value = round(amount * exchange_rate, 2)
    fee_fiat = round(fee * exchange_rate, 2)
    
    # Generate timestamps
    tx_time = datetime.now()
    timestamp = tx_time.strftime("%Y-%m-%d %H:%M:%S UTC")
    timestamp_relative = "just now"
    
    # Generate confirmation data
    confirmations = random.randint(6, 50) if crypto == "btc" else random.randint(15, 100)
    confirmations_text = f"{confirmations}/6" if crypto == "btc" else f"{confirmations}/12"
    confirmations_percent = min(100, (confirmations / (6 if crypto == "btc" else 12)) * 100)
    
    # Generate block data
    block_height = random.randint(700000, 800000) if crypto == "btc" else random.randint(15000000, 16000000)
    tx_size = random.randint(250, 500)
    
    # Status (make it look like it's processing)
    status = random.choice(["Confirmed", "Completed", "Success"])
    
    memo_html = f'<div class="memo"><strong>Memo:</strong> {memo}</div>' if memo else ""
    
    # Generate secondary color (darker version of primary)
    primary_color = crypto_data["color"]
    secondary_color = f"hsl({int(primary_color[1:3], 16)}, {int(primary_color[5:7], 16)}%, 40%)"
    
    html = HTML_TEMPLATE.format(
        crypto_name=crypto_data["name"],
        crypto_symbol=crypto_data["symbol"],
        color=crypto_data["color"],
        secondary_color=secondary_color,
        crypto_icon=crypto_data["icon"],
        tx_id=tx_id,
        tx_id_short=tx_id_short,
        explorer_url=crypto_data["explorer_url"],
        sender=sender,
        receiver=receiver,
        amount=round(amount, crypto_data["decimals"]),
        fee=round(fee, crypto_data["decimals"]),
        timestamp=timestamp,
        timestamp_relative=timestamp_relative,
        ref_id=ref_id,
        qr_code=qr_code,
        memo_html=memo_html,
        fiat_value=fiat_value,
        fee_fiat=fee_fiat,
        confirmations=confirmations_percent,
        confirmations_text=confirmations_text,
        status=status,
        network=config["networks"][crypto],
        block_height=block_height,
        tx_size=tx_size
    )
    
    filename = f"{OUTPUT_FOLDER}/{crypto}_tx_{ref_id}_{int(time.time())}.html"
    with open(filename, "w") as f:
        f.write(html)
    
    return filename

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
💰 *Crypto Transfer Pro* 💰
_The most realistic crypto transaction generator_

🔹 Generate convincing crypto receipts
🔹 Supports multiple cryptocurrencies
🔹 Complete with QR codes and blockchain explorer links
🔹 Realistic transaction details

Use /generate to create a fake transaction
Use /help for more information
""", parse_mode="Markdown")

async def generate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("Bitcoin (BTC)", callback_data="btc"),
            InlineKeyboardButton("Ethereum (ETH)", callback_data="eth"),
        ],
        [
            InlineKeyboardButton("Tether (USDT)", callback_data="usdt"),
            InlineKeyboardButton("Dogecoin (DOGE)", callback_data="doge"),
        ],
        [
            InlineKeyboardButton("Monero (XMR)", callback_data="xmr"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("""
🪙 *Select Cryptocurrency*

Choose which cryptocurrency you want to simulate:
""", reply_markup=reply_markup, parse_mode="Markdown")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    crypto = query.data
    crypto_data = CRYPTO_DATA[crypto]
    
    context.user_data["crypto"] = crypto
    await query.edit_message_text(f"""
📤 *{crypto_data['name']} Transfer*

Please enter the recipient's {crypto_data['name']} address:
(Example: `{generate_fake_address(crypto)}`)

Or send /random to use a random address
""", parse_mode="Markdown")
    
    context.user_data["awaiting_receiver"] = True

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        config = init_config()
        text = update.message.text
        
        if context.user_data.get("awaiting_receiver"):
            crypto = context.user_data["crypto"]
            crypto_data = CRYPTO_DATA[crypto]
            
            if text == "/random":
                receiver = generate_fake_address(crypto)
            else:
                receiver = text.strip()
            
            # Basic address validation
            valid = False
            if crypto == "btc":
                valid = any(receiver.startswith(p) for p in crypto_data["address_prefix"]) and len(receiver) >= 26
            elif crypto in ["eth", "usdt"]:
                valid = receiver.startswith("0x") and len(receiver) == 42
            elif crypto == "doge":
                valid = receiver.startswith("D") and len(receiver) >= 34
            elif crypto == "xmr":
                valid = (receiver.startswith("4") or receiver.startswith("8")) and len(receiver) >= 95
            
            if valid or text == "/random":
                context.user_data["receiver"] = receiver
                context.user_data["awaiting_receiver"] = False
                context.user_data["awaiting_amount"] = True
                
                await update.message.reply_text(f"""
💵 *Enter Amount*

Please enter the amount of {crypto_data['symbol']} to send:
(Minimum: {crypto_data['min_amount']}, Maximum: {crypto_data['max_amount']})

Current rate: 1 {crypto_data['symbol']} ≈ {config['exchange_rates'][crypto]} USD
""", parse_mode="Markdown")
            else:
                await update.message.reply_text(f"""
❌ *Invalid Address*

The {crypto_data['name']} address you entered doesn't appear to be valid.
Please check and try again.

Example: `{generate_fake_address(crypto)}`
""", parse_mode="Markdown")
        
        elif context.user_data.get("awaiting_amount"):
            crypto = context.user_data["crypto"]
            crypto_data = CRYPTO_DATA[crypto]
            
            try:
                amount = float(text)
                if amount < crypto_data["min_amount"]:
                    await update.message.reply_text(f"""
❌ *Amount Too Small*

Minimum transfer amount: {crypto_data['min_amount']} {crypto_data['symbol']}
""", parse_mode="Markdown")
                    return
                if amount > crypto_data["max_amount"]:
                    await update.message.reply_text(f"""
❌ *Amount Too Large*

Maximum transfer amount: {crypto_data['max_amount']} {crypto_data['symbol']}
""", parse_mode="Markdown")
                    return
                    
                context.user_data["amount"] = amount
                context.user_data["awaiting_amount"] = False
                context.user_data["awaiting_memo"] = True
                
                await update.message.reply_text(f"""
📝 *Transaction Memo*

Please enter a memo for this transaction (optional)
Or send /skip to proceed without a memo
""", parse_mode="Markdown")
            except ValueError:
                await update.message.reply_text("""
❌ *Invalid Amount*

Please enter a valid number for the amount.
Example: `1.5`
""", parse_mode="Markdown")
        
        elif context.user_data.get("awaiting_memo"):
            memo = text if text != "/skip" else ""
            crypto = context.user_data["crypto"]
            receiver = context.user_data["receiver"]
            amount = context.user_data["amount"]
            
            # Generate transaction
            config["last_ref_id"] += 1
            ref_id = f"TRX{config['last_ref_id']}"
            fee = config["network_fees"][crypto]
            sender = generate_fake_address(crypto)
            
            filename = generate_receipt(crypto, sender, receiver, amount, fee, ref_id, memo)
            save_config(config)
            
            # Send receipt with retry logic
            max_retries = 3
            retry_delay = 2  # seconds
            
            for attempt in range(max_retries):
                try:
                    with open(filename, "rb") as f:
                        await update.message.reply_document(
                            document=f,
                            caption=f"""
✅ *Fake {CRYPTO_DATA[crypto]['name']} Transaction Generated!*

▪️ Amount: *{amount} {CRYPTO_DATA[crypto]['symbol']}*
▪️ To: `{receiver}`
▪️ Fee: {fee} {CRYPTO_DATA[crypto]['symbol']}
▪️ Ref ID: {ref_id}
▪️ Memo: {memo if memo else 'None'}

📁 Receipt saved as: `{filename}`
""",
                            parse_mode="Markdown"
                        )
                    break  # Success, exit retry loop
                except Exception as e:
                    if attempt == max_retries - 1:
                        await update.message.reply_text(f"""
⚠️ *Failed to send receipt after {max_retries} attempts*

The transaction was generated but we couldn't send the file.
You can find it at: `{filename}`

Error: {str(e)}
""", parse_mode="Markdown")
                    else:
                        time.sleep(retry_delay)
            
            # Clear conversation state
            context.user_data.clear()
    
    except Exception as e:
        await update.message.reply_text(f"""
⚠️ *An error occurred*

Sorry, something went wrong while processing your request.

Error: {str(e)}
""", parse_mode="Markdown")
        # Clear conversation state to avoid getting stuck
        context.user_data.clear()

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
🆘 *Crypto Transfer Pro Help*

🔹 `/generate` - Create a fake crypto transaction
🔹 `/settings` - View current bot configuration
🔹 `/help` - Show this help message

*Features:*
- Realistic transaction receipts
- Multiple cryptocurrency support
- QR codes
- Blockchain explorer links
- Network fees
- Memo support
- Fiat value estimates
""", parse_mode="Markdown")

async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    config = init_config()
    rates = "\n".join([f"▪️ {k.upper()}: ${v}" for k, v in config["exchange_rates"].items()])
    fees = "\n".join([f"▪️ {k.upper()}: {v} {k.upper()}" for k, v in config["network_fees"].items()])
    
    await update.message.reply_text(f"""
⚙️ *Current Settings*

*Exchange Rates:*
{rates}

*Network Fees:*
{fees}

*Last Ref ID:* {config['last_ref_id']}
""", parse_mode="Markdown")

def main():
    config = init_config()
    
    if not config["telegram_token"]:
        print("""
███████╗ █████╗ ██╗  ██╗███████╗    ████████╗██████╗  █████╗ ███╗   ██╗███████╗██████╗ 
██╔════╝██╔══██╗██║ ██╔╝██╔════╝    ╚══██╔══╝██╔══██╗██╔══██╗████╗  ██║██╔════╝██╔══██╗
█████╗  ███████║█████╔╝ █████╗         ██║   ██████╔╝███████║██╔██╗ ██║█████╗  ██████╔╝
██╔══╝  ██╔══██║██╔═██╗ ██╔══╝         ██║   ██╔══██╗██╔══██║██║╚██╗██║██╔══╝  ██╔══██╗
██║     ██║  ██║██║  ██╗███████╗       ██║   ██║  ██║██║  ██║██║ ╚████║███████╗██║  ██║
╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝       ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
                                                                                        
Fake Crypto Transfer Pro - The most realistic crypto transaction generator

1. First, create a bot with @BotFather
2. Get your chat ID from @userinfobot
3. Enter your bot token below:
""")
        config["telegram_token"] = input("Bot Token: ").strip()
        config["chat_id"] = input("Chat ID: ").strip()
        save_config(config)
    
    # Create Application with error handler
    application = Application.builder().token(config["telegram_token"]).build()
    
    # Add error handler
    async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
        print(f"Update {update} caused error {context.error}")
        if update and hasattr(update, 'message') and update.message:
            try:
                await update.message.reply_text(f"""
⚠️ *An unexpected error occurred*

Sorry, something went wrong. Please try again.

Error: {str(context.error)}
""", parse_mode="Markdown")
            except:
                pass
    
    application.add_error_handler(error_handler)
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("generate", generate_command))
    application.add_handler(CommandHandler("settings", settings_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("🤖 Crypto Transfer Pro is running... Press Ctrl+C to stop")
    application.run_polling()

if __name__ == "__main__":
    main()