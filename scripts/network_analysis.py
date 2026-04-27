"""Social network analysis of the Steam friends graph.

Reads:  data/friends-edges-hashed.csv  (hashed src/dst SteamIDs)
        data/steam-profiles-analysis.csv  (per-profile metrics)
Writes: data/network-metrics.csv          (per-profile network metrics)
        assets/network-graph.png          (visualization)
        assets/network-degree-vs-inventory.png
        assets/network-clustering-distribution.png
        assets/network-summary.txt

Question: do players with high inventory cluster together? Are they
more central in the friends graph than expected by chance?
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from scipy import stats

import steam_api as sapi

ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"
ASSETS_DIR = ROOT / "assets"
ASSETS_DIR.mkdir(exist_ok=True)


def load_graph_and_profiles() -> tuple[nx.Graph, pd.DataFrame]:
    edges = pd.read_csv(DATA_DIR / "friends-edges-hashed.csv")
    profiles = pd.read_csv(DATA_DIR / "steam-profiles-analysis.csv", dtype={"steam_id_64": str})

    # Add hashes if missing
    if "steam_id_hash" not in profiles.columns or profiles["steam_id_hash"].isna().any():
        profiles["steam_id_hash"] = profiles["steam_id_64"].apply(sapi.hash_steamid)

    G = nx.Graph()
    # Add nodes for all profiles in the sample
    for _, row in profiles.iterrows():
        h = row["steam_id_hash"]
        G.add_node(
            h,
            inventory_log=row.get("inventory_log", 0.0) or 0.0,
            cs2_hours=row.get("cs2_hours", 0) or 0,
            country=row.get("country_code", ""),
            is_public=bool(row.get("is_public", False)),
            has_cs2=bool(row.get("has_cs2", False)),
            in_sample=True,
        )

    # Add edges (only those between sample nodes are kept; outsiders dropped)
    sample_nodes = set(G.nodes())
    for _, e in edges.iterrows():
        a, b = e["src_steam_id_hash"], e["dst_steam_id_hash"]
        if a in sample_nodes and b in sample_nodes:
            G.add_edge(a, b)

    return G, profiles


def compute_network_metrics(G: nx.Graph, profiles: pd.DataFrame) -> pd.DataFrame:
    print(f"Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    print(f"Density: {nx.density(G):.5f}")
    components = list(nx.connected_components(G))
    components.sort(key=len, reverse=True)
    print(f"Connected components: {len(components)}")
    print(f"Largest component size: {len(components[0])}")

    deg = dict(G.degree())
    clustering = nx.clustering(G)

    largest = G.subgraph(components[0]).copy()
    print(f"\nComputing betweenness on largest component (n={largest.number_of_nodes()}). This may take a while...")
    if largest.number_of_nodes() <= 2500:
        between = nx.betweenness_centrality(largest, k=min(500, largest.number_of_nodes()))
    else:
        between = {n: float("nan") for n in largest.nodes()}

    rows = []
    for h, attrs in G.nodes(data=True):
        rows.append({
            "steam_id_hash": h,
            "degree": deg.get(h, 0),
            "clustering": clustering.get(h, 0.0),
            "betweenness": between.get(h, float("nan")),
            "in_largest_component": h in largest.nodes(),
            "inventory_log": attrs.get("inventory_log", 0.0),
            "cs2_hours": attrs.get("cs2_hours", 0),
            "country": attrs.get("country", ""),
        })
    return pd.DataFrame(rows)


def plot_graph(G: nx.Graph, out: Path) -> None:
    components = sorted(nx.connected_components(G), key=len, reverse=True)
    largest = G.subgraph(components[0]).copy()
    print(f"Drawing largest component: {largest.number_of_nodes()} nodes")

    fig, ax = plt.subplots(figsize=(12, 12))
    pos = nx.spring_layout(largest, k=0.4, iterations=80, seed=42)

    # Color by inventory_log
    inv = np.array([largest.nodes[n].get("inventory_log", 0) for n in largest.nodes()])

    nx.draw_networkx_edges(largest, pos, alpha=0.15, width=0.4, ax=ax)
    nodes = nx.draw_networkx_nodes(
        largest,
        pos,
        node_size=20 + 8 * inv,
        node_color=inv,
        cmap="viridis",
        alpha=0.85,
        ax=ax,
    )
    plt.colorbar(nodes, ax=ax, label="log(Inventory USD + 1)")
    ax.set_title(
        f"Friends graph — largest connected component ({largest.number_of_nodes()} nodes, "
        f"{largest.number_of_edges()} edges)\nNode size and color: log(inventory value)"
    )
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(out, dpi=140)
    plt.close(fig)


def plot_degree_vs_inventory(metrics: pd.DataFrame, out: Path) -> None:
    sub = metrics[metrics["inventory_log"] > 0].copy()
    if len(sub) < 10:
        return
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(sub["degree"], sub["inventory_log"], alpha=0.5, s=30)
    ax.set_xlabel("Degree (number of friends in sample)")
    ax.set_ylabel("log(Inventory USD + 1)")
    ax.set_title(f"Friends in sample vs Inventory value (n={len(sub)})")
    fig.tight_layout()
    fig.savefig(out, dpi=120)
    plt.close(fig)


def plot_clustering_distribution(metrics: pd.DataFrame, out: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(metrics["clustering"].dropna(), bins=30, edgecolor="black", alpha=0.7)
    ax.set_xlabel("Local clustering coefficient")
    ax.set_ylabel("Frequency")
    ax.set_title("Distribution of clustering coefficient across nodes")
    fig.tight_layout()
    fig.savefig(out, dpi=120)
    plt.close(fig)


def correlate_inventory_centrality(metrics: pd.DataFrame) -> str:
    out = []
    out.append("=" * 60)
    out.append("CORRELATIONS: inventory_log vs network metrics")
    out.append("=" * 60)
    sub = metrics[metrics["inventory_log"] > 0]
    if len(sub) < 10:
        return "  Insufficient data for correlations"

    for col in ["degree", "clustering", "betweenness"]:
        s = sub[[col, "inventory_log"]].dropna()
        if len(s) < 10:
            out.append(f"  {col}: insufficient data (n={len(s)})")
            continue
        r, p = stats.spearmanr(s[col], s["inventory_log"])
        rp, pp = stats.pearsonr(s[col], s["inventory_log"])
        out.append(
            f"  {col}: n={len(s)} | spearman r={r:.3f} (p={p:.4f}) | pearson r={rp:.3f} (p={pp:.4f})"
        )
    return "\n".join(out)


def main() -> None:
    print("Loading graph and profiles...")
    G, profiles = load_graph_and_profiles()
    print(f"\nNodes: {G.number_of_nodes()} | Edges: {G.number_of_edges()}")

    metrics = compute_network_metrics(G, profiles)
    metrics_out = DATA_DIR / "network-metrics.csv"
    metrics.to_csv(metrics_out, index=False)
    print(f"\nWrote {metrics_out}")

    plot_graph(G, ASSETS_DIR / "network-graph.png")
    print("  OK: network-graph.png")
    plot_degree_vs_inventory(metrics, ASSETS_DIR / "network-degree-vs-inventory.png")
    print("  OK: network-degree-vs-inventory.png")
    plot_clustering_distribution(metrics, ASSETS_DIR / "network-clustering-distribution.png")
    print("  OK: network-clustering-distribution.png")

    corr_text = correlate_inventory_centrality(metrics)
    print("\n" + corr_text)

    summary_lines = []
    summary_lines.append("=" * 60)
    summary_lines.append("NETWORK ANALYSIS SUMMARY")
    summary_lines.append("=" * 60)
    summary_lines.append(f"\nNodes: {G.number_of_nodes()}")
    summary_lines.append(f"Edges: {G.number_of_edges()}")
    summary_lines.append(f"Density: {nx.density(G):.5f}")
    components = list(nx.connected_components(G))
    components.sort(key=len, reverse=True)
    summary_lines.append(f"Connected components: {len(components)}")
    summary_lines.append(f"Largest component: {len(components[0])} nodes")
    summary_lines.append(f"Mean degree: {metrics['degree'].mean():.2f}")
    summary_lines.append(f"Median clustering: {metrics['clustering'].median():.3f}")
    summary_lines.append("")
    summary_lines.append(corr_text)

    summary = "\n".join(summary_lines)
    (ASSETS_DIR / "network-summary.txt").write_text(summary, encoding="utf-8")
    print(f"\nDone. Outputs in {ASSETS_DIR}/")


if __name__ == "__main__":
    main()
