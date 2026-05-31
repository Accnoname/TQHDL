"""
step_05_text_skills.py — Phân tích Kỹ năng: Text & Categorical
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import matplotlib.pyplot as plt
from collections import Counter
import pandas as pd
from src.data.load_data import load

OUTPUT_DIR = PROJECT_ROOT / "reports" / "figures"
OUTPUT_1 = OUTPUT_DIR / "output_step_05_text_skills_1.png"
OUTPUT_2 = OUTPUT_DIR / "output_step_05_text_skills_2.png"
OUTPUT_3 = OUTPUT_DIR / "output_step_05_text_skills_3.png"
OUTPUT_4 = OUTPUT_DIR / "output_step_05_text_skills_4.png"


def _save_fig(fig: plt.Figure, output_path: Path) -> None:
    fig.tight_layout()
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved -> {output_path}")

def _top_items(series_of_lists, top_n=15) -> pd.Series:
    counter: Counter = Counter()
    for lst in series_of_lists.dropna():
        counter.update(lst)
    items, counts = zip(*counter.most_common(top_n))
    return pd.Series(counts, index=items)

def main():
    df = load()

    # 1. Top 15 Core Skills
    fig, ax = plt.subplots(figsize=(10, 7))
    top_skills = _top_items(df["core_skills_list"])
    palette = plt.cm.Blues_r([0.3 + 0.05 * i for i in range(len(top_skills))])
    ax.barh(top_skills.index[::-1], top_skills.values[::-1], color=palette[::-1], edgecolor="white")
    ax.set_title("Top 15 Kỹ Năng Cốt Lõi")
    ax.set_xlabel("Số lượt đề cập")
    for i, (idx, val) in enumerate(zip(top_skills.index[::-1], top_skills.values[::-1])):
        ax.text(val + 10, i, str(val), va="center", fontsize=8)
    _save_fig(fig, OUTPUT_1)

    # 2. Top 15 AI Keywords
    fig, ax = plt.subplots(figsize=(10, 7))
    top_ai_kw = _top_items(df["ai_keywords_list"])
    palette2 = plt.cm.Reds_r([0.3 + 0.05 * i for i in range(len(top_ai_kw))])
    ax.barh(top_ai_kw.index[::-1], top_ai_kw.values[::-1], color=palette2[::-1], edgecolor="white")
    ax.set_title("Top 15 Từ Khóa AI")
    ax.set_xlabel("Số lượt đề cập")
    for i, (idx, val) in enumerate(zip(top_ai_kw.index[::-1], top_ai_kw.values[::-1])):
        ax.text(val + 2, i, str(val), va="center", fontsize=8)
    _save_fig(fig, OUTPUT_2)

    # 3. Tỷ lệ cần reskilling theo ngành
    fig, ax = plt.subplots(figsize=(10, 8))
    reskill = (
        df.groupby("industry")["reskilling_required"]
        .mean()
        .sort_values(ascending=True)
        * 100
    )
    colors = ["#EF9A9A" if v >= 50 else "#A5D6A7" for v in reskill.values]
    ax.barh(reskill.index, reskill.values, color=colors, edgecolor="white")
    ax.axvline(50, color="gray", linestyle="--", linewidth=1, alpha=0.7)
    ax.set_title("% Cần Reskilling Theo Ngành")
    ax.set_xlabel("Tỷ lệ (%)")
    for i, val in enumerate(reskill.values):
        ax.text(val + 0.5, i, f"{val:.1f}%", va="center", fontsize=8)
    _save_fig(fig, OUTPUT_3)

    # 4. Rủi ro dịch chuyển AI theo ngành
    fig, ax = plt.subplots(figsize=(10, 8))
    risk_by_industry = (
        df.groupby(["industry", "ai_job_displacement_risk"], observed=True)
        .size()
        .unstack(fill_value=0)
    )
    risk_by_industry_pct = risk_by_industry.div(risk_by_industry.sum(axis=1), axis=0) * 100
    risk_by_industry_pct = risk_by_industry_pct.sort_values("High", ascending=True)
    c_map = {"Low": "#66BB6A", "Medium": "#FFA726", "High": "#EF5350"}
    bottom = pd.Series([0.0] * len(risk_by_industry_pct), index=risk_by_industry_pct.index)
    for risk in ["Low", "Medium", "High"]:
        if risk in risk_by_industry_pct.columns:
            ax.barh(risk_by_industry_pct.index, risk_by_industry_pct[risk],
                    left=bottom, color=c_map[risk], label=risk)
            bottom += risk_by_industry_pct[risk]
    ax.set_title("Rủi Ro Dịch Chuyển AI Theo Ngành (%)")
    ax.set_xlabel("Tỷ lệ (%)")
    ax.legend(title="Mức độ rủi ro", loc="lower right")
    _save_fig(fig, OUTPUT_4)

if __name__ == "__main__":
    main()
