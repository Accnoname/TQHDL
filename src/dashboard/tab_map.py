"""
tab_map.py — Tab 4: Bản đồ thế giới tương tác (Choropleth Plotly).
"""
from __future__ import annotations
import pandas as pd
import plotly.express as px
import streamlit as st

from src.dashboard.styles import apply_theme

def get_geo(dark: bool = True):
    return dict(
        bgcolor="rgba(0,0,0,0)",
        showframe=False,
        showcoastlines=True,
        coastlinecolor="rgba(255,255,255,0.15)" if dark else "rgba(0,0,0,0.1)",
        showland=True,
        landcolor="#1e293b" if dark else "#e2e8f0",
        showocean=True,
        oceancolor="#0b0f19" if dark else "#f0f4ff",
        showlakes=False,
        showcountries=True,
        countrycolor="rgba(255,255,255,0.1)" if dark else "rgba(0,0,0,0.05)",
        projection_type="natural earth",
    )


def _make_map(df_stats, color_col, color_scale, cb_title, cb_fmt="",
              hover_extra=None, title="", height=460, dark=True):
    """Tạo choropleth figure chuẩn hóa."""
    hover_extra = hover_extra or {}
    max_c = df_stats[color_col].quantile(0.95)

    fig = px.choropleth(
        df_stats,
        locations="country",
        locationmode="country names",
        color=color_col,
        hover_name="country",
        hover_data={"job_count": True, **hover_extra},
        animation_frame="posting_year",
        color_continuous_scale=color_scale,
        range_color=[0, max_c],
        labels={color_col: cb_title},
    )

    # apply_theme để ra dark base (không pass coloraxis_colorbar ở đây)
    apply_theme(fig, height=height, title=title, dark=dark)

    # Override geo + margin riêng (không conflict)
    fig.update_layout(
        geo=get_geo(dark),
        margin=dict(l=0, r=0, t=40, b=0),
    )

    # Colorbar riêng — 1 lần gọi duy nhất, không conflict
    cb_args = dict(
        title=cb_title,
        tickfont=dict(color="#cbd5e1"),
        title_font=dict(color="#cbd5e1"),
    )
    if cb_fmt:
        cb_args["tickprefix"] = cb_fmt
    fig.update_layout(coloraxis_colorbar=cb_args)

    return fig


def render(df: pd.DataFrame, dark: bool = True) -> None:
    if "country" not in df.columns:
        st.info("Không có cột 'country' trong dữ liệu.")
        return

    # ── Chuẩn bị dữ liệu tổng hợp theo quốc gia + năm ────
    agg_args: dict = {"job_count": ("country", "size")}
    if "salary_usd" in df.columns:
        agg_args["mean_salary"] = ("salary_usd", "mean")
    if "automation_risk_score" in df.columns:
        agg_args["mean_risk"] = ("automation_risk_score", "mean")
    if "ai_intensity_score" in df.columns:
        agg_args["mean_ai_intensity"] = ("ai_intensity_score", "mean")

    stats = (
        df.dropna(subset=["country"])
        .groupby(["country", "posting_year"]).agg(**agg_args)
        .reset_index()
        .sort_values("posting_year")
    )

    # ── Map 1: Số lượng tin tuyển dụng ────────────────────
    st.markdown("#### :material/map: Mật Độ Tuyển Dụng Theo Quốc Gia")
    st.caption("Kéo thanh thời gian ▶ để xem diễn biến 2010–2025. Hover để xem chi tiết.")

    extra1 = {}
    if "mean_salary" in stats.columns:
        extra1["mean_salary"] = ":,.0f"
    if "mean_risk" in stats.columns:
        extra1["mean_risk"] = ":.3f"

    fig1 = _make_map(
        stats, "job_count", "Purples", "Số tin tuyển dụng",
        hover_extra=extra1,
        title=":material/map: Số Tin Tuyển Dụng Theo Quốc Gia & Năm",
        dark=dark,
    )
    st.plotly_chart(fig1, width="stretch")

    # ── Map 2: Lương trung bình ────────────────────────────
    if "mean_salary" in stats.columns:
        st.markdown("---")
        st.markdown("#### :material/payments: Lương Trung Bình Theo Quốc Gia")

        fig2 = _make_map(
            stats, "mean_salary", "Blues", "Lương TB (USD)",
            cb_fmt="$",
            hover_extra={"job_count": True},
            title=":material/payments: Lương Trung Bình Theo Quốc Gia & Năm",
            dark=dark,
        )
        st.plotly_chart(fig2, width="stretch")

    # ── Map 3: Cường độ AI ─────────────────────────────────
    if "mean_ai_intensity" in stats.columns:
        st.markdown("---")
        st.markdown("#### :material/smart_toy: Cường Độ AI Trung Bình Theo Quốc Gia")

        ai_min = stats["mean_ai_intensity"].min()
        ai_max = stats["mean_ai_intensity"].max()

        fig3 = px.choropleth(
            stats,
            locations="country",
            locationmode="country names",
            color="mean_ai_intensity",
            hover_name="country",
            hover_data={"mean_ai_intensity": ":.2f", "job_count": True},
            animation_frame="posting_year",
            color_continuous_scale=[[0, "#1e293b" if dark else "#e2e8f0"], [0.5, "#6366f1"], [1, "#06b6d4"]],
            range_color=[ai_min, ai_max],
            labels={"mean_ai_intensity": "AI Intensity"},
        )
        apply_theme(fig3, height=460, title=":material/smart_toy: Cường Độ AI Trung Bình Theo Quốc Gia & Năm", dark=dark)
        fig3.update_layout(
            geo=get_geo(dark),
            margin=dict(l=0, r=0, t=40, b=0),
        )
        fig3.update_layout(
            coloraxis_colorbar=dict(
                title="AI Intensity",
                tickfont=dict(color="#cbd5e1"),
                title_font=dict(color="#cbd5e1"),
            )
        )
        st.plotly_chart(fig3, width="stretch")

