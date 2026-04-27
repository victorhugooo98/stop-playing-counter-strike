"""Validate that the confounders used in analyze_correlation.py are reasonably
independent.

If they are highly collinear, the partial-correlation interpretation breaks
down. We compute:
  - Pairwise correlation matrix
  - VIF (Variance Inflation Factor) for each confounder
  - PCA to see how many components explain ≥95% of variance
  - Re-run Analysis A using PC1 + PC2 instead of raw confounders

Outputs:
  assets/confounder_correlation_matrix.csv
  assets/vif_table.csv
  assets/pca_explained_variance.png
  assets/analysis_a_pca_controls.csv
  assets/validate_proxies_summary.txt
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from statsmodels.stats.multitest import multipletests
from statsmodels.stats.outliers_influence import variance_inflation_factor

ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"
ASSETS_DIR = ROOT / "assets"
ASSETS_DIR.mkdir(exist_ok=True)

CONFOUNDERS = [
    "cs2_hours",
    "account_age_years",
    "steam_level",
    "player_xp",
    "badges_count",
    "friends_count",
]

PROXIES = [
    ("cs2_hours", "CS2 hours played"),
    ("steam_level", "Steam level"),
    ("player_xp", "Player XP (Steam)"),
    ("badges_count", "Badges count"),
    ("friends_count", "Friends count"),
    ("account_age_years", "Account age (years)"),
    ("number_of_vac_bans", "VAC bans count"),
]
INDEPENDENT = "inventory_log"


def load_df() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "steam-profiles-analysis.csv", dtype={"steam_id_64": str})
    df = df[df["total_usd"].fillna(0) > 0].copy()
    return df


def compute_correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    cols = CONFOUNDERS + [INDEPENDENT]
    sub = df[cols].dropna()
    return sub.corr()


def compute_vif(df: pd.DataFrame) -> pd.DataFrame:
    sub = df[CONFOUNDERS].dropna().copy()
    # Standardize for VIF stability
    scaler = StandardScaler()
    X = scaler.fit_transform(sub)
    rows = []
    for i, name in enumerate(CONFOUNDERS):
        try:
            vif = variance_inflation_factor(X, i)
        except Exception as e:
            vif = float("nan")
        rows.append({"variable": name, "VIF": vif})
    return pd.DataFrame(rows)


def run_pca(df: pd.DataFrame) -> tuple[PCA, np.ndarray, pd.DataFrame]:
    sub = df[CONFOUNDERS].dropna().copy()
    scaler = StandardScaler()
    X = scaler.fit_transform(sub)
    pca = PCA()
    pcs = pca.fit_transform(X)
    pc_df = pd.DataFrame(
        pcs,
        index=sub.index,
        columns=[f"PC{i+1}" for i in range(pcs.shape[1])],
    )
    return pca, X, pc_df


def regression_with_pca_controls(df: pd.DataFrame, pc_df: pd.DataFrame, n_components: int = 2) -> pd.DataFrame:
    """Re-run Analysis A controlling on principal components instead of raw confounders."""
    df = df.join(pc_df, how="left")
    pc_cols = [f"PC{i+1}" for i in range(n_components)]
    rows = []
    for var, label in PROXIES:
        if var in CONFOUNDERS:
            # Skip dependent vars that are themselves confounders
            continue
        if var not in df.columns:
            continue
        cols = [INDEPENDENT] + pc_cols + [var]
        sub = df[cols].dropna()
        n = len(sub)
        if n < 30:
            rows.append({"variable": var, "label": label, "n": n})
            continue
        X = sm.add_constant(sub[[INDEPENDENT] + pc_cols])
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


def plot_pca_explained(pca: PCA, out: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    cumvar = np.cumsum(pca.explained_variance_ratio_)
    indiv = pca.explained_variance_ratio_
    x = np.arange(1, len(indiv) + 1)
    ax.bar(x, indiv, alpha=0.6, label="Individual")
    ax.plot(x, cumvar, "ro-", label="Cumulative")
    ax.axhline(0.95, linestyle="--", color="gray", alpha=0.5, label="95% threshold")
    ax.set_xlabel("Principal Component")
    ax.set_ylabel("Explained variance ratio")
    ax.set_title("PCA — explained variance of confounders")
    ax.set_xticks(x)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out, dpi=120)
    plt.close(fig)


def main() -> None:
    print("Loading data...")
    df = load_df()
    print(f"N (with inventory > 0): {len(df)}")

    print("\n[1/4] Correlation matrix among confounders...")
    corr = compute_correlation_matrix(df)
    corr.to_csv(ASSETS_DIR / "confounder_correlation_matrix.csv")
    print(corr.to_string())

    print("\n[2/4] VIF (Variance Inflation Factor)...")
    vif = compute_vif(df)
    vif.to_csv(ASSETS_DIR / "vif_table.csv", index=False)
    print(vif.to_string(index=False))

    print("\n[3/4] PCA of confounders...")
    pca, X, pc_df = run_pca(df)
    print("Explained variance ratio:", np.round(pca.explained_variance_ratio_, 3))
    print("Cumulative:", np.round(np.cumsum(pca.explained_variance_ratio_), 3))
    print("Loadings (top components):")
    loadings = pd.DataFrame(
        pca.components_.T,
        columns=[f"PC{i+1}" for i in range(len(pca.components_))],
        index=CONFOUNDERS,
    )
    print(loadings.to_string())
    loadings.to_csv(ASSETS_DIR / "pca_loadings.csv")
    plot_pca_explained(pca, ASSETS_DIR / "pca_explained_variance.png")

    n_for_95 = int(np.searchsorted(np.cumsum(pca.explained_variance_ratio_), 0.95) + 1)
    print(f"\nComponents to reach 95%: {n_for_95}")

    print(f"\n[4/4] Analysis A re-run controlling for PC1+PC2...")
    pca_results = regression_with_pca_controls(df, pc_df, n_components=2)
    pca_results.to_csv(ASSETS_DIR / "analysis_a_pca_controls.csv", index=False)
    print(pca_results.to_string(index=False))

    # Summary
    summary_lines = []
    summary_lines.append("=" * 60)
    summary_lines.append("VALIDATE PROXIES — SUMMARY")
    summary_lines.append("=" * 60)
    summary_lines.append(f"\nN (with inventory > 0): {len(df)}")

    summary_lines.append(f"\nVIF (>10 = severe multicollinearity):")
    for _, row in vif.iterrows():
        flag = " [!]" if row["VIF"] > 10 else ""
        summary_lines.append(f"  {row['variable']:25s}: {row['VIF']:.2f}{flag}")

    max_vif = vif["VIF"].max()
    summary_lines.append(f"\nMax VIF: {max_vif:.2f}")
    if max_vif > 10:
        summary_lines.append("  [!] SEVERE MULTICOLLINEARITY detected — partial-correlation interpretation in Analysis A may be unstable.")
    elif max_vif > 5:
        summary_lines.append("  [!] MODERATE multicollinearity — interpret with care.")
    else:
        summary_lines.append("  [OK] Confounders are reasonably independent.")

    summary_lines.append(f"\nPCA: {n_for_95} component(s) explain ≥95% of variance.")
    if n_for_95 == 1:
        summary_lines.append("  [!] Confounders are essentially the same dimension — controlling for one effectively controls for all.")
    elif n_for_95 == 2:
        summary_lines.append("  [OK] Two independent dimensions in confounders.")
    else:
        summary_lines.append(f"  [OK] {n_for_95} independent dimensions — robust set of controls.")

    if "p_fdr_bh" in pca_results.columns:
        sig_n = (pca_results["p_fdr_bh"].fillna(1) < 0.01).sum()
        summary_lines.append(f"\nAnalysis A re-run with PCA controls: {sig_n} metrics significant after FDR.")

    summary_lines.append("\n" + "=" * 60)

    summary = "\n".join(summary_lines)
    (ASSETS_DIR / "validate_proxies_summary.txt").write_text(summary, encoding="utf-8")
    # print without emojis for Windows console safety
    safe = summary.encode("ascii", errors="replace").decode("ascii")
    print("\n" + safe)
    print(f"\nWrote outputs to {ASSETS_DIR}/")


if __name__ == "__main__":
    main()
