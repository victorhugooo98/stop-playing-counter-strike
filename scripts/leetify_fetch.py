"""Fetch Leetify profile data via the public Swagger API.

Endpoint: https://api-public.cs-prod.leetify.com/v3/profile?steam64_id=...
Documented at: https://api-public-docs.cs-prod.leetify.com/swagger.json

Reads:  data/steam-profiles-raw.csv
Writes: data/leetify-profiles.csv  (one row per SteamID with stats flattened)

Privacy: respects Leetify privacy_mode field.
"""
from __future__ import annotations

import argparse
import csv
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
INPUT_CSV = DATA_DIR / "steam-profiles-raw.csv"
OUTPUT_CSV = DATA_DIR / "leetify-profiles.csv"

LEETIFY_BASE = "https://api-public.cs-prod.leetify.com"

_rate = sapi.RateLimiter(60)  # 60 req/min, conservative

OUTPUT_FIELDS = [
    "steam_id_64",
    "steam_id_hash",
    "leetify_id",
    "privacy_mode",
    "name",
    "winrate",
    "total_matches",
    "first_match_date",
    "rank_leetify",
    "rank_premier",
    "rank_faceit",
    "rank_faceit_elo",
    "rank_wingman",
    "rating_aim",
    "rating_positioning",
    "rating_utility",
    "rating_clutch",
    "rating_opening",
    "rating_ct_leetify",
    "rating_t_leetify",
    "stat_accuracy_head",
    "stat_accuracy_enemy_spotted",
    "stat_preaim",
    "stat_reaction_time_ms",
    "stat_spray_accuracy",
    "stat_counter_strafing_good_shots_ratio",
    "stat_ct_opening_aggression_success_rate",
    "stat_ct_opening_duel_success_percentage",
    "stat_t_opening_aggression_success_rate",
    "stat_t_opening_duel_success_percentage",
    "stat_traded_deaths_success_percentage",
    "stat_trade_kill_opportunities_per_round",
    "stat_trade_kills_success_percentage",
    "stat_he_foes_damage_avg",
    "stat_flashbang_thrown",
    "stat_flashbang_leading_to_kill",
    "stat_utility_on_death_avg",
    "recent_matches_count",
    "ban_count",
]


def fetch_leetify_profile(steamid: str) -> dict | None:
    """Fetch and flatten Leetify profile. Returns None on errors or missing."""
    _rate.wait()
    try:
        r = requests.get(
            f"{LEETIFY_BASE}/v3/profile",
            params={"steam64_id": steamid},
            timeout=20,
        )
    except requests.RequestException as e:
        return {"steam_id_64": steamid, "error": str(e)}

    if r.status_code == 404:
        return None  # not on Leetify
    if r.status_code == 429:
        time.sleep(60)
        return {"steam_id_64": steamid, "error": "rate_limited"}
    if not r.ok:
        return {"steam_id_64": steamid, "error": f"http_{r.status_code}"}

    try:
        data = r.json()
    except ValueError:
        return None

    return flatten(steamid, data)


def flatten(steamid: str, data: dict) -> dict:
    ranks = data.get("ranks") or {}
    rating = data.get("rating") or {}
    stats = data.get("stats") or {}
    return {
        "steam_id_64": steamid,
        "steam_id_hash": sapi.hash_steamid(steamid),
        "leetify_id": data.get("id"),
        "privacy_mode": data.get("privacy_mode"),
        "name": "",  # do NOT store; use hash for analysis
        "winrate": data.get("winrate"),
        "total_matches": data.get("total_matches"),
        "first_match_date": data.get("first_match_date"),
        "rank_leetify": ranks.get("leetify"),
        "rank_premier": ranks.get("premier"),
        "rank_faceit": ranks.get("faceit"),
        "rank_faceit_elo": ranks.get("faceit_elo"),
        "rank_wingman": ranks.get("wingman"),
        "rating_aim": rating.get("aim"),
        "rating_positioning": rating.get("positioning"),
        "rating_utility": rating.get("utility"),
        "rating_clutch": rating.get("clutch"),
        "rating_opening": rating.get("opening"),
        "rating_ct_leetify": rating.get("ct_leetify"),
        "rating_t_leetify": rating.get("t_leetify"),
        "stat_accuracy_head": stats.get("accuracy_head"),
        "stat_accuracy_enemy_spotted": stats.get("accuracy_enemy_spotted"),
        "stat_preaim": stats.get("preaim"),
        "stat_reaction_time_ms": stats.get("reaction_time_ms"),
        "stat_spray_accuracy": stats.get("spray_accuracy"),
        "stat_counter_strafing_good_shots_ratio": stats.get("counter_strafing_good_shots_ratio"),
        "stat_ct_opening_aggression_success_rate": stats.get("ct_opening_aggression_success_rate"),
        "stat_ct_opening_duel_success_percentage": stats.get("ct_opening_duel_success_percentage"),
        "stat_t_opening_aggression_success_rate": stats.get("t_opening_aggression_success_rate"),
        "stat_t_opening_duel_success_percentage": stats.get("t_opening_duel_success_percentage"),
        "stat_traded_deaths_success_percentage": stats.get("traded_deaths_success_percentage"),
        "stat_trade_kill_opportunities_per_round": stats.get("trade_kill_opportunities_per_round"),
        "stat_trade_kills_success_percentage": stats.get("trade_kills_success_percentage"),
        "stat_he_foes_damage_avg": stats.get("he_foes_damage_avg"),
        "stat_flashbang_thrown": stats.get("flashbang_thrown"),
        "stat_flashbang_leading_to_kill": stats.get("flashbang_leading_to_kill"),
        "stat_utility_on_death_avg": stats.get("utility_on_death_avg"),
        "recent_matches_count": len(data.get("recent_matches") or []),
        "ban_count": len(data.get("bans") or []),
    }


def load_existing() -> set[str]:
    if not OUTPUT_CSV.exists():
        return set()
    df = pd.read_csv(OUTPUT_CSV, dtype={"steam_id_64": str})
    return set(df["steam_id_64"].astype(str))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(INPUT_CSV))
    parser.add_argument("--output", default=str(OUTPUT_CSV))
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--public-only", action="store_true", default=True)
    parser.add_argument("--has-cs2", action="store_true", default=True)
    args = parser.parse_args()

    df = pd.read_csv(args.input, dtype={"steam_id_64": str})
    if args.public_only:
        df = df[df["is_public"] == True]  # noqa: E712
    if args.has_cs2:
        df = df[df["has_cs2"] == True]  # noqa: E712
    print(f"Filtered profiles: {len(df)}")

    done = load_existing()
    pending = df[~df["steam_id_64"].astype(str).isin(done)]
    print(f"Already processed: {len(done)} | Pending: {len(pending)}")

    if args.limit:
        pending = pending.head(args.limit)
        print(f"Limiting to first {len(pending)}")

    out_path = Path(args.output)
    new_file = not out_path.exists()
    with out_path.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=OUTPUT_FIELDS, extrasaction="ignore")
        if new_file:
            w.writeheader()
        for sid in tqdm(pending["steam_id_64"].astype(str).tolist(), desc="leetify"):
            row = fetch_leetify_profile(sid)
            if row is None:
                # not on Leetify; record as missing for completeness
                row = {
                    "steam_id_64": sid,
                    "steam_id_hash": sapi.hash_steamid(sid),
                    "privacy_mode": "not_found",
                }
            w.writerow(row)
            f.flush()


if __name__ == "__main__":
    main()
