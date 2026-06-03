"""
tab_overview.py — Tab 1: Tổng quan thị trường lao động.
Biểu đồ: Xu hướng theo năm, Top ngành, Top quốc gia, Cấp độ KN theo khu vực.
"""
from __future__ import annotations
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.dashboard.styles import apply_theme, PLOTLY_LAYOUT, PALETTE_ACCENT

H = 320  # chart height px


def render(df: pd.DataFrame, dark: bool = True) -> None:

    # ── Row 1: Trend + Pie ────────────────────────────────
    col_a, col_b = st.columns([2, 1], gap="medium")

    with col_a:
        by_year = df.groupby("posting_year").size().reset_index(name="count")
        pct_ai  = (df.groupby("posting_year")["ai_mentioned"].mean() * 100
                   ).reset_index(name="pct_ai")
        merged  = by_year.merge(pct_ai, on="posting_year")

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=merged["posting_year"], y=merged["count"],
            name="Số tin đăng", marker_color="#6366f1",
            opacity=0.75, hovertemplate="%{x}: %{y:,} tin<extra></extra>",
        ))
        fig.add_trace(go.Scatter(
            x=merged["posting_year"], y=merged["pct_ai"],
            name="% Đề cập AI", yaxis="y2",
            mode="lines+markers",
            line=dict(color="#06b6d4", width=2.5),
            marker=dict(size=7, symbol="circle"),
            hovertemplate="%{x}: %{y:.1f}%<extra></extra>",
        ))
        # Dual-axis: dùng update_layout(**PLOTLY_LAYOUT) trước (không có xaxis/yaxis)
        # rồi update_layout riêng cho axes, tránh duplicate kwarg
        apply_theme(fig, height=H, title=":material/trending_up: Xu Hướng Tuyển Dụng & % Đề Cập AI (2010–2025)", dark=dark)
        fig.update_layout(
            yaxis=dict(title="Số tin đăng"),
            yaxis2=dict(
                title="% AI", overlaying="y", side="right",
                showgrid=False, range=[0, 105],
                ticksuffix="%", tickfont=dict(color="#06b6d4"),
            ),
            legend_orientation="h", legend_y=1.12, legend_x=0,
            bargap=0.25,
        )
        st.plotly_chart(fig, width="stretch")

    with col_b:
        if "ai_mentioned" in df.columns:
            counts = df["ai_mentioned"].value_counts().reset_index()
            counts.columns = ["ai_mentioned", "count"]
            counts["label"] = counts["ai_mentioned"].map({True: "Có AI", False: "Không AI"})
            fig2 = px.pie(
                counts, values="count", names="label", hole=0.55,
                color="label",
                color_discrete_map={"Có AI": "#6366f1", "Không AI": "#1e293b" if dark else "#e2e8f0"},
            )
            fig2.update_traces(
                textfont_size=12, pull=[0.05, 0],
                hovertemplate="%{label}: %{value:,} (%{percent})<extra></extra>",
            )
            apply_theme(fig2, height=H, title=":material/pie_chart: Tỷ Lệ Đề Cập AI", dark=dark)
            st.plotly_chart(fig2, width="stretch")

    # ── Row 2: Top Industry + Top Country ────────────────
    col_c, col_d = st.columns(2, gap="medium")

    with col_c:
        top_ind = df["industry"].value_counts().head(10).reset_index()
        top_ind.columns = ["industry", "count"]
        fig3 = px.bar(
            top_ind.sort_values("count"), x="count", y="industry",
            orientation="h", text_auto=True,
            color="count", color_continuous_scale="Purples",
        )
        fig3.update_traces(hovertemplate="%{y}: %{x:,}<extra></extra>")
        apply_theme(fig3, height=H, title=":material/factory: Top 10 Ngành Tuyển Dụng Nhiều Nhất", dark=dark)
        fig3.update_layout(coloraxis_showscale=False, yaxis_title="", xaxis_title="Số tin")
        st.plotly_chart(fig3, width="stretch")

    with col_d:
        top_country = df["country"].value_counts().head(12).reset_index()
        top_country.columns = ["country", "count"]
        fig4 = px.bar(
            top_country.sort_values("count"), x="count", y="country",
            orientation="h", text_auto=True,
            color="count", color_continuous_scale="Blues",
        )
        fig4.update_traces(hovertemplate="%{y}: %{x:,}<extra></extra>")
        apply_theme(fig4, height=H, title=":material/public: Top 12 Quốc Gia Tuyển Dụng", dark=dark)
        fig4.update_layout(coloraxis_showscale=False, yaxis_title="", xaxis_title="Số tin")
        st.plotly_chart(fig4, width="stretch")

    # ── Row 3: Seniority 100% stacked ─────────────────────
    seniority_order = ["Junior", "Mid", "Senior", "Lead", "Executive"]
    if "region" not in df.columns or "seniority_level" not in df.columns:
        return

    region_sen = (
        df.groupby(["region", "seniority_level"], observed=False)
        .size().unstack(fill_value=0)
    )
    cols_present = [c for c in seniority_order if c in region_sen.columns]
    if not cols_present:
        return

    region_sen = region_sen[cols_present]
    region_pct = region_sen.div(region_sen.sum(axis=1), axis=0) * 100
    region_pct = region_pct.reset_index()

    fig5 = go.Figure()
    colors_map = dict(zip(seniority_order, PALETTE_ACCENT))
    for level in cols_present:
        fig5.add_trace(go.Bar(
            name=level,
            y=region_pct["region"],
            x=region_pct[level],
            orientation="h",
            marker_color=colors_map.get(level, "#888"),
            hovertemplate=f"<b>%{{y}}</b> — {level}: %{{x:.1f}}%<extra></extra>",
        ))

    dyn_h = max(280, len(region_pct) * 38 + 60)
    apply_theme(fig5, height=dyn_h,
                title=":material/badge: Cơ Cấu Cấp Độ Kinh Nghiệm Theo Khu Vực (100%)", dark=dark)
    fig5.update_layout(
        barmode="stack",
        xaxis_ticksuffix="%",
        xaxis_range=[0, 100],
        yaxis_title="",
    )
    st.plotly_chart(fig5, width="stretch")

