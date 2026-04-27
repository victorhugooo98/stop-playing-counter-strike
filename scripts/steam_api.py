"""Core Steam Web API wrapper with caching, rate limiting, and error handling.

This module is shared by all collection scripts. It centralizes:
- Authentication (reads STEAM_API_KEY from .env)
- Rate limiting (token bucket, conservative defaults)
- Disk-based response caching (JSON, TTL configurable)
- Error handling (401 = private, 403 = forbidden, 429 = rate limit, 5xx = retry)
- SteamID hashing for PII-safe outputs

References:
- https://partner.steamgames.com/doc/webapi/ISteamUser
- https://partner.steamgames.com/doc/webapi/IPlayerService
- https://steamapi.xpaw.me/ (community-curated documentation)
"""
from __future__ import annotations

import hashlib
import json
import os
import random
import time
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).parent.parent
CACHE_DIR = ROOT / "cache"
CACHE_DIR.mkdir(exist_ok=True)

load_dotenv(ROOT / ".env")

API_KEY = os.environ.get("STEAM_API_KEY")
if not API_KEY:
    raise RuntimeError("STEAM_API_KEY missing from .env")

CACHE_TTL_SECONDS = int(os.environ.get("CACHE_TTL_HOURS", "24")) * 3600
RATE_API = int(os.environ.get("RATE_LIMIT_STEAM_API", "100"))  # req/min

# CS2 / CS:GO / Counter-Strike 2 app id
CS2_APPID = 730


# ---------------------------------------------------------------------------
# Rate limiter (simple token bucket)
# ---------------------------------------------------------------------------
class RateLimiter:
    def __init__(self, requests_per_minute: int):
        self.interval = 60.0 / max(requests_per_minute, 1)
        self.last_call = 0.0

    def wait(self) -> None:
        now = time.monotonic()
        elapsed = now - self.last_call
        if elapsed < self.interval:
            time.sleep(self.interval - elapsed)
        self.last_call = time.monotonic()


_rate = RateLimiter(RATE_API)


# ---------------------------------------------------------------------------
# Cache helpers
# ---------------------------------------------------------------------------
def _cache_key(endpoint: str, params: dict) -> Path:
    safe_params = {k: v for k, v in params.items() if k != "key"}
    h = hashlib.sha256(
        f"{endpoint}|{json.dumps(safe_params, sort_keys=True)}".encode()
    ).hexdigest()[:24]
    return CACHE_DIR / f"{h}.json"


def _read_cache(path: Path, ttl: int = CACHE_TTL_SECONDS) -> dict | None:
    if not path.exists():
        return None
    age = time.time() - path.stat().st_mtime
    if age > ttl:
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def _write_cache(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data), encoding="utf-8")


# ---------------------------------------------------------------------------
# Generic fetcher
# ---------------------------------------------------------------------------
def _fetch(
    endpoint: str,
    params: dict,
    *,
    use_cache: bool = True,
    ttl: int = CACHE_TTL_SECONDS,
    retries: int = 3,
) -> dict | None:
    """GET an endpoint with caching, rate limiting, and retry on 5xx/429.

    Returns parsed JSON dict, or None for 401/403/404 (treat as missing data).
    Raises RuntimeError on persistent failure.
    """
    cache_path = _cache_key(endpoint, params)
    if use_cache:
        cached = _read_cache(cache_path, ttl)
        if cached is not None:
            return cached

    full_params = {"key": API_KEY, **params}

    last_err: Exception | None = None
    for attempt in range(retries):
        _rate.wait()
        try:
            r = requests.get(endpoint, params=full_params, timeout=15)
        except requests.RequestException as e:
            last_err = e
            time.sleep(2 ** attempt + random.random())
            continue

        if r.status_code in (401, 403):
            return None  # private
        if r.status_code == 404:
            return None
        if r.status_code == 429:
            wait = (2 ** attempt) * 5 + random.uniform(1, 3)
            time.sleep(wait)
            continue
        if r.status_code >= 500:
            time.sleep(2 ** attempt)
            continue

        try:
            r.raise_for_status()
        except requests.HTTPError as e:
            last_err = e
            continue

        try:
            data = r.json()
        except ValueError:
            return None

        if use_cache:
            _write_cache(cache_path, data)
        return data

    if last_err:
        raise RuntimeError(f"Failed {endpoint}: {last_err}") from last_err
    return None


# ---------------------------------------------------------------------------
# High-level Steam API functions
# ---------------------------------------------------------------------------
def resolve_vanity(vanity: str) -> str | None:
    data = _fetch(
        "https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/",
        {"vanityurl": vanity},
    )
    if not data:
        return None
    response = data.get("response", {})
    if response.get("success") == 1:
        return response.get("steamid")
    return None


def get_player_summary(steamid: str) -> dict:
    data = _fetch(
        "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/",
        {"steamids": steamid},
    )
    if not data:
        return {}
    players = data.get("response", {}).get("players", [])
    return players[0] if players else {}


def get_player_summaries_batch(steamids: list[str]) -> list[dict]:
    """Up to 100 SteamIDs per call."""
    if not steamids:
        return []
    all_players: list[dict] = []
    for i in range(0, len(steamids), 100):
        chunk = steamids[i : i + 100]
        data = _fetch(
            "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/",
            {"steamids": ",".join(chunk)},
        )
        if data:
            all_players.extend(data.get("response", {}).get("players", []))
    return all_players


def get_owned_games(steamid: str) -> dict:
    data = _fetch(
        "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/",
        {
            "steamid": steamid,
            "include_played_free_games": 1,
            "include_appinfo": 0,
        },
    )
    return (data or {}).get("response", {})


def get_steam_level(steamid: str) -> int | None:
    data = _fetch(
        "https://api.steampowered.com/IPlayerService/GetSteamLevel/v1/",
        {"steamid": steamid},
    )
    if not data:
        return None
    return data.get("response", {}).get("player_level")


def get_friend_list(steamid: str) -> list[dict]:
    """Returns list of {steamid, relationship, friend_since}.

    Empty if friend list is private.
    """
    data = _fetch(
        "https://api.steampowered.com/ISteamUser/GetFriendList/v1/",
        {"steamid": steamid, "relationship": "friend"},
    )
    if not data:
        return []
    return data.get("friendslist", {}).get("friends", [])


def get_user_stats_for_game(steamid: str, appid: int = CS2_APPID) -> dict:
    """Game-specific stats. Often empty for CS2 (Valve restricted)."""
    data = _fetch(
        "https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v2/",
        {"steamid": steamid, "appid": appid},
    )
    return (data or {}).get("playerstats", {})


def get_player_bans(steamid: str) -> dict:
    data = _fetch(
        "https://api.steampowered.com/ISteamUser/GetPlayerBans/v1/",
        {"steamids": steamid},
    )
    if not data:
        return {}
    players = data.get("players", [])
    return players[0] if players else {}


def get_player_badges(steamid: str) -> dict:
    data = _fetch(
        "https://api.steampowered.com/IPlayerService/GetBadges/v1/",
        {"steamid": steamid},
    )
    return (data or {}).get("response", {})


# ---------------------------------------------------------------------------
# Inventory (community endpoint, not Web API — no key needed)
# ---------------------------------------------------------------------------
_INV_HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.5",
    "X-Requested-With": "XMLHttpRequest",
}


def get_cs2_inventory(steamid: str) -> dict | None:
    """Public inventory via community endpoint. Returns None if private.

    Steam community returns 403 for private inventories and 200 with
    {"success": false} for some genuinely empty / restricted ones.
    """
    cache_path = _cache_key("inventory", {"steamid": steamid})
    cached = _read_cache(cache_path, ttl=CACHE_TTL_SECONDS)
    if cached is not None:
        # Negative cache: recheck if previous attempt said "not public"
        if cached.get("_negative"):
            return None
        return cached

    _rate.wait()
    url = f"https://steamcommunity.com/inventory/{steamid}/{CS2_APPID}/2"
    headers = dict(_INV_HEADERS)
    headers["Referer"] = f"https://steamcommunity.com/profiles/{steamid}/inventory"

    try:
        r = requests.get(
            url,
            params={"l": "english", "count": "2000"},
            timeout=20,
            headers=headers,
        )
    except requests.RequestException:
        return None
    if r.status_code in (401, 403, 404):
        _write_cache(cache_path, {"_negative": True})
        return None
    if r.status_code == 429:
        time.sleep(30)
        return None
    if not r.ok:
        return None
    try:
        data = r.json()
    except ValueError:
        return None
    if not data or data.get("success") is False:
        _write_cache(cache_path, {"_negative": True})
        return None
    _write_cache(cache_path, data)
    return data


# ---------------------------------------------------------------------------
# PII helpers
# ---------------------------------------------------------------------------
def hash_steamid(steamid: str | int, *, salt: str = "stop-playing-cs-v1") -> str:
    """Hash SteamID 64 to 16-char hex prefix for safe publication."""
    h = hashlib.sha256(f"{salt}|{steamid}".encode()).hexdigest()
    return h[:16]


# ---------------------------------------------------------------------------
# Aggregate profile fetcher
# ---------------------------------------------------------------------------
def fetch_full_profile(steamid: str) -> dict:
    """Aggregate everything we need for analysis into a flat dict.

    Public fields only. Private endpoints return None / empty silently.
    """
    summary = get_player_summary(steamid)
    if not summary:
        return {"steam_id_64": steamid, "exists": False}

    visibility = summary.get("communityvisibilitystate", 1)
    is_public = visibility == 3

    out: dict[str, Any] = {
        "steam_id_64": steamid,
        "steam_id_hash": hash_steamid(steamid),
        "exists": True,
        "visibility": visibility,
        "is_public": is_public,
        "persona_state": summary.get("personastate"),
        "country_code": summary.get("loccountrycode"),
        "time_created": summary.get("timecreated"),
        "last_logoff": summary.get("lastlogoff"),
        "profile_state": summary.get("profilestate"),
    }

    if not is_public:
        return out

    # Owned games
    games = get_owned_games(steamid)
    out["total_games_owned"] = games.get("game_count", 0)
    cs2 = next(
        (g for g in games.get("games", []) if g.get("appid") == CS2_APPID),
        None,
    )
    if cs2:
        out["cs2_minutes_total"] = cs2.get("playtime_forever", 0)
        out["cs2_minutes_2weeks"] = cs2.get("playtime_2weeks", 0)
        out["has_cs2"] = True
    else:
        out["cs2_minutes_total"] = 0
        out["cs2_minutes_2weeks"] = 0
        out["has_cs2"] = False

    # Steam level + badges
    out["steam_level"] = get_steam_level(steamid)
    badges = get_player_badges(steamid)
    out["player_xp"] = badges.get("player_xp", 0)
    out["player_level"] = badges.get("player_level", 0)
    out["badges_count"] = len(badges.get("badges", []))

    # Bans
    bans = get_player_bans(steamid)
    out["vac_banned"] = bans.get("VACBanned", False)
    out["number_of_vac_bans"] = bans.get("NumberOfVACBans", 0)
    out["number_of_game_bans"] = bans.get("NumberOfGameBans", 0)
    out["community_banned"] = bans.get("CommunityBanned", False)
    out["economy_ban"] = bans.get("EconomyBan", "none")

    # Friends list size (signal for engagement); we don't store the list itself in profile row
    friends = get_friend_list(steamid)
    out["friends_count"] = len(friends)
    out["friends_public"] = len(friends) > 0  # if 0 may be private OR genuinely 0

    return out


if __name__ == "__main__":
    # Quick self-test
    print("Self-test: fetching vhs profile...")
    sid = resolve_vanity("vhschmidt")
    print(f"  Vanity resolved: {sid}")
    p = fetch_full_profile(sid)
    for k, v in p.items():
        print(f"  {k}: {v}")
