"""Generate visualizations from data/steam-profiles-analysis.csv.

Outputs PNGs to assets/.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"
ASSETS_DIR = ROOT / "assets"
ASSETS_DIR.mkdir(exist_ok=True)

sns.set_theme(style="whitegrid", palette="deep")


def fig_inventory_distribution(df: pd.DataFrame, out: Path) -> None:
    sub = df[df["total_usd"].notna() & (df["total_usd"] > 0)]
    if len(sub) < 5:
        return
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    axes[0].hist(sub["total_usd"], bins=40, edgecolor="black")
    axes[0].set_xlabel("Inventory value (USD)")
    axes[0].set_ylabel("Profiles")
    axes[0].set_title("Inventory value distribution (linear)")
    axes[1].hist(np.log10(sub["total_usd"] + 1), bins=40, edgecolor="black", color="orange")
    axes[1].set_xlabel("log10(Inventory value + 1)")
    axes[1].set_ylabel("Profiles")
    axes[1].set_title("Inventory value distribution (log)")
    fig.suptitle(f"Counter-Strike 2 inventory values (n={len(sub)})")
    fig.tight_layout()
    fig.savefig(out, dpi=120)
    plt.close(fig)


def fig_inventory_vs_premier(df: pd.DataFrame, out: Path) -> None:
    sub = df.dropna(subset=["total_usd", "rank_premier"])
    sub = sub[sub["total_usd"] > 0]
    if len(sub) < 10:
        return
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.regplot(
        data=sub,
        x="inventory_log",
        y="rank_premier",
        ax=ax,
        scatter_kws={"alpha": 0.6, "s": 50},
        line_kws={"color": "red"},
    )
    ax.set_xlabel("log(Inventory USD + 1)")
    ax.set_ylabel("Premier rating")
    ax.set_title(f"Inventory value vs Premier rating (n={len(sub)})")
    fig.tight_layout()
    fig.savefig(out, dpi=120)
    plt.close(fig)


def fig_quartile_boxplots(df: pd.DataFrame, out: Path) -> None:
    sub = df.dropna(subset=["total_usd", "rank_premier"])
    sub = sub[sub["total_usd"] > 0]
    if len(sub) < 20:
        return
    sub = sub.copy()
    sub["inv_quartile"] = pd.qcut(
        sub["total_usd"], q=4, labels=["Q1 (low)", "Q2", "Q3", "Q4 (high)"], duplicates="drop"
    )
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    metrics = [
        ("rank_premier", "Premier rating"),
        ("rating_aim", "Leetify Aim rating"),
        ("stat_accuracy_head", "Headshot %"),
    ]
    for ax, (col, label) in zip(axes, metrics):
        if col not in sub.columns:
            continue
        sns.boxplot(data=sub, x="inv_quartile", y=col, ax=ax, hue="inv_quartile", palette="viridis", legend=False)
        ax.set_xlabel("Inventory quartile")
        ax.set_ylabel(label)
        ax.set_title(label)
    fig.suptitle("Performance metrics by inventory quartile")
    fig.tight_layout()
    fig.savefig(out, dpi=120)
    plt.close(fig)


def fig_correlation_heatmap(df: pd.DataFrame, out: Path) -> None:
    cols = [
        "inventory_log",
        "cs2_hours",
        "account_age_years",
        "steam_level",
        "rank_premier",
        "rank_leetify",
        "winrate",
        "rating_aim",
        "rating_positioning",
        "stat_accuracy_head",
        "stat_preaim",
        "stat_reaction_time_ms",
    ]
    cols = [c for c in cols if c in df.columns]
    sub = df[cols].dropna()
    if len(sub) < 10:
        return
    corr = sub.corr()
    fig, ax = plt.subplots(figsize=(11, 9))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", vmin=-1, vmax=1, center=0, ax=ax)
    ax.set_title(f"Correlation heatmap (n={len(sub)})")
    fig.tight_layout()
    fig.savefig(out, dpi=120)
    plt.close(fig)


def fig_country_breakdown(df: pd.DataFrame, out: Path) -> None:
    counts = df["country_code"].value_counts(dropna=False).head(10)
    fig, ax = plt.subplots(figsize=(8, 5))
    counts.plot(kind="bar", ax=ax, color="steelblue", edgecolor="black")
    ax.set_xlabel("Country")
    ax.set_ylabel("Profiles")
    ax.set_title(f"Sample composition by country (top 10, n={len(df)})")
    fig.tight_layout()
    fig.savefig(out, dpi=120)
    plt.close(fig)


def fig_hours_vs_inventory(df: pd.DataFrame, out: Path) -> None:
    sub = df.dropna(subset=["cs2_hours", "total_usd"])
    sub = sub[(sub["total_usd"] > 0) & (sub["cs2_hours"] > 0)]
    if len(sub) < 10:
        return
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(data=sub, x="cs2_hours", y="total_usd", alpha=0.6, s=60, ax=ax)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("CS2 hours played (log)")
    ax.set_ylabel("Inventory value USD (log)")
    ax.set_title(f"Hours vs Inventory (n={len(sub)})")
    fig.tight_layout()
    fig.savefig(out, dpi=120)
    plt.close(fig)


def fig_quartile_violin(df: pd.DataFrame, out: Path) -> None:
    sub = df.dropna(subset=["total_usd"])
    sub = sub[sub["total_usd"] > 0].copy()
    if len(sub) < 20:
        return
    sub["inv_quartile"] = pd.qcut(
        sub["total_usd"], q=4, labels=["Q1 (low)", "Q2", "Q3", "Q4 (high)"], duplicates="drop"
    )
    metrics = [
        ("cs2_hours", "CS2 hours played"),
        ("account_age_years", "Account age (years)"),
        ("friends_count", "Friends count"),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    for ax, (col, label) in zip(axes, metrics):
        if col not in sub.columns:
            continue
        sns.violinplot(
            data=sub, x="inv_quartile", y=col, ax=ax,
            hue="inv_quartile", palette="viridis", legend=False, cut=0,
        )
        ax.set_xlabel("Inventory quartile")
        ax.set_ylabel(label)
        ax.set_title(label)
    fig.suptitle("Distribution of confounders by inventory quartile")
    fig.tight_layout()
    fig.savefig(out, dpi=120)
    plt.close(fig)


def fig_inventory_vs_hours_facet(df: pd.DataFrame, out: Path) -> None:
    sub = df.dropna(subset=["total_usd", "cs2_hours"])
    sub = sub[(sub["total_usd"] > 0) & (sub["cs2_hours"] > 0)].copy()
    if len(sub) < 20:
        return
    sub["region"] = np.where(sub["country_code"] == "BR", "BR", "Other / NaN")
    sub["vac_status"] = np.where(sub["number_of_vac_bans"].fillna(0) > 0, "VAC banned", "Clean")
    g = sns.FacetGrid(sub, col="region", row="vac_status", height=4, sharex=True, sharey=True)
    g.map_dataframe(sns.scatterplot, x="cs2_hours", y="total_usd", alpha=0.6, s=40)
    for ax in g.axes.flatten():
        ax.set_xscale("log")
        ax.set_yscale("log")
    g.set_axis_labels("CS2 hours (log)", "Inventory USD (log)")
    g.fig.suptitle(f"Hours vs Inventory by region and VAC status (n={len(sub)})", y=1.03)
    g.fig.tight_layout()
    g.fig.savefig(out, dpi=120, bbox_inches="tight")
    plt.close(g.fig)


def fig_correlation_heatmap_clustered(df: pd.DataFrame, out: Path) -> None:
    cols = [
        "inventory_log",
        "cs2_hours",
        "account_age_years",
        "steam_level",
        "player_xp",
        "badges_count",
        "friends_count",
        "rank_premier",
        "rank_leetify",
        "winrate",
        "rating_aim",
        "stat_accuracy_head",
        "stat_preaim",
        "stat_reaction_time_ms",
    ]
    cols = [c for c in cols if c in df.columns]
    sub = df[cols].copy()
    # Drop columns with too many NaNs
    keep = [c for c in cols if sub[c].notna().sum() >= 30]
    sub = sub[keep].dropna()
    if len(sub) < 10:
        return
    corr = sub.corr()
    g = sns.clustermap(
        corr, annot=True, fmt=".2f", cmap="RdBu_r",
        vmin=-1, vmax=1, center=0, figsize=(11, 10),
    )
    g.fig.suptitle(f"Hierarchically clustered correlation heatmap (n={len(sub)})", y=1.02)
    g.savefig(out, dpi=120, bbox_inches="tight")
    plt.close(g.fig)


def fig_inventory_log_log(df: pd.DataFrame, out: Path) -> None:
    sub = df["total_usd"].dropna()
    sub = sub[sub > 0]
    if len(sub) < 10:
        return
    sorted_vals = np.sort(sub.values)[::-1]
    ranks = np.arange(1, len(sorted_vals) + 1)
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.loglog(ranks, sorted_vals, "o-", alpha=0.6, markersize=4)
    ax.set_xlabel("Rank (log)")
    ax.set_ylabel("Inventory USD (log)")
    ax.set_title(f"Inventory value rank distribution (log-log) — n={len(sub)}")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(out, dpi=120)
    plt.close(fig)


def fig_vac_rate_by_quartile(df: pd.DataFrame, out: Path) -> None:
    sub = df.dropna(subset=["total_usd"])
    sub = sub[sub["total_usd"] > 0].copy()
    if len(sub) < 20:
        return
    sub["inv_quartile"] = pd.qcut(
        sub["total_usd"], q=4, labels=["Q1 (low)", "Q2", "Q3", "Q4 (high)"], duplicates="drop"
    )
    sub["has_vac_ban"] = sub["number_of_vac_bans"].fillna(0) > 0
    rate = sub.groupby("inv_quartile", observed=True)["has_vac_ban"].agg(["mean", "count"])
    rate["pct"] = rate["mean"] * 100
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(rate.index.astype(str), rate["pct"], color="steelblue", edgecolor="black")
    for bar, n in zip(bars, rate["count"]):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.3,
            f"n={n}",
            ha="center", va="bottom",
        )
    ax.set_xlabel("Inventory quartile")
    ax.set_ylabel("VAC ban rate (%)")
    ax.set_title("VAC ban rate by inventory quartile")
    fig.tight_layout()
    fig.savefig(out, dpi=120)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default=str(DATA_DIR / "steam-profiles-analysis.csv"),
    )
    parser.add_argument("--output-dir", default=str(ASSETS_DIR))
    args = parser.parse_args()

    df = pd.read_csv(args.input, dtype={"steam_id_64": str})
    out_dir = Path(args.output_dir)
    out_dir.mkdir(exist_ok=True)

    print(f"Loaded {len(df)} rows.")

    figures = [
        ("inventory_distribution.png", fig_inventory_distribution),
        ("inventory_vs_premier.png", fig_inventory_vs_premier),
        ("quartile_boxplots.png", fig_quartile_boxplots),
        ("correlation_heatmap.png", fig_correlation_heatmap),
        ("country_breakdown.png", fig_country_breakdown),
        ("hours_vs_inventory.png", fig_hours_vs_inventory),
        ("inventory_quartile_violin.png", fig_quartile_violin),
        ("inventory_vs_hours_facet.png", fig_inventory_vs_hours_facet),
        ("correlation_heatmap_clustered.png", fig_correlation_heatmap_clustered),
        ("inventory_distribution_log_log.png", fig_inventory_log_log),
        ("vac_rate_by_inventory_quartile.png", fig_vac_rate_by_quartile),
    ]

    for name, fn in figures:
        path = out_dir / name
        try:
            fn(df, path)
            print(f"  OK: {path}")
        except Exception as e:
            print(f"  FAIL: {name} - {e}")

    print("\nDone.")


if __name__ == "__main__":
    main()
