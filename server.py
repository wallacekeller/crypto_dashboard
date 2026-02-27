"""
Backend FastAPI — serve os dados da CoinGecko para o frontend.
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

COINGECKO_URL = "https://api.coingecko.com/api/v3"
COINS = ["bitcoin", "ethereum"]


@app.get("/api/prices")
def get_prices():
    try:
        resp = requests.get(
            f"{COINGECKO_URL}/simple/price",
            params={
                "ids": ",".join(COINS),
                "vs_currencies": "usd,brl",
                "include_24hr_change": "true",
                "include_24hr_vol": "true",
                "include_market_cap": "true",
            },
            timeout=10,
        )
        resp.raise_for_status()
        return {"ok": True, "data": resp.json()}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@app.get("/api/history/{coin_id}")
def get_history(coin_id: str):
    try:
        resp = requests.get(
            f"{COINGECKO_URL}/coins/{coin_id}/market_chart",
            params={"vs_currency": "usd", "days": 7, "interval": "daily"},
            timeout=10,
        )
        resp.raise_for_status()
        prices = [p for _, p in resp.json().get("prices", [])]
        return {"ok": True, "prices": prices}
    except Exception as e:
        return {"ok": False, "error": str(e)}


@app.get("/", response_class=HTMLResponse)
def index():
    html_path = os.path.join(os.path.dirname(__file__), "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        return f.read()