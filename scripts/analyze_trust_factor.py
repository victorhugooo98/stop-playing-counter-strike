"""Empirical collateral analysis for the Trust Factor saturation thesis.

The thesis (in 02-vista-grossa/06-trust-factor-saturado.md):
- Reports drive Trust Factor, but reports contain a heavy noise of frustration-driven false positives
- Trust Factor is opaque, with no appeals path
- Result: honest skilled players degrade in matchmaking quality while smurfs and cheaters
  with fresh accounts retain neutral Trust Factor

What we can measure with public data:
- VAC ban distribution across the sample (the only "definitive" signal)
- Whether VAC bans correlate with Steam-side proxies that the user can SEE
  (hours, level, account age, friends, inventory)
- If there is no clean predictor of who got VAC banned, that is consistent with
  the thesis that the Valve signal is not the same as community reports

Outputs:
  assets/trust_factor_vac_predictors.csv
  assets/trust_factor_vac_distribution.png
  assets/trust_factor_summary.txt
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"
ASSETS_DIR = ROOT / "assets"
ASSETS_DIR.mkdir(exist_ok=True)


def main() -> None:
    df = pd.read_csv(DATA_DIR / "steam-profiles-analysis.csv", dtype={"steam_id_64": str})
    df = df[df["is_public"].fillna(False) & df["has_cs2"].fillna(False)].copy()
    print(f"N (public + has CS2): {len(df)}")

    df["has_vac_ban"] = (df["number_of_vac_bans"].fillna(0) > 0).astype(int)
    df["has_game_ban"] = (df["number_of_game_bans"].fillna(0) > 0).astype(int)
    df["has_any_ban"] = ((df["has_vac_ban"] + df["has_game_ban"]) > 0).astype(int)

    n_vac = int(df["has_vac_ban"].sum())
    n_game = int(df["has_game_ban"].sum())
    n_any = int(df["has_any_ban"].sum())
    print(f"VAC banned: {n_vac} ({n_vac/len(df)*100:.1f}%)")
    print(f"Game banned: {n_game} ({n_game/len(df)*100:.1f}%)")
    print(f"Any ban: {n_any} ({n_any/len(df)*100:.1f}%)")

    # Predictors we can compute from public Steam data
    predictors = [
        ("cs2_hours", "CS2 hours played"),
        ("account_age_years", "Account age (years)"),
        ("steam_level", "Steam level"),
        ("badges_count", "Badges count"),
        ("friends_count", "Friends count"),
        ("total_games_owned", "Total games owned"),
        ("total_usd", "Inventory value (USD)"),
        ("inventory_log", "log(Inventory + 1)"),
    ]

    # 1) Compare means between banned vs not-banned
    print("\n" + "=" * 60)
    print("Group means: BANNED vs CLEAN (Welch's t-test, two-sided)")
    print("=" * 60)
    rows = []
    for var, label in predictors:
        if var not in df.columns:
            continue
        a = df.loc[df["has_any_ban"] == 1, var].dropna()
        b = df.loc[df["has_any_ban"] == 0, var].dropna()
        if len(a) < 5 or len(b) < 5:
            continue
        t, p = stats.ttest_ind(a, b, equal_var=False)
        cohen_d = (a.mean() - b.mean()) / np.sqrt((a.var(ddof=1) + b.var(ddof=1)) / 2) if (a.var() + b.var()) > 0 else 0.0
        rows.append({
            "variable": var,
            "label": label,
            "n_banned": len(a),
            "n_clean": len(b),
            "mean_banned": a.mean(),
            "mean_clean": b.mean(),
            "t_stat": t,
            "p_value": p,
            "cohen_d": cohen_d,
        })
    res = pd.DataFrame(rows)
    res.to_csv(ASSETS_DIR / "trust_factor_vac_predictors.csv", index=False)
    print(res.to_string(index=False))

    # 2) Logistic regression: can we predict VAC ban from public proxies?
    feat_cols = [c for c, _ in predictors if c in df.columns]
    sub = df[feat_cols + ["has_any_ban"]].dropna()
    print(f"\nLogistic regression sample: n={len(sub)}")
    if len(sub) >= 50 and sub["has_any_ban"].sum() >= 10:
        X = sm.add_constant(sub[feat_cols])
        y = sub["has_any_ban"]
        try:
            logit = sm.Logit(y, X).fit(disp=False, maxiter=100)
            print(logit.summary().as_text()[:2200])
            mcfadden = 1 - logit.llf / logit.llnull
            print(f"\nMcFadden pseudo-R²: {mcfadden:.4f}")
            print("(values < 0.1 indicate the model has very weak predictive power)")
        except Exception as e:
            print(f"Logit failed: {e}")
            mcfadden = None
    else:
        mcfadden = None
        print("Not enough banned cases for logistic regression.")

    # 3) Visualization: violin/box of each predictor split by ban status
    feat_for_plot = [
        ("cs2_hours", "CS2 hours"),
        ("account_age_years", "Account age (years)"),
        ("steam_level", "Steam level"),
        ("badges_count", "Badges count"),
    ]
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    for ax, (col, label) in zip(axes.flatten(), feat_for_plot):
        if col not in df.columns:
            continue
        data = [
            df.loc[df["has_any_ban"] == 0, col].dropna(),
            df.loc[df["has_any_ban"] == 1, col].dropna(),
        ]
        bp = ax.boxplot(data, labels=["Clean", "Banned"], patch_artist=True)
        for patch, color in zip(bp["boxes"], ["lightgreen", "lightcoral"]):
            patch.set_facecolor(color)
        ax.set_ylabel(label)
        ax.set_title(label)
        ax.grid(axis="y", alpha=0.3)
    fig.suptitle(
        f"Public Steam metrics: banned (n={n_any}) vs clean (n={len(df)-n_any})\n"
        "If reports were reliable predictors, banned profiles would cluster at extremes",
        y=0.995,
    )
    fig.tight_layout()
    fig.savefig(ASSETS_DIR / "trust_factor_vac_distribution.png", dpi=120)
    plt.close(fig)
    print(f"\nWrote {ASSETS_DIR / 'trust_factor_vac_distribution.png'}")

    # 4) Summary
    summary = []
    summary.append("=" * 60)
    summary.append("TRUST FACTOR SATURATION — collateral evidence")
    summary.append("=" * 60)
    summary.append(f"\nN (public + CS2): {len(df)}")
    summary.append(f"VAC banned: {n_vac} ({n_vac/len(df)*100:.1f}%)")
    summary.append(f"Game banned: {n_game} ({n_game/len(df)*100:.1f}%)")
    summary.append(f"Any ban: {n_any} ({n_any/len(df)*100:.1f}%)")

    summary.append("\nGroup mean differences (banned vs clean):")
    if not res.empty:
        for _, r in res.iterrows():
            sig = " [sig]" if r["p_value"] < 0.05 else ""
            summary.append(
                f"  {r['label']:25s}  d={r['cohen_d']:+.3f}  p={r['p_value']:.4f}{sig}"
            )

    if mcfadden is not None:
        summary.append(f"\nLogistic regression McFadden pseudo-R^2: {mcfadden:.4f}")
        if mcfadden < 0.05:
            summary.append("  --> Public Steam metrics are essentially USELESS at predicting VAC bans.")
            summary.append("      Consistent with the thesis that the Valve signal is largely")
            summary.append("      orthogonal to what an honest player can see or control.")
        elif mcfadden < 0.15:
            summary.append("  --> Public metrics are weak predictors.")
        else:
            summary.append("  --> Public metrics show moderate predictive power.")

    summary.append("\nCaveat:")
    summary.append("  - VAC bans are a NARROW signal: only the 'caught' cheaters appear.")
    summary.append("  - Reports-driven Trust Factor degradation is INVISIBLE in this dataset.")
    summary.append("  - We cannot directly observe Trust Factor or report counts; this analysis")
    summary.append("    only shows that simple public proxies do not predict bans, which is")
    summary.append("    consistent with (but does not prove) saturation/noise in the report signal.")

    text = "\n".join(summary)
    print("\n" + text)
    (ASSETS_DIR / "trust_factor_summary.txt").write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
