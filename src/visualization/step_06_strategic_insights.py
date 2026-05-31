"""
step_06_strategic_insights.py — Trả lời câu hỏi chiến lược & Heatmap
"""
import sys
from pathlib import Path
from typing import Optional, Sequence

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
from src.data.load_data import load

try:
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

OUTPUT_DIR = PROJECT_ROOT / "reports" / "figures"
OUTPUT_1 = OUTPUT_DIR / "output_step_06_strategic_1.png"
OUTPUT_HTML_JOBS = PROJECT_ROOT / "reports" / "figures" / "output_step_06_worldmap_jobs.html"
OUTPUT_HTML_SALARY = PROJECT_ROOT / "reports" / "figures" / "output_step_06_worldmap_salary.html"

def _fmt_usd(x, _):
    if pd.isna(x):
        return ""
    return f"${int(x):,}"


def _pick_first_column(df: pd.DataFrame, candidates: Sequence[str]) -> Optional[str]:
    for col in candidates:
        if col in df.columns:
            return col
    return None

def _build_skill_stats(df: pd.DataFrame) -> pd.DataFrame:
    def _merge_lists(row):
        skills = []
        if isinstance(row["core_skills_list"], list):
            skills.extend([s for s in row["core_skills_list"] if s])
        if isinstance(row["ai_skills_list"], list):
            skills.extend([s for s in row["ai_skills_list"] if s])
        return skills

    tmp = df.copy()
    tmp["all_skills_list"] = tmp.apply(_merge_lists, axis=1)
    exploded = tmp.explode("all_skills_list").dropna(subset=["all_skills_list"])
    exploded["all_skills_list"] = exploded["all_skills_list"].str.strip()
    exploded = exploded[exploded["all_skills_list"].ne("")]

    stats = (
        exploded.groupby("all_skills_list")["salary_usd"]
        .agg(["count", "mean"])
        .rename(columns={"count": "job_count", "mean": "mean_salary"})
        .sort_values("job_count", ascending=False)
    )
    return stats


def plot_risk_by_adoption_stage(df: pd.DataFrame, output_path: Path) -> None:
    """
    Vẽ biểu đồ cột chồng 100% thể hiện phân bổ rủi ro mất việc
    theo từng giai đoạn áp dụng AI của ngành.
    """
    print("Đang vẽ biểu đồ cột chồng chiến lược...")

    required_cols = {"industry_ai_adoption_stage", "ai_job_displacement_risk"}
    if not required_cols.issubset(df.columns):
        missing = ", ".join(sorted(required_cols - set(df.columns)))
        print(f"Thiếu cột: {missing}. Bỏ qua biểu đồ.")
        return

    risk_dist = (
        df.groupby(["industry_ai_adoption_stage", "ai_job_displacement_risk"])
        .size()
        .unstack(fill_value=0)
    )

    for col in ["Low", "Medium", "High"]:
        if col not in risk_dist.columns:
            risk_dist[col] = 0
    risk_dist = risk_dist[["Low", "Medium", "High"]]

    stages_order = ["Emerging", "Growing", "Mature"]
    valid_stages = [s for s in stages_order if s in risk_dist.index]
    risk_dist = risk_dist.reindex(valid_stages)

    if risk_dist.empty:
        print("Không đủ dữ liệu cho biểu đồ rủi ro.")
        return

    risk_pct = risk_dist.div(risk_dist.sum(axis=1), axis=0).fillna(0) * 100

    fig, ax = plt.subplots(figsize=(10, 6))
    colors = ["#2ca02c", "#ff7f0e", "#d62728"]

    risk_pct.plot(kind="bar", stacked=True, ax=ax, color=colors, edgecolor="white", width=0.6)

    ax.set_title(
        "Phân bổ Rủi ro việc làm theo Giai đoạn áp dụng AI",
        fontsize=14,
        pad=15,
        fontweight="bold",
    )
    ax.set_xlabel("Giai đoạn áp dụng AI của Ngành (Adoption Stage)", fontsize=12)
    ax.set_ylabel("Tỷ lệ phần trăm việc làm (%)", fontsize=12)
    ax.set_ylim(0, 100)
    plt.xticks(rotation=0, fontsize=11)

    ax.legend(title="Mức độ rủi ro (Risk)", loc="upper left", bbox_to_anchor=(1.02, 1), borderaxespad=0.0)

    for container in ax.containers:
        for bar in container:
            height = bar.get_height()
            if height > 2:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_y() + height / 2,
                    f"{height:.1f}%",
                    ha="center",
                    va="center",
                    color="white",
                    fontweight="bold",
                    fontsize=10,
                )

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print(f"Đã lưu biểu đồ thành công tại: {output_path}")


def plot_world_heatmap(
    df: pd.DataFrame,
    color_col: str,
    title: str,
    output_html: Path,
    color_scale,
) -> None:
    if not PLOTLY_AVAILABLE:
        print("Plotly not available. Skip world heatmap.")
        return

    if "country" not in df.columns or "posting_year" not in df.columns:
        print("Missing country/posting_year. Skip world heatmap.")
        return

    agg_map = {"job_count": ("country", "size")}
    if "salary_usd" in df.columns:
        agg_map["mean_salary"] = ("salary_usd", "mean")
    if "ai_intensity_score" in df.columns:
        agg_map["mean_ai_intensity"] = ("ai_intensity_score", "mean")

    stats = (
        df.dropna(subset=["country", "posting_year"])
        .groupby(["country", "posting_year"]).agg(**agg_map)
        .reset_index()
    )
    stats = stats.sort_values(by="posting_year")

    if color_col not in stats.columns:
        print(f"Missing {color_col}. Skip world heatmap.")
        return

    hover_data = {"job_count": True}
    if "mean_salary" in stats.columns:
        hover_data["mean_salary"] = ":,.0f"
    if "mean_ai_intensity" in stats.columns:
        hover_data["mean_ai_intensity"] = ":.2f"

    max_color = stats[color_col].max()
    if pd.isna(max_color) or max_color == 0:
        print(f"Empty values for {color_col}. Skip world heatmap.")
        return

    fig = px.choropleth(
        stats,
        locations="country",
        locationmode="country names",
        color=color_col,
        hover_name="country",
        hover_data=hover_data,
        animation_frame="posting_year",
        color_continuous_scale=color_scale,
        range_color=[0, max_color],
        title=title,
    )
    fig.write_html(output_html)
    print(f"Saved interactive map -> {output_html}")


def main():
    df = load()

    plot_risk_by_adoption_stage(df, OUTPUT_1)

if __name__ == "__main__":
    main()
