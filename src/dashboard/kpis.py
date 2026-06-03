"""
kpis.py — Hàng KPI metric cards phía trên dashboard.
"""
from __future__ import annotations
import pandas as pd
import streamlit as st


def render_kpis(df: pd.DataFrame) -> None:
    """Hiển thị 5 KPI cards từ dữ liệu đã lọc."""

    total_jobs      = len(df)
    avg_salary      = df["salary_usd"].mean() if "salary_usd" in df.columns else 0
    median_salary   = df["salary_usd"].median() if "salary_usd" in df.columns else 0
    avg_risk        = df["automation_risk_score"].mean() if "automation_risk_score" in df.columns else 0
    pct_ai          = df["ai_mentioned"].mean() * 100 if "ai_mentioned" in df.columns else 0
    pct_reskill     = df["reskilling_required"].mean() * 100 if "reskilling_required" in df.columns else 0

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.metric(
            label=":material/folder_open: Tổng Tin Tuyển Dụng",
            value=f"{total_jobs:,}",
        )
    with c2:
        st.metric(
            label=":material/payments: Lương Trung Bình",
            value=f"${avg_salary:,.0f}",
            delta=f"Median ${median_salary:,.0f}",
        )
    with c3:
        st.metric(
            label=":material/warning: Rủi Ro Tự Động Hóa",
            value=f"{avg_risk:.2f}",
            delta="Thang điểm 0–1",
        )
    with c4:
        st.metric(
            label=":material/smart_toy: % Đề Cập AI",
            value=f"{pct_ai:.1f}%",
        )
    with c5:
        st.metric(
            label=":material/school: % Cần Reskilling",
            value=f"{pct_reskill:.1f}%",
        )
