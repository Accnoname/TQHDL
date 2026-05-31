"""
step_03_bivariate.py — Phân tích song biến: Các mối quan hệ với Lương và Rủi ro
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
from src.data.load_data import load

OUTPUT_DIR = PROJECT_ROOT / "reports" / "figures"
OUTPUT_1 = OUTPUT_DIR / "output_step_03_bivariate_1.png"
OUTPUT_2 = OUTPUT_DIR / "output_step_03_bivariate_2.png"
OUTPUT_3 = OUTPUT_DIR / "output_step_03_bivariate_3.png"


def _save_fig(fig: plt.Figure, output_path: Path) -> None:
    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved -> {output_path}")

def _fmt_usd(x, _):
    return f"${int(x):,}"

def main():
    df = load()

    # 1. Lương trung vị theo cấp độ
    fig, ax = plt.subplots(figsize=(10, 6))
    seniority_order = ["Junior", "Mid", "Senior", "Lead", "Executive"]
    salary_seniority = df.groupby("seniority_level", observed=False)["salary_usd"].median().reindex(seniority_order)
    colors = ["#BBDEFB", "#90CAF9", "#64B5F6", "#42A5F5", "#1E88E5"]
    bars = ax.bar(salary_seniority.index, salary_seniority.values, color=colors, edgecolor="white", linewidth=0.8)
    ax.set_title("Lương Trung Vị Theo Cấp Độ")
    ax.set_ylabel("Lương (USD)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(_fmt_usd))
    for bar, val in zip(bars, salary_seniority.values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 200, f"${val:,.0f}",
                ha="center", va="bottom", fontsize=8, fontweight="bold")
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    _save_fig(fig, OUTPUT_1)

    # 2. Top 10 ngành có lương cao nhất
    fig, ax = plt.subplots(figsize=(10, 6))
    top_salary_industry = df.groupby("industry")["salary_usd"].median().sort_values().tail(10)
    gradient = plt.cm.Blues([0.4 + 0.06 * i for i in range(10)])
    bars = ax.barh(top_salary_industry.index, top_salary_industry.values, color=gradient, edgecolor="white")
    ax.set_title("Top 10 Ngành Có Lương Trung Vị Cao Nhất")
    ax.set_xlabel("Lương trung vị (USD)")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(_fmt_usd))
    for bar, val in zip(bars, top_salary_industry.values):
        ax.text(bar.get_width() + 200, bar.get_y() + bar.get_height() / 2, f"${val:,.0f}",
                va="center", fontsize=8)
    _save_fig(fig, OUTPUT_2)

    # 3. Rủi ro tự động hóa trung vị theo ngành
    fig, ax = plt.subplots(figsize=(12, 10))
    risk_by_industry = df.groupby("industry")["automation_risk_score"].median().sort_values()
    c_map = plt.cm.RdYlGn_r(np.linspace(0.1, 0.9, len(risk_by_industry)))
    bars2 = ax.barh(risk_by_industry.index, risk_by_industry.values, color=c_map, edgecolor="white")
    ax.set_title("Rủi Ro Tự Động Hóa Trung Vị Theo Ngành")
    ax.set_xlabel("Automation Risk Score")
    ax.axvline(0.5, color="gray", linestyle="--", alpha=0.6)
    for bar, val in zip(bars2, risk_by_industry.values):
        ax.text(val + 0.005, bar.get_y() + bar.get_height() / 2, f"{val:.2f}",
                va="center", fontsize=8)
    _save_fig(fig, OUTPUT_3)

if __name__ == "__main__":
    main()
