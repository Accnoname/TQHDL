"""
step_04_trends.py — Phân tích chuỗi thời gian: Xu hướng qua các năm
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
from src.data.load_data import load

OUTPUT_DIR = PROJECT_ROOT / "reports" / "figures"
OUTPUT_1 = OUTPUT_DIR / "output_step_04_trends_1.png"
OUTPUT_2 = OUTPUT_DIR / "output_step_04_trends_2.png"
OUTPUT_3 = OUTPUT_DIR / "output_step_04_trends_3.png"
OUTPUT_4 = OUTPUT_DIR / "output_step_04_trends_4.png"


def _save_fig(fig: plt.Figure, output_path: Path) -> None:
    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved -> {output_path}")

def _fmt_usd(x, _):
    return f"${int(x):,}"

def main():
    df = load()

    # 1. % Tin đăng đề cập AI theo năm
    fig, ax = plt.subplots(figsize=(10, 6))
    pct_ai = df.groupby("posting_year")["ai_mentioned"].mean() * 100
    ax.plot(pct_ai.index, pct_ai.values, marker="o", color="#E91E63", linewidth=2.5, markersize=6)
    ax.fill_between(pct_ai.index, pct_ai.values, alpha=0.15, color="#E91E63")
    ax.set_title("% Tin Đăng Có Đề Cập AI Theo Năm")
    ax.set_xlabel("Năm")
    ax.set_ylabel("Tỷ lệ (%)")
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.1f%%"))
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    _save_fig(fig, OUTPUT_1)

    # 2. Lương theo năm
    fig, ax = plt.subplots(figsize=(10, 6))
    salary_year = df.groupby("posting_year")["salary_usd"].agg(["median", "mean"])
    ax.plot(salary_year.index, salary_year["median"], marker="o", label="Median", color="#1976D2", linewidth=2.5)
    ax.plot(salary_year.index, salary_year["mean"], marker="s", label="Mean", color="#E53935",
            linewidth=2, linestyle="--")
    ax.set_title("Lương Theo Năm")
    ax.set_xlabel("Năm")
    ax.set_ylabel("Lương (USD)")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(_fmt_usd))
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    _save_fig(fig, OUTPUT_2)

    # 3. Xu hướng rủi ro tự động hóa
    fig, ax = plt.subplots(figsize=(10, 6))
    trend = df.groupby("posting_year")["automation_risk_score"].agg(["mean", "median"])
    ax.plot(trend.index, trend["mean"], marker="o", color="#E64A19", linewidth=2.5, label="Mean")
    ax.plot(trend.index, trend["median"], marker="s", color="#1565C0", linewidth=2,
            linestyle="--", label="Median")
    ax.set_title("Xu Hướng Rủi Ro Tự Động Hóa Theo Năm")
    ax.set_xlabel("Năm")
    ax.set_ylabel("Automation Risk Score")
    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.set_ylim(0, 1)
    _save_fig(fig, OUTPUT_3)

    # 4. Xu hướng Reskilling
    fig, ax = plt.subplots(figsize=(10, 6))
    reskill_trend = df.groupby(["posting_year", "reskilling_required"]).size().unstack(fill_value=0)
    years = reskill_trend.index
    no_reskill = reskill_trend.get(False, pd.Series([0] * len(years), index=years))
    yes_reskill = reskill_trend.get(True, pd.Series([0] * len(years), index=years))
    ax.stackplot(
        years,
        no_reskill,
        yes_reskill,
        labels=["Không cần Reskilling", "Cần Reskilling"],
        colors=["#90CAF9", "#FFAB91"],
        alpha=0.85,
    )
    ax.set_title("Xu Hướng Yêu Cầu Tái Đào Tạo (Reskilling)")
    ax.set_xlabel("Năm")
    ax.set_ylabel("Số lượng công việc")
    ax.legend(loc="upper left")
    _save_fig(fig, OUTPUT_4)

if __name__ == "__main__":
    main()
