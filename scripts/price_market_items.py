"""Step 2 of inventory pipeline: price every UNIQUE market_hash_name once.

Reads:  data/inventories.csv
Writes: data/market-prices.csv  (market_hash_name -> price_usd, volume)
        cache/market_prices.json (persistent cache)

Then step 3 (aggregate_inventory.py) joins the two to produce per-profile values.

This separation lets us cache prices across all profiles and avoid redundant
calls — the same skin appearing in 50 inventories gets priced once.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import time
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv
from tqdm import tqdm

import steam_api as sapi

ROOT = Path(__file__).parent.parent
load_dotenv(ROOT / ".env")

DATA_DIR = ROOT / "data"
CACHE_DIR = ROOT / "cache"
CACHE_DIR.mkdir(exist_ok=True)
PRICE_CACHE = CACHE_DIR / "market_prices.json"
INPUT_CSV = DATA_DIR / "inventories.csv"
OUTPUT_CSV = DATA_DIR / "market-prices.csv"

# Steam Market is rate-limited ~20/min without auth; we go 25 with retries.
RATE_MARKET = int(os.environ.get("RATE_LIMIT_STEAM_MARKET", "25"))
_rate = sapi.RateLimiter(RATE_MARKET)
PRICE_TTL_SECONDS = 7 * 24 * 3600


def _parse(s: str) -> float:
    if not s:
        return 0.0
    return float(s.replace("$", "").replace(",", "").strip() or 0)


def load_cache() -> dict[str, dict]:
    if PRICE_CACHE.exists():
        try:
            return json.loads(PRICE_CACHE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def save_cache(c: dict) -> None:
    PRICE_CACHE.write_text(json.dumps(c), encoding="utf-8")


def fetch_price(name: str, cache: dict) -> dict:
    entry = cache.get(name)
    if entry and (time.time() - entry.get("ts", 0)) < PRICE_TTL_SECONDS:
        return entry
    _rate.wait()
    try:
        r = requests.get(
            "https://steamcommunity.com/market/priceoverview/",
            params={
                "appid": sapi.CS2_APPID,
                "currency": 1,
                "market_hash_name": name,
            },
            timeout=15,
            headers={"User-Agent": "Mozilla/5.0"},
        )
    except requests.RequestException as e:
        return {"price_usd": 0.0, "volume": 0, "source": "error", "ts": time.time(), "err": str(e)}

    if r.status_code == 429:
        time.sleep(60)
        return {"price_usd": 0.0, "volume": 0, "source": "rate_limited", "ts": time.time()}
    if not r.ok:
        return {"price_usd": 0.0, "volume": 0, "source": f"http_{r.status_code}", "ts": time.time()}
    try:
        d = r.json()
    except ValueError:
        return {"price_usd": 0.0, "volume": 0, "source": "invalid_json", "ts": time.time()}

    if not d.get("success"):
        entry = {"price_usd": 0.0, "volume": 0, "source": "no_market", "ts": time.time()}
    else:
        price_str = d.get("lowest_price") or d.get("median_price") or "$0"
        vol_str = (d.get("volume") or "0").replace(",", "")
        try:
            volume = int(vol_str)
        except ValueError:
            volume = 0
        entry = {
            "price_usd": _parse(price_str),
            "volume": volume,
            "source": "steam_market",
            "ts": time.time(),
        }
    cache[name] = entry
    return entry


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(INPUT_CSV))
    parser.add_argument("--output", default=str(OUTPUT_CSV))
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument(
        "--marketable-only",
        action="store_true",
        default=True,
        help="Only price marketable items (default)",
    )
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    if args.marketable_only:
        df = df[df["marketable"] == True]  # noqa: E712
    # Drop pseudo-rows and price uniques
    df = df[~df["market_hash_name"].isin(["__PRIVATE__", "__EMPTY__"])]
    unique_names = df["market_hash_name"].dropna().unique().tolist()
    print(f"Unique marketable items to price: {len(unique_names)}")

    cache = load_cache()
    print(f"Cache hits available: {len(cache)}")

    if args.limit:
        unique_names = unique_names[: args.limit]

    rows = []
    saved_every = 50
    for i, name in enumerate(tqdm(unique_names, desc="prices")):
        info = fetch_price(name, cache)
        rows.append({
            "market_hash_name": name,
            "price_usd": info.get("price_usd", 0.0),
            "volume": info.get("volume", 0),
            "source": info.get("source", "unknown"),
        })
        if (i + 1) % saved_every == 0:
            save_cache(cache)

    save_cache(cache)
    out_df = pd.DataFrame(rows)
    out_df.to_csv(args.output, index=False)
    print(f"\nWrote {args.output} ({len(out_df)} rows)")
    priced = out_df[out_df["price_usd"] > 0]
    print(f"Successfully priced: {len(priced)} / {len(out_df)}")


if __name__ == "__main__":
    main()
