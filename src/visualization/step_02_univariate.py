"""
step_02_univariate.py — Phân tích đơn biến: Cường độ AI, Rủi ro tự động hóa, Mức lương, Giai đoạn áp dụng
"""
import sys
from pathlib import Path
from typing import Tuple, List

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
from src.data.load_data import load

OUTPUT_DIR = PROJECT_ROOT / "reports" / "figures"
OUTPUT_1 = OUTPUT_DIR / "output_step_02_univariate_1.png"
OUTPUT_2 = OUTPUT_DIR / "output_step_02_univariate_2.png"
OUTPUT_3 = OUTPUT_DIR / "output_step_02_univariate_3.png"
OUTPUT_4 = OUTPUT_DIR / "output_step_02_univariate_4.png"


def _save_fig(fig: plt.Figure, output_path: Path) -> None:
    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved -> {output_path}")

def _qcut_counts(series: pd.Series, q: int) -> Tuple[List[str], np.ndarray]:
    cleaned = series.dropna()
    if cleaned.empty:
        return [], np.array([])
    bins = pd.qcut(cleaned, q=q, duplicates="drop")
    counts = bins.value_counts().sort_index()
    labels = [f"{interval.left:.2f}-{interval.right:.2f}" for interval in counts.index]
    return labels, counts.values

def _fmt_usd(x: float, _pos: int) -> str:
    return f"${int(x):,}"

def main():
    df = load()

    # 1. Cường độ AI (Pie)
    fig, ax = plt.subplots(figsize=(8, 6))
    ai_labels, ai_values = _qcut_counts(df["ai_intensity_score"], 4)
    ai_colors = ["#FCE4EC", "#F8BBD0", "#F06292", "#D81B60"][:len(ai_values)]
    ax.pie(
        ai_values,
        labels=ai_labels,
        colors=ai_colors,
        autopct=lambda pct: f"{pct:.1f}%" if pct > 0 else "",
        startangle=90,
        counterclock=False,
        wedgeprops={"edgecolor": "white", "linewidth": 1},
        textprops={"fontsize": 8},
    )
    ax.set_title("Phân Bổ Cường Độ AI")
    ax.axis("equal")
    _save_fig(fig, OUTPUT_1)

    # 2. Phân bố điểm rủi ro tự động hóa (Histogram)
    fig, ax = plt.subplots(figsize=(10, 6))
    risk_data = df["automation_risk_score"].dropna()
    if not risk_data.empty:
        ax.hist(risk_data, bins=30, color="#FFA726", edgecolor="white", alpha=0.9)
        mean_val = risk_data.mean()
        median_val = risk_data.median()
        ax.axvline(mean_val, color="#B71C1C", linestyle="--", linewidth=2, label="Trung bình")
        ax.axvline(median_val, color="#4C72B0", linestyle="-", linewidth=2, label="Trung vị")
        ax.legend(frameon=False, fontsize=9)
    else:
        ax.text(0.5, 0.5, "Không có dữ liệu rủi ro", ha="center", va="center")
        ax.set_axis_off()
    ax.set_title("Phân Bố Điểm Rủi Ro Tự Động Hóa")
    ax.set_xlabel("Điểm rủi ro tự động hóa")
    ax.set_ylabel("Số lượng")
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    _save_fig(fig, OUTPUT_2)

    # 3. Giai đoạn áp dụng AI theo ngành (Cột chồng)
    fig, ax = plt.subplots(figsize=(10, 7))
    stage_counts = df.groupby(["industry", "industry_ai_adoption_stage"], observed=True).size().unstack(fill_value=0)
    stage_counts = stage_counts.sort_values("Mature", ascending=False).head(12)
    stage_colors = {"Emerging": "#FFCC80", "Growing": "#64B5F6", "Mature": "#81C784"}
    bottom = pd.Series([0] * len(stage_counts), index=stage_counts.index, dtype=float)
    for stage in ["Emerging", "Growing", "Mature"]:
        if stage in stage_counts.columns:
            ax.barh(stage_counts.index[::-1], stage_counts[stage][::-1],
                    left=bottom[::-1].values, color=stage_colors[stage], label=stage)
            bottom += stage_counts[stage]
    ax.set_title("Giai Đoạn Áp Dụng AI Theo Ngành")
    ax.set_xlabel("Số lượng")
    ax.legend(title="Giai đoạn", loc="lower right")
    _save_fig(fig, OUTPUT_3)

    # 4. Phân bổ mức lương (Box + Sample)
    fig, ax = plt.subplots(figsize=(10, 6))
    salary = df["salary_usd"].dropna()
    sample = salary.sample(n=min(400, len(salary)), random_state=7)
    rng = np.random.default_rng(7)
    y_jitter = 1 + rng.uniform(-0.07, 0.07, size=len(sample))
    ax.scatter(sample, y_jitter, s=12, color="#90CAF9", alpha=0.35, edgecolors="none")
    ax.boxplot(
        salary,
        vert=False,
        patch_artist=True,
        showfliers=False,
        boxprops=dict(facecolor="#4C72B0", color="white", linewidth=1),
        medianprops=dict(color="white", linewidth=2),
        whiskerprops=dict(color="#4C72B0"),
        capprops=dict(color="#4C72B0"),
    )
    ax.set_title("Phân Bố Mức Lương Tổng Quan")
    ax.set_xlabel("Lương (USD)")
    ax.set_yticks([])
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(_fmt_usd))
    ax.grid(axis="x", linestyle="--", alpha=0.4)
    _save_fig(fig, OUTPUT_4)

if __name__ == "__main__":
    main()
