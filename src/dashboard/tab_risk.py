"""
tab_risk.py — Tab 3: Phân tích Rủi ro AI & Reskilling.
"""
from __future__ import annotations
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.dashboard.styles import apply_theme, PALETTE_RISK, PALETTE_ACCENT

H = 320


def render(df: pd.DataFrame, dark: bool = True) -> None:

    # ── Row 1: Histogram rủi ro + Donut displacement ──────
    col_a, col_b = st.columns([1.4, 1], gap="medium")

    with col_a:
        risk_data = df["automation_risk_score"].dropna() if "automation_risk_score" in df.columns else pd.Series(dtype=float)
        if not risk_data.empty:
            fig1 = go.Figure()
            fig1.add_trace(go.Histogram(
                x=risk_data, nbinsx=35,
                marker=dict(
                    color=risk_data,
                    colorscale=[[0, "#22c55e"], [0.5, "#f59e0b"], [1, "#ef4444"]],
                    line=dict(width=0.3, color="rgba(0,0,0,0.4)"),
                ),
                hovertemplate="Score: %{x:.2f}<br>Số tin: %{y}<extra></extra>",
            ))
            mean_v = risk_data.mean()
            med_v  = risk_data.median()
            for val, color, dash, label in [
                (mean_v, "#ef4444", "dash",  f"TB: {mean_v:.2f}"),
                (med_v,  "#06b6d4", "solid", f"TV: {med_v:.2f}"),
            ]:
                fig1.add_vline(
                    x=val, line_color=color, line_dash=dash, line_width=2,
                    annotation_text=label, annotation_font_color=color,
                    annotation_position="top right",
                )
            apply_theme(fig1, height=H,
                        title=":material/bar_chart: Phân Bố Điểm Rủi Ro Tự Động Hóa", dark=dark)
            fig1.update_layout(xaxis_title="Automation Risk Score",
                               yaxis_title="Số tin", bargap=0.05)
            st.plotly_chart(fig1, width="stretch")

    with col_b:
        if "ai_job_displacement_risk" in df.columns:
            disp = df["ai_job_displacement_risk"].value_counts().reset_index()
            disp.columns = ["risk", "count"]
            fig2 = px.pie(
                disp, values="count", names="risk", hole=0.58,
                color="risk", color_discrete_map=PALETTE_RISK,
            )
            fig2.update_traces(
                textfont_size=12, pull=[0.05, 0.02, 0],
                hovertemplate="<b>%{label}</b>: %{value:,} (%{percent})<extra></extra>",
            )
            apply_theme(fig2, height=H,
                        title=":material/pie_chart: Phân Bố Rủi Ro Dịch Chuyển Việc Làm", dark=dark)
            st.plotly_chart(fig2, width="stretch")

    # ── Row 2: Risk theo ngành + Reskilling trend ─────────
    col_c, col_d = st.columns([1.2, 1], gap="medium")

    with col_c:
        if "automation_risk_score" in df.columns:
            risk_ind = (
                df.groupby("industry")["automation_risk_score"]
                .median().sort_values().reset_index()
            )
            risk_ind.columns = ["industry", "risk"]
            fig3 = px.bar(
                risk_ind, x="risk", y="industry", orientation="h",
                color="risk",
                color_continuous_scale=[[0, "#22c55e"], [0.5, "#f59e0b"], [1, "#ef4444"]],
                text=risk_ind["risk"].apply(lambda v: f"{v:.2f}"),
            )
            fig3.update_traces(
                textposition="outside",
                hovertemplate="<b>%{y}</b>: %{x:.3f}<extra></extra>",
            )
            dyn_h = max(H + 80, len(risk_ind) * 22 + 60)
            apply_theme(fig3, height=dyn_h,
                        title=":material/factory: Rủi Ro Tự Động Hóa Trung Vị Theo Ngành", dark=dark)
            fig3.update_layout(
                coloraxis_showscale=False,
                xaxis_range=[0, 1.05],
                xaxis_title="Risk Score",
                yaxis_title="",
            )
            st.plotly_chart(fig3, width="stretch")

    with col_d:
        if "reskilling_required" in df.columns:
            reskill_trend = (
                df.groupby(["posting_year", "reskilling_required"])
                .size().unstack(fill_value=0).reset_index()
            )
            reskill_trend.columns.name = None
            fig4 = go.Figure()
            if False in reskill_trend.columns:
                fig4.add_trace(go.Bar(
                    x=reskill_trend["posting_year"],
                    y=reskill_trend[False],
                    name="Không cần Reskilling",
                    marker_color="#6366f1", opacity=0.75,
                    hovertemplate="%{x}: %{y:,}<extra>Không cần</extra>",
                ))
            if True in reskill_trend.columns:
                fig4.add_trace(go.Bar(
                    x=reskill_trend["posting_year"],
                    y=reskill_trend[True],
                    name="Cần Reskilling",
                    marker_color="#f59e0b", opacity=0.85,
                    hovertemplate="%{x}: %{y:,}<extra>Cần Reskilling</extra>",
                ))
            apply_theme(fig4, height=H,
                        title=":material/school: Xu Hướng Yêu Cầu Reskilling Theo Năm", dark=dark)
            fig4.update_layout(
                barmode="stack",
                legend_orientation="h", legend_y=1.1,
                xaxis_title="Năm", yaxis_title="Số tin",
            )
            st.plotly_chart(fig4, width="stretch")

    # ── Row 3: 100% stacked rủi ro theo ngành ─────────────
    if "ai_job_displacement_risk" in df.columns:
        risk_by_ind = (
            df.groupby(["industry", "ai_job_displacement_risk"], observed=True)
            .size().unstack(fill_value=0)
        )
        for col in ["Low", "Medium", "High"]:
            if col not in risk_by_ind.columns:
                risk_by_ind[col] = 0
        risk_pct = risk_by_ind[["Low", "Medium", "High"]]
        risk_pct = (
            risk_pct.div(risk_pct.sum(axis=1), axis=0) * 100
        ).sort_values("High", ascending=True).reset_index()

        fig5 = go.Figure()
        for level in ["Low", "Medium", "High"]:
            fig5.add_trace(go.Bar(
                y=risk_pct["industry"], x=risk_pct[level],
                name=level, orientation="h",
                marker_color=PALETTE_RISK[level],
                hovertemplate=f"<b>%{{y}}</b> — {level}: %{{x:.1f}}%<extra></extra>",
            ))
        dyn_h2 = max(H, len(risk_pct) * 22 + 80)
        apply_theme(fig5, height=dyn_h2,
                    title=":material/stacked_bar_chart: Phân Bố Rủi Ro Dịch Chuyển AI Theo Ngành (100%)", dark=dark)
        fig5.update_layout(
            barmode="stack",
            xaxis_ticksuffix="%",
            xaxis_range=[0, 100],
            yaxis_title="",
            legend_orientation="h", legend_y=1.04,
        )
        st.plotly_chart(fig5, width="stretch")

    # ── Row 4: Risk theo AI adoption stage ───────────────
    if ("industry_ai_adoption_stage" in df.columns and
            "ai_job_displacement_risk" in df.columns):
        stage_risk = (
            df.groupby(
                ["industry_ai_adoption_stage", "ai_job_displacement_risk"],
                observed=True,
            ).size().unstack(fill_value=0)
        )
        for col in ["Low", "Medium", "High"]:
            if col not in stage_risk.columns:
                stage_risk[col] = 0
        stage_pct = stage_risk[["Low", "Medium", "High"]]
        stage_pct = (
            stage_pct.div(stage_pct.sum(axis=1), axis=0) * 100
        ).reindex(["Emerging", "Growing", "Mature"]).reset_index()

        fig6 = go.Figure()
        for level in ["Low", "Medium", "High"]:
            fig6.add_trace(go.Bar(
                x=stage_pct["industry_ai_adoption_stage"],
                y=stage_pct[level],
                name=level,
                marker_color=PALETTE_RISK[level],
                text=stage_pct[level].apply(
                    lambda v: f"{v:.1f}%" if pd.notna(v) and v > 3 else ""),
                textposition="inside",
                textfont_color="white",
                hovertemplate=f"<b>%{{x}}</b> — {level}: %{{y:.1f}}%<extra></extra>",
            ))
        apply_theme(fig6, height=H,
                    title=":material/rocket_launch: Rủi Ro Việc Làm Theo Giai Đoạn Áp Dụng AI", dark=dark)
        fig6.update_layout(
            barmode="stack",
            yaxis_ticksuffix="%",
            yaxis_range=[0, 100],
            xaxis_title="",
            legend_orientation="h", legend_y=1.1,
        )
        st.plotly_chart(fig6, width="stretch")

