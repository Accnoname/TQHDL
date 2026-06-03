"""
tab_salary.py — Tab 2: Phân tích Lương & Kỹ năng.
"""
from __future__ import annotations
from collections import Counter
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.dashboard.styles import apply_theme, PALETTE_ACCENT

H = 320


def _top_items(series_of_lists, top_n=15) -> pd.Series:
    counter: Counter = Counter()
    for lst in series_of_lists.dropna():
        if isinstance(lst, list):
            counter.update(lst)
    if not counter:
        return pd.Series(dtype=int)
    items, counts = zip(*counter.most_common(top_n))
    return pd.Series(counts, index=items)


def render(df: pd.DataFrame, dark: bool = True) -> None:

    # ── Row 1: Bar seniority + Violin ────────────────────
    col_a, col_b = st.columns(2, gap="medium")
    seniority_order = ["Junior", "Mid", "Senior", "Lead", "Executive"]

    with col_a:
        sal_sen = (
            df[df["seniority_level"].isin(seniority_order)]
            .groupby("seniority_level", observed=False)["salary_usd"]
            .median().reindex(seniority_order).reset_index()
        )
        sal_sen.columns = ["seniority_level", "median_salary"]
        fig1 = px.bar(
            sal_sen, x="seniority_level", y="median_salary",
            color="seniority_level",
            color_discrete_sequence=PALETTE_ACCENT,
            text=sal_sen["median_salary"].apply(
                lambda v: f"${v:,.0f}" if pd.notna(v) else ""),
        )
        fig1.update_traces(
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>Median: $%{y:,.0f}<extra></extra>",
        )
        apply_theme(fig1, height=H,
                    title=":material/attach_money: Lương Trung Vị Theo Cấp Độ Kinh Nghiệm", dark=dark)
        fig1.update_layout(showlegend=False, yaxis_tickprefix="$",
                           yaxis_title="USD", xaxis_title="")
        st.plotly_chart(fig1, width="stretch")

    with col_b:
        salary_data = df[
            df["salary_usd"].notna() &
            df["seniority_level"].isin(seniority_order)
        ]
        fig2 = go.Figure()
        for i, level in enumerate(seniority_order):
            sub = salary_data[salary_data["seniority_level"] == level]["salary_usd"]
            if sub.empty:
                continue
            col = PALETTE_ACCENT[i % len(PALETTE_ACCENT)]
            fig2.add_trace(go.Violin(
                y=sub, name=level,
                line_color=col, fillcolor=col,
                opacity=0.6, box_visible=True, meanline_visible=True,
                hovertemplate=f"<b>{level}</b><br>$%{{y:,.0f}}<extra></extra>",
            ))
        apply_theme(fig2, height=H,
                    title=":material/stacked_line_chart: Phân Bố Lương Theo Cấp Độ (Violin)", dark=dark)
        fig2.update_layout(showlegend=False, yaxis_tickprefix="$")
        st.plotly_chart(fig2, width="stretch")

    # ── Row 2: Top ngành lương cao + Lương theo năm ──────
    col_c, col_d = st.columns(2, gap="medium")

    with col_c:
        top_sal = (
            df.groupby("industry")["salary_usd"]
            .median().sort_values(ascending=False).head(10).reset_index()
        )
        top_sal.columns = ["industry", "median_salary"]
        fig3 = px.bar(
            top_sal.sort_values("median_salary"),
            x="median_salary", y="industry", orientation="h",
            color="median_salary", color_continuous_scale="Purples",
            text=top_sal.sort_values("median_salary")["median_salary"]
                .apply(lambda v: f"${v:,.0f}"),
        )
        fig3.update_traces(
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>$%{x:,.0f}<extra></extra>",
        )
        apply_theme(fig3, height=H, title=":material/emoji_events: Top 10 Ngành Có Lương Cao Nhất", dark=dark)
        fig3.update_layout(coloraxis_showscale=False,
                           xaxis_tickprefix="$", xaxis_title="Median USD",
                           yaxis_title="")
        st.plotly_chart(fig3, width="stretch")

    with col_d:
        sal_year = (
            df.groupby("posting_year")["salary_usd"]
            .agg(["median", "mean"]).reset_index()
        )
        fig4 = go.Figure()
        fig4.add_trace(go.Scatter(
            x=sal_year["posting_year"], y=sal_year["median"],
            name="Median", mode="lines+markers",
            line=dict(color="#6366f1", width=2.5), marker=dict(size=7),
            hovertemplate="%{x}: $%{y:,.0f}<extra>Median</extra>",
        ))
        fig4.add_trace(go.Scatter(
            x=sal_year["posting_year"], y=sal_year["mean"],
            name="Mean", mode="lines+markers",
            line=dict(color="#f59e0b", width=2, dash="dot"), marker=dict(size=6),
            hovertemplate="%{x}: $%{y:,.0f}<extra>Mean</extra>",
        ))
        apply_theme(fig4, height=H, title=":material/calendar_today: Xu Hướng Lương Theo Năm", dark=dark)
        fig4.update_layout(
            yaxis_tickprefix="$",
            legend_orientation="h",
            legend_y=1.1,
        )
        st.plotly_chart(fig4, width="stretch")

    # ── Row 3: Top kỹ năng ────────────────────────────────
    col_e, col_f = st.columns(2, gap="medium")

    with col_e:
        if "core_skills_list" in df.columns:
            top_core = _top_items(df["core_skills_list"], 15)
            if not top_core.empty:
                fig5 = px.bar(
                    x=top_core.values[::-1], y=top_core.index[::-1],
                    orientation="h", text=top_core.values[::-1],
                    color=top_core.values[::-1],
                    color_continuous_scale="Blues",
                )
                fig5.update_traces(
                    textposition="outside",
                    hovertemplate="<b>%{y}</b>: %{x:,}<extra></extra>",
                )
                apply_theme(fig5, height=H + 50, title=":material/build: Top 15 Kỹ Năng Cốt Lõi", dark=dark)
                fig5.update_layout(coloraxis_showscale=False,
                                   xaxis_title="Số lượt", yaxis_title="")
                st.plotly_chart(fig5, width="stretch")

    with col_f:
        if "ai_keywords_list" in df.columns:
            top_ai = _top_items(df["ai_keywords_list"], 15)
            if not top_ai.empty:
                fig6 = px.bar(
                    x=top_ai.values[::-1], y=top_ai.index[::-1],
                    orientation="h", text=top_ai.values[::-1],
                    color=top_ai.values[::-1],
                    color_continuous_scale="Reds",
                )
                fig6.update_traces(
                    textposition="outside",
                    hovertemplate="<b>%{y}</b>: %{x:,}<extra></extra>",
                )
                apply_theme(fig6, height=H + 50, title=":material/smart_toy: Top 15 Từ Khóa AI", dark=dark)
                fig6.update_layout(coloraxis_showscale=False,
                                   xaxis_title="Số lượt", yaxis_title="")
                st.plotly_chart(fig6, width="stretch")
