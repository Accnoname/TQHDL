"""
step_01_overview.py — Khám phá dữ liệu: Xu hướng theo năm, Ngành, Quốc gia, Cấp độ
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
OUTPUT_1 = OUTPUT_DIR / "output_step_01_overview_1.png"
OUTPUT_2 = OUTPUT_DIR / "output_step_01_overview_2.png"
OUTPUT_3 = OUTPUT_DIR / "output_step_01_overview_3.png"
OUTPUT_4 = OUTPUT_DIR / "output_step_01_overview_4.png"
ACCENT = "#1E66B5"
BLUE_SCALE = ["#11C3EB", "#126920", "#B51EA1", "#2E2ED2", "#E64D4D"]


def _save_fig(fig: plt.Figure, output_path: Path) -> None:
    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved -> {output_path}")

def main():
    df = load()

    # 1. Số tin đăng theo năm
    fig, ax = plt.subplots(figsize=(10, 6))
    by_year = df.groupby("posting_year").size().sort_index()
    ax.plot(
        by_year.index,
        by_year.values,
        color=ACCENT,
        marker="o",
        linewidth=2.2,
        markersize=5,
    )
    ax.set_title("Số Tin Đăng Theo Năm")
    ax.set_xlabel("Năm")
    ax.set_ylabel("Số lượng")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    label_offset = max(by_year.values) * 0.02
    for year, val in by_year.items():
        ax.text(year, val + label_offset, str(val), ha="center", va="bottom", fontsize=7)
    _save_fig(fig, OUTPUT_1)

    # 2. Top 10 ngành nghề
    fig, ax = plt.subplots(figsize=(10, 6))
    top_industry = df["industry"].value_counts().head(10)
    colors = plt.cm.Blues(np.linspace(0.35, 0.95, 10))[::-1]
    bars = ax.barh(top_industry.index[::-1], top_industry.values[::-1], color=colors)
    ax.set_title("Top 10 Ngành Nghề")
    ax.set_xlabel("Số lượng")
    for bar, val in zip(bars, top_industry.values[::-1]):
        ax.text(bar.get_width() + 5, bar.get_y() + bar.get_height() / 2, str(val),
                va="center", fontsize=8)
    _save_fig(fig, OUTPUT_2)

    # 3. Top 15 quốc gia
    fig, ax = plt.subplots(figsize=(10, 7))
    top_country = df["country"].value_counts().head(15)
    country_colors = plt.cm.Blues(np.linspace(0.35, 0.95, len(top_country)))[::-1]
    ax.barh(top_country.index[::-1], top_country.values[::-1], color=country_colors, edgecolor="white")
    ax.set_title("Top 15 Quốc Gia")
    ax.set_xlabel("Số lượng")
    _save_fig(fig, OUTPUT_3)

    # 4. Cấp độ kinh nghiệm theo khu vực (100% stacked)
    fig, ax = plt.subplots(figsize=(10, 7))
    seniority_order = ["Junior", "Mid", "Senior", "Lead", "Executive"]
    palette = BLUE_SCALE
    region_order = df["region"].value_counts().index
    region_seniority = pd.crosstab(df["region"], df["seniority_level"])
    region_seniority = region_seniority.reindex(index=region_order, columns=seniority_order, fill_value=0)
    region_pct = region_seniority.div(region_seniority.sum(axis=1), axis=0).mul(100)
    region_pct = region_pct.iloc[::-1]

    left = np.zeros(len(region_pct))
    for level, color in zip(seniority_order, palette):
        values = region_pct[level].values
        ax.barh(region_pct.index, values, left=left, color=color, edgecolor="white", linewidth=0.5, label=level)
        left += values

    ax.set_title("Cấp Độ Kinh Nghiệm Theo Khu Vực")
    ax.set_xlabel("Tỷ lệ (%)")
    ax.xaxis.set_major_formatter(mticker.PercentFormatter())
    ax.legend(title="Cấp độ", ncol=3, fontsize=8, title_fontsize=8, frameon=False, loc="lower right")
    _save_fig(fig, OUTPUT_4)

if __name__ == "__main__":
    main()
