"""BFS crawler from seed Steam profiles.

Walks the friends graph from configured seeds, fetching public profile data
for each node. Saves periodically to support resume.

Output: data/steam-profiles-raw.csv (one row per visited SteamID)
        data/friends-edges.csv      (edges of the friendship graph)

Usage:
    python scripts/seed_friends_crawler.py [--hops 2] [--max-profiles 3000]
"""
from __future__ import annotations

import argparse
import csv
import os
import sys
import time
from collections import deque
from pathlib import Path

from dotenv import load_dotenv
from tqdm import tqdm

import steam_api as sapi

ROOT = Path(__file__).parent.parent
load_dotenv(ROOT / ".env")

DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

PROFILES_CSV = DATA_DIR / "steam-profiles-raw.csv"
EDGES_CSV = DATA_DIR / "friends-edges.csv"
PROGRESS_FILE = DATA_DIR / ".crawler_progress.json"

PROFILE_FIELDS = [
    "steam_id_64",
    "steam_id_hash",
    "hop_distance",
    "discovered_via",
    "exists",
    "visibility",
    "is_public",
    "country_code",
    "time_created",
    "last_logoff",
    "profile_state",
    "total_games_owned",
    "has_cs2",
    "cs2_minutes_total",
    "cs2_minutes_2weeks",
    "steam_level",
    "player_xp",
    "player_level",
    "badges_count",
    "vac_banned",
    "number_of_vac_bans",
    "number_of_game_bans",
    "community_banned",
    "economy_ban",
    "friends_count",
    "friends_public",
]


def load_seeds() -> list[str]:
    """Load seed SteamIDs from .env, resolving vanities if needed."""
    seeds: list[str] = []

    sid_csv = os.environ.get("SEED_STEAM_IDS", "").strip()
    if sid_csv:
        seeds.extend([s.strip() for s in sid_csv.split(",") if s.strip()])

    vanity_csv = os.environ.get("SEED_VANITY_URLS", "").strip()
    if vanity_csv:
        for v in [s.strip() for s in vanity_csv.split(",") if s.strip()]:
            sid = sapi.resolve_vanity(v)
            if sid:
                seeds.append(sid)
                print(f"[seeds] Resolved vanity '{v}' -> {sid}")
            else:
                print(f"[seeds] WARNING: could not resolve vanity '{v}'")

    seeds = list(dict.fromkeys(seeds))  # dedupe, preserve order
    if not seeds:
        sys.exit("No seeds configured. Set SEED_STEAM_IDS or SEED_VANITY_URLS in .env")
    return seeds


def load_existing_profiles() -> dict[str, dict]:
    """Read previously collected SteamIDs to support resume.

    Returns dict {steamid: row} so we can decide whether to expand from each.
    """
    if not PROFILES_CSV.exists():
        return {}
    out: dict[str, dict] = {}
    with PROFILES_CSV.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            out[row["steam_id_64"]] = row
    return out


def append_profile(row: dict) -> None:
    new_file = not PROFILES_CSV.exists()
    with PROFILES_CSV.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=PROFILE_FIELDS, extrasaction="ignore")
        if new_file:
            w.writeheader()
        w.writerow(row)


def append_edges(source: str, friends: list[dict]) -> None:
    """Append friendship edges. Note: src + dst are SteamID 64s, not hashed.

    This file is in .gitignore territory if you publish data — see ethics_check.py.
    For analysis, edges are useful; for publication, hash them.
    """
    new_file = not EDGES_CSV.exists()
    with EDGES_CSV.open("a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new_file:
            w.writerow(["src_steam_id", "dst_steam_id", "friend_since"])
        for fr in friends:
            w.writerow([source, fr.get("steamid"), fr.get("friend_since", "")])


def crawl(
    seeds: list[str],
    *,
    max_hops: int,
    max_profiles: int,
    only_brazil: bool = False,
) -> None:
    existing = load_existing_profiles()  # dict[steamid -> row]
    seen: set[str] = set(existing.keys())
    queue: deque[tuple[str, int, str]] = deque()
    expanded: set[str] = set()  # nodes we've already pulled friend lists for

    # Detect previously-expanded nodes by inspecting friends-edges.csv
    if EDGES_CSV.exists():
        with EDGES_CSV.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                expanded.add(row["src_steam_id"])

    # Add seeds
    for s in seeds:
        if s not in seen:
            queue.append((s, 0, "seed"))

    # Re-expand any previously-collected profile whose hop_distance < max_hops
    # and that hasn't been expanded yet.
    re_expand = 0
    for sid, row in existing.items():
        try:
            hop = int(row.get("hop_distance", 99))
        except (TypeError, ValueError):
            hop = 99
        is_pub = str(row.get("is_public")).lower() == "true"
        has_cs2 = str(row.get("has_cs2")).lower() == "true"
        if (
            is_pub
            and has_cs2
            and hop < max_hops
            and sid not in expanded
        ):
            queue.append((sid, hop, row.get("discovered_via", "seed")))
            re_expand += 1

    print(f"[crawler] Seeds: {seeds}")
    print(f"[crawler] Already collected: {len(seen)} profiles")
    print(f"[crawler] Re-queued for expansion: {re_expand}")
    print(f"[crawler] Already expanded (in edges): {len(expanded)}")
    print(f"[crawler] Max hops: {max_hops} | Max profiles: {max_profiles}")

    pbar = tqdm(total=max_profiles, initial=len(seen), desc="profiles")

    try:
        while queue and len(seen) < max_profiles:
            steamid, hop, via = queue.popleft()

            if steamid in seen:
                # Already collected: only expand its friends if not yet expanded
                if steamid in expanded:
                    continue
                profile = existing.get(steamid, {})
                # Convert string flags from CSV to bool
                is_pub = str(profile.get("is_public")).lower() == "true"
                has_cs2 = str(profile.get("has_cs2")).lower() == "true"
                country = profile.get("country_code", "")
            else:
                try:
                    profile = sapi.fetch_full_profile(steamid)
                except Exception as e:
                    tqdm.write(f"[!] error on {steamid}: {e}")
                    continue

                profile["hop_distance"] = hop
                profile["discovered_via"] = via
                append_profile(profile)
                seen.add(steamid)
                pbar.update(1)
                is_pub = bool(profile.get("is_public"))
                has_cs2 = bool(profile.get("has_cs2"))
                country = profile.get("country_code", "")

            # Decide whether to expand from this node
            should_expand = is_pub and has_cs2 and hop < max_hops
            if only_brazil and country != "BR":
                should_expand = False

            if should_expand and steamid not in expanded:
                friends = sapi.get_friend_list(steamid)
                expanded.add(steamid)
                if friends:
                    append_edges(steamid, friends)
                    for fr in friends:
                        fid = fr.get("steamid")
                        if fid and fid not in seen:
                            queue.append((fid, hop + 1, steamid))

    except KeyboardInterrupt:
        tqdm.write("\n[crawler] Interrupted by user. Progress saved.")
    finally:
        pbar.close()

    print(f"\n[crawler] Total collected: {len(seen)} profiles")
    print(f"[crawler] Output: {PROFILES_CSV}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--hops", type=int, default=int(os.environ.get("MAX_HOPS", "2")))
    parser.add_argument(
        "--max-profiles",
        type=int,
        default=int(os.environ.get("MAX_PROFILES", "3000")),
    )
    parser.add_argument(
        "--only-brazil",
        action="store_true",
        help="Only expand from BR profiles (smaller, more focused sample)",
    )
    args = parser.parse_args()

    seeds = load_seeds()
    crawl(
        seeds,
        max_hops=args.hops,
        max_profiles=args.max_profiles,
        only_brazil=args.only_brazil,
    )


if __name__ == "__main__":
    main()
