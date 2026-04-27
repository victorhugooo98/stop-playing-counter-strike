"""PII / publication-readiness audit for the dossiê dataset.

Run before any commit that touches data/. Detects:
- Plain SteamID 64 alongside steam_id_hash (working files OK; published files = block)
- Persona names, real names, avatar URLs in CSVs
- Friends list with both src+dst as plain SteamID 64s (instead of hashes)
- .env or any *.key file outside .gitignore

Severity model:
- WARN: working files. Plain SteamID is expected here for analysis.
- BLOCK: anything that makes the repo unsafe to make public AS IS.

Usage:
    python scripts/ethics_check.py                # working-tree audit (warns on plain ID)
    python scripts/ethics_check.py --strict       # treat all PII findings as BLOCK
    python scripts/ethics_check.py --pre-publish  # audit *-public.csv and assert publish-safe
    python scripts/ethics_check.py --fix-edges    # generate friends-edges-hashed.csv
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

# Files that must NEVER be published with plain SteamIDs / PII
SENSITIVE = {
    "friends-edges.csv",
}

# Files we treat as analysis working copies; plain SteamID warns but does not block
WORKING_COPIES_WITH_PLAIN_ID = {
    "inventories.csv",
    "inventory-values.csv",
    "leetify-profiles.csv",
    "steam-profiles-raw.csv",
    "steam-profiles-analysis.csv",
    "seed-profiles.csv",
}

# Files expected to be safe to publish (no plain ID present)
PUBLISHABLE = {
    "lawsuits.csv",
    "revenue-timeline.csv",
    "botfarm-services.csv",
    "market-prices.csv",
    "network-metrics.csv",
    "friends-edges-hashed.csv",
}

PII_COLUMNS = {"persona_name", "personaname", "name", "real_name", "avatar", "avatar_url"}
HASHED_ID_COL = "steam_id_hash"
PLAIN_ID_COL = "steam_id_64"

ENV_PATTERN = re.compile(r"\.env(\..+)?$")
KEY_PATTERN = re.compile(r"\.(key|pem|p12)$")


class Findings:
    """Collects findings categorized as BLOCK or WARN."""
    def __init__(self) -> None:
        self.blocks: list[str] = []
        self.warns: list[str] = []

    def block(self, msg: str) -> None:
        self.blocks.append(msg)

    def warn(self, msg: str) -> None:
        self.warns.append(msg)


def check_pii_columns(df: pd.DataFrame, name: str, findings: Findings) -> None:
    for col in df.columns:
        if col.lower() in PII_COLUMNS and not (df[col].fillna("") == "").all():
            findings.block(f"{name}: column '{col}' contains non-empty PII data")


def check_anonymization(
    df: pd.DataFrame,
    name: str,
    findings: Findings,
    *,
    strict: bool,
    is_published_view: bool,
) -> None:
    has_plain = PLAIN_ID_COL in df.columns
    has_hash = HASHED_ID_COL in df.columns

    if not has_plain:
        return  # no plain SteamID column at all → nothing to flag

    msg = (
        f"{name}: contains '{PLAIN_ID_COL}' column "
        f"({len(df)} rows){' [also has hash]' if has_hash else ''}"
    )

    if is_published_view:
        # If we are auditing a *-public.csv file, plain SteamID = hard block
        findings.block(msg + " — published views must not contain plain SteamID")
    elif strict:
        findings.block(msg + " — strict mode")
    elif name in WORKING_COPIES_WITH_PLAIN_ID:
        findings.warn(
            msg + " — expected in working copy; sanitize before public publication"
        )
    else:
        # Unknown file with plain ID → block (might be a published file we forgot to classify)
        findings.block(
            msg + " — file not in WORKING_COPIES_WITH_PLAIN_ID; classify or sanitize"
        )


def check_friends_edges(path: Path, findings: Findings) -> None:
    if not path.exists():
        return
    df = pd.read_csv(path, dtype=str)
    if "src_steam_id" in df.columns:
        bad_prefixes = ~df["src_steam_id"].astype(str).str.startswith(("76561",))
        if bad_prefixes.any():
            findings.block(f"{path.name}: src column has non-SteamID values")
        findings.warn(
            f"{path.name}: contains plain SteamIDs (src+dst) "
            "— expected; ensure file is in .gitignore. Run --fix-edges to publish hashed."
        )


def check_env_files(findings: Findings) -> None:
    gitignore = ROOT / ".gitignore"
    ignored = gitignore.read_text(encoding="utf-8") if gitignore.exists() else ""
    for p in ROOT.iterdir():
        if p.is_file() and ENV_PATTERN.search(p.name) and p.name != ".env.example":
            if ".env" not in ignored:
                findings.block(f"{p.name} not in .gitignore — credentials at risk")
        if p.is_file() and KEY_PATTERN.search(p.name):
            findings.block(f"{p.name}: keyfile present at repo root")


def fix_friends_edges() -> None:
    """Generate friends-edges-hashed.csv from friends-edges.csv."""
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
    df[["src_steam_id_hash", "dst_steam_id_hash", "friend_since"]].to_csv(out, index=False)
    print(f"Wrote {out}")


def audit_directory(target: Path, *, strict: bool, is_published_view: bool) -> Findings:
    findings = Findings()
    if not target.exists():
        print(f"Target directory not found: {target}")
        return findings

    check_env_files(findings)

    csvs = sorted(target.glob("*.csv"))
    if not csvs:
        print(f"No CSVs found in {target}")
        return findings

    for csv_path in csvs:
        try:
            df = pd.read_csv(csv_path, dtype=str)
        except Exception as e:
            findings.warn(f"could not read {csv_path.name}: {e}")
            continue
        print(f"\n[{csv_path.name}] rows={len(df)} cols={len(df.columns)}")
        cols_preview = list(df.columns)[:10]
        suffix = "..." if len(df.columns) > 10 else ""
        print(f"  columns: {cols_preview}{suffix}")

        check_pii_columns(df, csv_path.name, findings)
        check_anonymization(
            df, csv_path.name, findings,
            strict=strict, is_published_view=is_published_view,
        )

        if csv_path.name in SENSITIVE:
            check_friends_edges(csv_path, findings)

    return findings


def report(findings: Findings, *, strict_or_publish: bool) -> int:
    print("\n" + "=" * 60)
    print(f"Findings: {len(findings.blocks)} BLOCK, {len(findings.warns)} WARN")
    print("=" * 60)
    if findings.blocks:
        print("\nBLOCK (must fix before publication):")
        for issue in findings.blocks:
            print(f"  - {issue}")
    if findings.warns:
        print("\nWARN (informational; expected in working copy):")
        for issue in findings.warns:
            print(f"  - {issue}")
    if not findings.blocks and not findings.warns:
        print("\nOK — no issues found")

    if findings.blocks:
        return 1
    if strict_or_publish and findings.warns:
        # In strict mode, even warns become blockers
        return 1
    return 0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fix-edges", action="store_true",
                        help="Regenerate friends-edges-hashed.csv from friends-edges.csv")
    parser.add_argument("--strict", action="store_true",
                        help="Treat all PII findings (including expected plain IDs in working copies) as BLOCK")
    parser.add_argument("--pre-publish", action="store_true",
                        help="Audit data/published/ (created by sanitize_for_publication.py) "
                             "as if it were the public release")
    args = parser.parse_args()

    if args.fix_edges:
        fix_friends_edges()
        return

    if args.pre_publish:
        target = DATA_DIR / "published"
        print("=" * 60)
        print(f"Pre-publish audit on {target}")
        print("=" * 60)
        findings = audit_directory(target, strict=False, is_published_view=True)
    else:
        target = DATA_DIR
        title = "STRICT mode" if args.strict else "working-tree mode"
        print("=" * 60)
        print(f"Ethics check — auditing {target} ({title})")
        print("=" * 60)
        findings = audit_directory(target, strict=args.strict, is_published_view=False)

    code = report(findings, strict_or_publish=args.strict or args.pre_publish)
    sys.exit(code)


if __name__ == "__main__":
    main()
