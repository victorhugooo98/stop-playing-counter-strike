"""Statistical analysis: does inventory value correlate with performance?

Two analyses run in parallel:

1) STEAM-ONLY (large N): correlations between inventory value and Steam-side
   proxies (level, badges, friends, hours, VAC bans).
2) LEETIFY (smaller N): correlations between inventory value and real
   performance metrics (Premier rating, K/D, headshot %, etc.).

Joins the three datasets (steam-profiles-raw, inventory-values, leetify-profiles)
and runs the pre-registered analyses described in 04-manipulacao/01-hipotese-formal.md.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
from statsmodels.stats.multitest import multipletests

ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"
ASSETS_DIR = ROOT / "assets"
ASSETS_DIR.mkdir(exist_ok=True)


# ---------------------------------------------------------------------------
# Load and join
# ---------------------------------------------------------------------------
def load_joined() -> pd.DataFrame:
    profiles = pd.read_csv(DATA_DIR / "steam-profiles-raw.csv", dtype={"steam_id_64": str})
    inv_path = DATA_DIR / "inventory-values.csv"
    leet_path = DATA_DIR / "leetify-profiles.csv"

    df = profiles.copy()
    if inv_path.exists():
        inv = pd.read_csv(inv_path, dtype={"steam_id_64": str})
        df = df.merge(inv, on=["steam_id_64", "steam_id_hash"], how="left")
    if leet_path.exists():
        leet = pd.read_csv(leet_path, dtype={"steam_id_64": str})
        df = df.merge(leet, on=["steam_id_64", "steam_id_hash"], how="left", suffixes=("", "_leet"))

    df = df[df["is_public"] == True].copy()  # noqa: E712
    df = df[df["has_cs2"] == True].copy()  # noqa: E712

    df["cs2_hours"] = df["cs2_minutes_total"].fillna(0) / 60
    df["account_age_years"] = (
        (pd.Timestamp.now().timestamp() - df["time_created"].fillna(0)) / (365.25 * 24 * 3600)
    )
    df["recent_active"] = df["cs2_minutes_2weeks"].fillna(0) > 0
    df["inventory_log"] = np.log1p(df["total_usd"].fillna(0))
    df["has_inventory"] = df["total_usd"].fillna(0) > 0
    df["leetify_public"] = (df["privacy_mode"] == "public") if "privacy_mode" in df.columns else False

    return df


# ---------------------------------------------------------------------------
# Analysis A: Steam-only (large N)
# ---------------------------------------------------------------------------
STEAM_PROXIES = [
    ("cs2_hours", "CS2 hours played"),
    ("steam_level", "Steam level"),
    ("player_xp", "Player XP (Steam)"),
    ("badges_count", "Badges count"),
    ("friends_count", "Friends count"),
    ("account_age_years", "Account age (years)"),
    ("number_of_vac_bans", "VAC bans count"),
]

# Confounders for partial correlation (Steam-only model)
STEAM_CONFOUNDERS = ["cs2_hours", "account_age_years", "steam_level"]

# ---------------------------------------------------------------------------
# Analysis B: Leetify (small N)
# ---------------------------------------------------------------------------
LEETIFY_PERFORMANCE = [
    ("rank_premier", "Premier rating"),
    ("rank_leetify", "Leetify rating"),
    ("rank_faceit", "Faceit level"),
    ("winrate", "Win rate"),
    ("rating_aim", "Aim rating (Leetify)"),
    ("rating_positioning", "Positioning rating"),
    ("rating_utility", "Utility rating"),
    ("stat_accuracy_head", "Headshot %"),
    ("stat_preaim", "Preaim (lower=better)"),
    ("stat_reaction_time_ms", "Reaction time ms"),
    ("stat_spray_accuracy", "Spray accuracy"),
    ("stat_counter_strafing_good_shots_ratio", "Counter-strafing"),
]

LEETIFY_CONFOUNDERS = [
    "cs2_hours",
    "account_age_years",
    "steam_level",
    "total_matches",
]

INDEPENDENT = "inventory_log"


def descriptive_stats(df: pd.DataFrame) -> str:
    out = []
    out.append("=" * 60)
    out.append("DESCRIPTIVE STATISTICS")
    out.append("=" * 60)
    out.append(f"\nN total (public + has CS2): {len(df)}")
    if "total_usd" in df.columns:
        out.append(f"N with inventory data: {df['total_usd'].notna().sum()}")
        out.append(f"N with nonzero inventory value: {(df['total_usd'].fillna(0) > 0).sum()}")
    if "privacy_mode" in df.columns:
        out.append(f"N with Leetify public profile: {(df['privacy_mode'] == 'public').sum()}")
    if "rank_premier" in df.columns:
        out.append(f"N with Premier rank: {df['rank_premier'].notna().sum()}")

    out.append("\nKey numeric columns:")
    desc_cols = ["cs2_hours", "total_usd", "rank_premier", "rank_leetify", "winrate", "steam_level"]
    for c in desc_cols:
        if c in df.columns:
            s = df[c].dropna()
            if len(s):
                out.append(
                    f"  {c}: n={len(s)} mean={s.mean():.2f} median={s.median():.2f} std={s.std():.2f} min={s.min():.2f} max={s.max():.2f}"
                )

    out.append("\nCountry breakdown (top 10):")
    for country, n in df["country_code"].value_counts(dropna=False).head(10).items():
        out.append(f"  {country}: {n}")

    out.append(f"\nVAC bans: {df['number_of_vac_bans'].fillna(0).sum():.0f} bans across {(df['number_of_vac_bans'].fillna(0) > 0).sum()} profiles")
    out.append(f"Game bans: {df['number_of_game_bans'].fillna(0).sum():.0f} bans across {(df['number_of_game_bans'].fillna(0) > 0).sum()} profiles")

    return "\n".join(out)


def simple_correlations(df: pd.DataFrame, vars_list: list, label_prefix: str = "") -> pd.DataFrame:
    rows = []
    for var, label in vars_list:
        if var not in df.columns:
            continue
        sub = df[[INDEPENDENT, var]].dropna()
        n = len(sub)
        if n < 10:
            rows.append({"variable": var, "label": label, "n": n})
            continue
        try:
            pr, pp = stats.pearsonr(sub[INDEPENDENT], sub[var])
            sr, sp = stats.spearmanr(sub[INDEPENDENT], sub[var])
        except Exception as e:
            rows.append({"variable": var, "label": label, "n": n, "error": str(e)})
            continue
        rows.append({
            "variable": var,
            "label": label,
            "n": n,
            "pearson_r": pr,
            "pearson_p": pp,
            "spearman_r": sr,
            "spearman_p": sp,
        })
    return pd.DataFrame(rows)


def partial_correlation_via_regression(
    df: pd.DataFrame,
    vars_list: list,
    confounders: list,
) -> pd.DataFrame:
    rows = []
    for var, label in vars_list:
        if var not in df.columns:
            continue
        # Skip if var is also in confounders (no point regressing var on itself)
        active_confounders = [c for c in confounders if c != var]
        cols = [INDEPENDENT] + active_confounders + [var]
        cols = list(dict.fromkeys(cols))  # dedupe
        sub = df[cols].dropna()
        n = len(sub)
        if n < 30:
            rows.append({"variable": var, "label": label, "n": n})
            continue
        X = sm.add_constant(sub[[INDEPENDENT] + active_confounders])
        y = sub[var]
        try:
            model = sm.OLS(y, X).fit()
            coef = model.params.get(INDEPENDENT)
            pval = model.pvalues.get(INDEPENDENT)
            ci_low, ci_high = model.conf_int().loc[INDEPENDENT].tolist()
            rows.append({
                "variable": var,
                "label": label,
                "n": n,
                "coef_inventory_log": coef,
                "p_value": pval,
                "ci_low": ci_low,
                "ci_high": ci_high,
                "r2_adj": model.rsquared_adj,
            })
        except Exception as e:
            rows.append({"variable": var, "label": label, "n": n, "error": str(e)})

    out = pd.DataFrame(rows)
    valid = out["p_value"].notna() if "p_value" in out.columns else pd.Series(False)
    if valid.sum() > 0:
        pvals = out.loc[valid, "p_value"].astype(float).tolist()
        _, p_bonf, _, _ = multipletests(pvals, method="bonferroni")
        _, p_fdr, _, _ = multipletests(pvals, method="fdr_bh")
        out.loc[valid, "p_bonferroni"] = p_bonf
        out.loc[valid, "p_fdr_bh"] = p_fdr
    return out


def quartile_comparison(df: pd.DataFrame, target_var: str, target_label: str) -> str:
    sub = df[df["total_usd"].notna() & (df["total_usd"] > 0)].copy()
    if len(sub) < 20:
        return f"  Insufficient data (n<20)\n"
    if target_var not in sub.columns:
        return ""
    sub = sub[sub[target_var].notna()].copy()
    if len(sub) < 20:
        return f"  Insufficient data with {target_var} (n<20)\n"
    sub["inv_quartile"] = pd.qcut(sub["total_usd"], q=4, labels=["Q1", "Q2", "Q3", "Q4"], duplicates="drop")
    out = []
    out.append(f"  {target_label} ({target_var}):")
    means = sub.groupby("inv_quartile", observed=True)[target_var].mean()
    for q, m in means.items():
        n_q = (sub["inv_quartile"] == q).sum()
        out.append(f"    {q}: mean={m:.3f} (n={n_q})")
    q1 = sub.loc[sub["inv_quartile"] == "Q1", target_var].dropna()
    q4 = sub.loc[sub["inv_quartile"] == "Q4", target_var].dropna()
    if len(q1) >= 5 and len(q4) >= 5:
        try:
            t, p = stats.ttest_ind(q1, q4, equal_var=False)
            d = (q4.mean() - q1.mean()) / np.sqrt((q1.std() ** 2 + q4.std() ** 2) / 2)
            out.append(f"    Q1 vs Q4: t={t:.3f} p={p:.4f} cohen_d={d:.3f}")
        except Exception as e:
            out.append(f"    Q1 vs Q4: error {e}")
    return "\n".join(out)


def conclusion_from_partial(corr_df: pd.DataFrame, name: str) -> str:
    out = []
    out.append("=" * 60)
    out.append(f"DECISION: {name}")
    out.append("=" * 60)

    significant_count = 0
    sig_rows = []
    if "p_fdr_bh" in corr_df.columns:
        for _, row in corr_df.iterrows():
            if pd.notna(row.get("p_fdr_bh")) and row["p_fdr_bh"] < 0.01:
                significant_count += 1
                sig_rows.append((row["label"], row["coef_inventory_log"], row["p_fdr_bh"]))

    out.append(
        f"\nMetrics significant after FDR correction (p<0.01): "
        f"{significant_count} / {corr_df.get('p_value', pd.Series()).notna().sum() if 'p_value' in corr_df.columns else 0}"
    )
    for label, coef, p in sig_rows:
        out.append(f"  - {label}: coef={coef:.4f} p_fdr={p:.5f}")

    if significant_count >= 2:
        out.append("\n>>> ≥2 metrics significant — H1 supported in this analysis.")
    elif significant_count == 1:
        out.append("\n>>> 1 metric significant — suggestive only.")
    else:
        out.append("\n>>> No significant metrics after correction — placebo/confounders sufficient.")
    return "\n".join(out)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default=str(ASSETS_DIR))
    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(exist_ok=True)

    print("Loading data...")
    df = load_joined()
    print(f"Joined N: {len(df)}")
    out_csv = DATA_DIR / "steam-profiles-analysis.csv"
    df.to_csv(out_csv, index=False)
    print(f"Wrote {out_csv}")

    desc = descriptive_stats(df)
    print(desc)
    (out_dir / "descriptive_stats.txt").write_text(desc, encoding="utf-8")

    # ---- ANALYSIS A: Steam-only (full sample) ----
    print("\n\n" + "=" * 60)
    print("ANALYSIS A: STEAM-ONLY PROXIES (large N)")
    print("=" * 60)

    df_steam = df[df["total_usd"].fillna(0) > 0].copy()
    print(f"\nN (with inventory > 0): {len(df_steam)}")

    print("\n--- A.1 Simple correlations (inventory_log vs Steam proxy) ---")
    simple_a = simple_correlations(df_steam, STEAM_PROXIES)
    simple_a.to_csv(out_dir / "correlations_simple_steam.csv", index=False)
    print(simple_a.to_string(index=False))

    print("\n--- A.2 Partial correlations (controlling cs2_hours, age, level) ---")
    partial_a = partial_correlation_via_regression(df_steam, STEAM_PROXIES, STEAM_CONFOUNDERS)
    partial_a.to_csv(out_dir / "correlations_partial_steam.csv", index=False)
    print(partial_a.to_string(index=False))

    print(conclusion_from_partial(partial_a, "Steam-only proxies"))

    print("\n--- A.3 Quartile comparisons ---")
    qa = []
    for var, label in STEAM_PROXIES:
        qa.append(quartile_comparison(df_steam, var, label))
    qa_str = "\n".join(qa)
    print(qa_str)
    (out_dir / "quartile_steam.txt").write_text(qa_str, encoding="utf-8")

    # ---- ANALYSIS B: Leetify (smaller N, real performance) ----
    print("\n\n" + "=" * 60)
    print("ANALYSIS B: LEETIFY PERFORMANCE METRICS (smaller N)")
    print("=" * 60)

    df_leet = df[df["leetify_public"]].copy()
    print(f"\nN (Leetify public): {len(df_leet)}")
    df_leet_inv = df_leet[df_leet["total_usd"].fillna(0) > 0].copy()
    print(f"N (Leetify public + inventory > 0): {len(df_leet_inv)}")

    print("\n--- B.1 Simple correlations ---")
    simple_b = simple_correlations(df_leet_inv, LEETIFY_PERFORMANCE)
    simple_b.to_csv(out_dir / "correlations_simple_leetify.csv", index=False)
    print(simple_b.to_string(index=False))

    print("\n--- B.2 Partial correlations (controlling hours, age, level, total_matches) ---")
    partial_b = partial_correlation_via_regression(
        df_leet_inv,
        LEETIFY_PERFORMANCE,
        LEETIFY_CONFOUNDERS,
    )
    partial_b.to_csv(out_dir / "correlations_partial_leetify.csv", index=False)
    print(partial_b.to_string(index=False))

    print(conclusion_from_partial(partial_b, "Leetify performance metrics"))

    print("\n--- B.3 Quartile comparisons ---")
    qb = []
    for var, label in LEETIFY_PERFORMANCE:
        if var in df_leet_inv.columns:
            qb.append(quartile_comparison(df_leet_inv, var, label))
    qb_str = "\n".join(qb)
    print(qb_str)
    (out_dir / "quartile_leetify.txt").write_text(qb_str, encoding="utf-8")

    # ---- Summary JSON ----
    summary = {
        "n_total": int(len(df)),
        "n_with_inventory": int(df["total_usd"].notna().sum()),
        "n_with_nonzero_inventory": int((df["total_usd"].fillna(0) > 0).sum()),
        "n_leetify_public": int(df["leetify_public"].sum() if "leetify_public" in df else 0),
        "n_leetify_with_inventory": int(len(df_leet_inv)),
        "country_distribution": df["country_code"].value_counts(dropna=False).head(10).to_dict(),
        "decision_steam": "see correlations_partial_steam.csv",
        "decision_leetify": "see correlations_partial_leetify.csv",
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"\n\nDone. Outputs in {out_dir}")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
