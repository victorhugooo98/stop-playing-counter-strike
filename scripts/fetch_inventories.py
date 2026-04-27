"""Step 1 of inventory pipeline: fetch raw inventories (no pricing).

Fast: only hits steamcommunity.com inventory endpoint.
Output: data/inventories.csv with one row per (steam_id, market_hash_name)
        listing item counts per type.

Pricing is done in step 2 (price_market_items.py).
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from tqdm import tqdm

import steam_api as sapi

ROOT = Path(__file__).parent.parent
load_dotenv(ROOT / ".env")

DATA_DIR = ROOT / "data"
INPUT_CSV = DATA_DIR / "steam-profiles-raw.csv"
OUTPUT_CSV = DATA_DIR / "inventories.csv"

FIELDS = ["steam_id_64", "steam_id_hash", "market_hash_name", "count", "marketable"]


def parse_inventory(raw: dict) -> list[dict]:
    if not raw:
        return []
    descs = {
        f"{d['classid']}_{d.get('instanceid', '0')}": d
        for d in raw.get("descriptions", [])
    }
    items: dict[str, dict] = {}
    for asset in raw.get("assets", []):
        key = f"{asset['classid']}_{asset.get('instanceid', '0')}"
        d = descs.get(key)
        if not d:
            continue
        name = (d.get("market_hash_name") or "").strip()
        if not name:
            continue
        marketable = bool(d.get("marketable", 0))
        if name not in items:
            items[name] = {"market_hash_name": name, "count": 0, "marketable": marketable}
        items[name]["count"] += 1
    return list(items.values())


def load_existing() -> set[str]:
    if not OUTPUT_CSV.exists():
        return set()
    df = pd.read_csv(OUTPUT_CSV, dtype={"steam_id_64": str})
    return set(df["steam_id_64"].unique().tolist())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(INPUT_CSV))
    parser.add_argument("--output", default=str(OUTPUT_CSV))
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    df = pd.read_csv(args.input, dtype={"steam_id_64": str})
    df = df[(df["is_public"] == True) & (df["has_cs2"] == True)]  # noqa: E712
    print(f"Filtered profiles: {len(df)}")

    done = load_existing()
    pending = df[~df["steam_id_64"].astype(str).isin(done)]
    print(f"Already processed: {len(done)} | Pending: {len(pending)}")

    if args.limit:
        pending = pending.head(args.limit)

    out_path = Path(args.output)
    new_file = not out_path.exists()
    with out_path.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        if new_file:
            w.writeheader()
        for sid in tqdm(pending["steam_id_64"].astype(str).tolist(), desc="inventories"):
            raw = sapi.get_cs2_inventory(sid)
            if raw is None:
                # private inventory — record marker row so we don't retry
                w.writerow({
                    "steam_id_64": sid,
                    "steam_id_hash": sapi.hash_steamid(sid),
                    "market_hash_name": "__PRIVATE__",
                    "count": 0,
                    "marketable": False,
                })
                f.flush()
                continue
            items = parse_inventory(raw)
            if not items:
                w.writerow({
                    "steam_id_64": sid,
                    "steam_id_hash": sapi.hash_steamid(sid),
                    "market_hash_name": "__EMPTY__",
                    "count": 0,
                    "marketable": False,
                })
            else:
                for item in items:
                    w.writerow({
                        "steam_id_64": sid,
                        "steam_id_hash": sapi.hash_steamid(sid),
                        "market_hash_name": item["market_hash_name"],
                        "count": item["count"],
                        "marketable": item["marketable"],
                    })
            f.flush()


if __name__ == "__main__":
    main()
