"""Generate publication-safe versions of all data CSVs.

Reads every CSV under data/ and writes a sanitized copy under data/published/:
- Drops `steam_id_64` column (keeps `steam_id_hash`)
- Drops common PII fields (name, real_name, avatar_url, persona_name, last_logoff)
- Replaces friends-edges.csv with friends-edges-hashed.csv contents
- Skips files explicitly listed in NEVER_PUBLISH

Usage:
    python scripts/sanitize_for_publication.py
    python scripts/ethics_check.py --pre-publish   # verify
"""
from __future__ import annotations

import shutil
from pathlib import Path

import pandas as pd

import steam_api as sapi

ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"
PUB_DIR = DATA_DIR / "published"

# Columns dropped from any CSV before publication
DROP_COLUMNS = {
    "steam_id_64",
    "name",
    "real_name",
    "personaname",
    "persona_name",
    "avatar",
    "avatar_url",
    "last_logoff",  # behavioral fingerprint
}

# Files that should NEVER appear in the published directory
NEVER_PUBLISH = {
    "friends-edges.csv",  # plain IDs; replaced by friends-edges-hashed.csv
    ".crawler_progress.json",
}

# Files copied as-is (already safe)
PASSTHROUGH = {
    "lawsuits.csv",
    "revenue-timeline.csv",
    "botfarm-services.csv",
    "market-prices.csv",
    "network-metrics.csv",
    "friends-edges-hashed.csv",
    "README.md",
}


def ensure_hash(df: pd.DataFrame) -> pd.DataFrame:
    """If steam_id_64 is present and steam_id_hash is missing, derive hash."""
    if "steam_id_64" in df.columns and (
        "steam_id_hash" not in df.columns or df["steam_id_hash"].isna().any()
    ):
        df = df.copy()
        df["steam_id_hash"] = df["steam_id_64"].astype(str).apply(sapi.hash_steamid)
    return df


def sanitize_one(src: Path, dst: Path) -> dict:
    df = pd.read_csv(src, dtype=str)
    rows_before = len(df)
    cols_before = list(df.columns)

    df = ensure_hash(df)

    drop_now = [c for c in DROP_COLUMNS if c in df.columns]
    df = df.drop(columns=drop_now)

    df.to_csv(dst, index=False)
    return {
        "file": src.name,
        "rows": rows_before,
        "cols_before": len(cols_before),
        "cols_after": len(df.columns),
        "dropped_cols": drop_now,
    }


def main() -> None:
    if PUB_DIR.exists():
        shutil.rmtree(PUB_DIR)
    PUB_DIR.mkdir(parents=True)
    print(f"Created clean {PUB_DIR}")

    summary = []
    for src in sorted(DATA_DIR.glob("*.csv")):
        if src.name in NEVER_PUBLISH:
            print(f"  SKIP (never publish): {src.name}")
            continue
        dst = PUB_DIR / src.name
        if src.name in PASSTHROUGH:
            shutil.copy2(src, dst)
            print(f"  COPY (passthrough): {src.name}")
            summary.append({
                "file": src.name, "rows": "n/a", "cols_before": "n/a",
                "cols_after": "n/a", "dropped_cols": [],
            })
            continue
        info = sanitize_one(src, dst)
        if info["dropped_cols"]:
            print(f"  SANITIZE: {src.name} --> dropped {info['dropped_cols']}")
        else:
            print(f"  SANITIZE: {src.name} --> no PII columns to drop")
        summary.append(info)

    # Also copy the README that explains the schemas
    if (DATA_DIR / "README.md").exists():
        shutil.copy2(DATA_DIR / "README.md", PUB_DIR / "README.md")

    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    for s in summary:
        if s["dropped_cols"]:
            print(f"  {s['file']:35s} {s['cols_before']}-->{s['cols_after']} cols, dropped: {s['dropped_cols']}")
        else:
            print(f"  {s['file']:35s} unchanged")

    print(f"\nWrote sanitized files to {PUB_DIR}")
    print("Next step: python scripts/ethics_check.py --pre-publish")


if __name__ == "__main__":
    main()
