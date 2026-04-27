"""Step 3: aggregate per-profile inventory value.

Joins data/inventories.csv with data/market-prices.csv,
producing data/inventory-values.csv (one row per profile).
"""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--inventories", default=str(DATA_DIR / "inventories.csv"))
    parser.add_argument("--prices", default=str(DATA_DIR / "market-prices.csv"))
    parser.add_argument("--output", default=str(DATA_DIR / "inventory-values.csv"))
    args = parser.parse_args()

    inv = pd.read_csv(args.inventories, dtype={"steam_id_64": str})
    prices = pd.read_csv(args.prices)

    # Build map name -> price
    price_map = dict(zip(prices["market_hash_name"], prices["price_usd"]))

    # Mark privacy / empty profiles via pseudo-rows
    private = inv[inv["market_hash_name"] == "__PRIVATE__"]["steam_id_64"].unique()
    empty = inv[inv["market_hash_name"] == "__EMPTY__"]["steam_id_64"].unique()
    real_items = inv[~inv["market_hash_name"].isin(["__PRIVATE__", "__EMPTY__"])].copy()
    real_items["price_usd"] = real_items["market_hash_name"].map(price_map).fillna(0)
    real_items["row_value"] = real_items["price_usd"] * real_items["count"]

    # Aggregate per profile
    agg = real_items.groupby(["steam_id_64", "steam_id_hash"]).agg(
        item_count_unique=("market_hash_name", "nunique"),
        item_count_total=("count", "sum"),
        marketable_count=("count", lambda s: int(s[real_items.loc[s.index, "marketable"] == True].sum()) if (real_items.loc[s.index, "marketable"] == True).any() else 0),  # noqa: E712
        total_usd=("row_value", "sum"),
        max_item_usd=("price_usd", "max"),
        items_priced=("price_usd", lambda s: int((s > 0).sum())),
    ).reset_index()
    agg["inventory_public"] = True

    # Add private / empty rows
    extras = []
    for sid in private:
        extras.append({
            "steam_id_64": sid,
            "steam_id_hash": real_items.iloc[0]["steam_id_hash"] if len(real_items) > 0 else "",
            "inventory_public": False,
            "item_count_unique": 0,
            "item_count_total": 0,
            "marketable_count": 0,
            "total_usd": 0.0,
            "max_item_usd": 0.0,
            "items_priced": 0,
        })
    for sid in empty:
        if sid in agg["steam_id_64"].values:
            continue
        extras.append({
            "steam_id_64": sid,
            "steam_id_hash": "",
            "inventory_public": True,
            "item_count_unique": 0,
            "item_count_total": 0,
            "marketable_count": 0,
            "total_usd": 0.0,
            "max_item_usd": 0.0,
            "items_priced": 0,
        })
    if extras:
        agg = pd.concat([agg, pd.DataFrame(extras)], ignore_index=True)

    # Reproduce hash if missing in extras
    import steam_api as sapi
    mask = agg["steam_id_hash"].isna() | (agg["steam_id_hash"] == "")
    agg.loc[mask, "steam_id_hash"] = agg.loc[mask, "steam_id_64"].apply(sapi.hash_steamid)

    agg = agg[[
        "steam_id_64", "steam_id_hash", "inventory_public",
        "item_count_unique", "item_count_total", "marketable_count",
        "total_usd", "max_item_usd", "items_priced",
    ]]
    agg.to_csv(args.output, index=False)
    print(f"Wrote {args.output} ({len(agg)} rows)")
    pub_with_value = agg[(agg["inventory_public"]) & (agg["total_usd"] > 0)]
    print(f"Public + nonzero value: {len(pub_with_value)}")
    if len(pub_with_value):
        print(pub_with_value[["item_count_total", "total_usd", "max_item_usd"]].describe())


if __name__ == "__main__":
    main()
