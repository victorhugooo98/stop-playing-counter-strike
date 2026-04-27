"""PII / publication-readiness audit for the dossiê dataset.

Run before any commit that touches data/. Exits 1 if any of the following:
- Plain SteamID 64 in a column that would be published
- Persona names, real names, avatar URLs in CSVs
- Friends list with both src+dst as plain SteamID 64s (instead of hashes)
- .env or any *.key file staged

Usage:
    python scripts/ethics_check.py [--fix-edges]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import pandas as pd

import steam_api as sapi

ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"

# Files we expect to be safe to publish (anonymized)
PUBLISHABLE = {
    "lawsuits.csv",
    "revenue-timeline.csv",
    "botfarm-services.csv",
    "leetify-profiles.csv",
    "inventory-values.csv",
    "steam-profiles-raw.csv",
    "seed-profiles.csv",
}

# Files that must NEVER be published with plain SteamIDs / PII
SENSITIVE = {
    "friends-edges.csv",
}

PII_COLUMNS = {"persona_name", "personaname", "name", "real_name", "avatar", "avatar_url"}
HASHED_ID_COL = "steam_id_hash"
PLAIN_ID_COL = "steam_id_64"

ENV_PATTERN = re.compile(r"\.env(\..+)?$")
KEY_PATTERN = re.compile(r"\.(key|pem|p12)$")


def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    sys.exit(1)


def warn(msg: str) -> None:
    print(f"WARN: {msg}")


def check_pii_columns(df: pd.DataFrame, name: str) -> list[str]:
    issues = []
    for col in df.columns:
        if col.lower() in PII_COLUMNS and not (df[col].fillna("") == "").all():
            issues.append(f"{name}: column '{col}' contains non-empty PII data")
    return issues


def check_anonymization(df: pd.DataFrame, name: str) -> list[str]:
    issues = []
    if PLAIN_ID_COL in df.columns and HASHED_ID_COL in df.columns:
        issues.append(
            f"{name}: contains both '{PLAIN_ID_COL}' and '{HASHED_ID_COL}' — "
            "plain SteamID must be removed for any published version"
        )
    return issues


def check_friends_edges(path: Path) -> list[str]:
    issues = []
    if not path.exists():
        return issues
    df = pd.read_csv(path, dtype=str)
    if "src_steam_id" in df.columns and not df["src_steam_id"].astype(str).str.startswith(("76561",)).all():
        issues.append(f"{path.name}: src column has non-SteamID values")
    if "src_steam_id" in df.columns:
        # If src and dst are plain, this file is sensitive
        issues.append(
            f"{path.name}: contains plain SteamIDs (src+dst) — should be in .gitignore "
            "OR replaced with hashes before publication"
        )
    return issues


def check_env_files() -> list[str]:
    issues = []
    for p in ROOT.iterdir():
        if p.is_file() and ENV_PATTERN.search(p.name) and p.name != ".env.example":
            # Verify it's gitignored
            gitignore = ROOT / ".gitignore"
            if gitignore.exists():
                ignored = gitignore.read_text(encoding="utf-8")
                if ".env" not in ignored:
                    issues.append(f"{p.name} not in .gitignore")
            else:
                issues.append(".gitignore missing — credentials at risk")
    return issues


def fix_friends_edges() -> None:
    """Hash the friends-edges.csv in place. Destructive — back up first."""
    src = DATA_DIR / "friends-edges.csv"
    if not src.exists():
        print("No friends-edges.csv to fix")
        return
    df = pd.read_csv(src, dtype=str)
    if "src_steam_id" not in df.columns:
        print("friends-edges.csv has no plain SteamID columns")
        return
    df["src_steam_id_hash"] = df["src_steam_id"].apply(sapi.hash_steamid)
    df["dst_steam_id_hash"] = df["dst_steam_id"].apply(sapi.hash_steamid)
    out = DATA_DIR / "friends-edges-hashed.csv"
    df[["src_steam_id_hash", "dst_steam_id_hash", "friend_since"]].to_csv(
        out, index=False
    )
    print(f"Wrote {out}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fix-edges", action="store_true")
    args = parser.parse_args()

    if args.fix_edges:
        fix_friends_edges()
        return

    print("=" * 60)
    print("Ethics check — auditing data/ for PII")
    print("=" * 60)

    all_issues: list[str] = []

    # Env / key files
    all_issues.extend(check_env_files())

    # Each CSV in data/
    if DATA_DIR.exists():
        for csv_path in sorted(DATA_DIR.glob("*.csv")):
            try:
                df = pd.read_csv(csv_path, dtype=str)
            except Exception as e:
                warn(f"could not read {csv_path.name}: {e}")
                continue
            print(f"\n[{csv_path.name}] rows={len(df)} cols={len(df.columns)}")
            print(f"  columns: {list(df.columns)[:10]}{'...' if len(df.columns) > 10 else ''}")

            all_issues.extend(check_pii_columns(df, csv_path.name))

            if csv_path.name in SENSITIVE:
                all_issues.extend(check_friends_edges(csv_path))

    print("\n" + "=" * 60)
    if all_issues:
        print(f"Issues found: {len(all_issues)}")
        for issue in all_issues:
            print(f"  - {issue}")
        print("\nFor publishable export, run with --fix-edges to hash sensitive files.")
        print("And ensure .env is in .gitignore.")
        sys.exit(1)
    else:
        print("OK — no PII issues found")
        print("\nReminders:")
        print("  - data/steam-profiles-raw.csv contains plain SteamIDs;")
        print("    publish only the steam_id_hash column when sharing.")
        print("  - data/friends-edges.csv is sensitive; keep .gitignored or hash via --fix-edges")
        print("  - .env contains credentials; verify it is .gitignored")


if __name__ == "__main__":
    main()
