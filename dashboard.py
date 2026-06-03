"""
dashboard.py — Entry point cho Streamlit Dashboard.
Chạy: python -m streamlit run dashboard.py

AI Impact on Job Market — Interactive Analytics Dashboard (2010–2025)
"""
from __future__ import annotations
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
import streamlit as st

# ── Page config ────────────────────────────────────────
st.set_page_config(
    page_title="AI Job Market Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "AI Impact on Job Market — 2010–2025"},
)

from src.dashboard.styles import get_css, MAIN_CSS
from src.dashboard.kpis import render_kpis
from src.dashboard import tab_overview, tab_salary, tab_risk, tab_map
from src.data.load_data import load

# ── Session state: dark mode mặc định ─────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

dark = st.session_state.dark_mode

# ── Inject CSS theo theme ──────────────────────────────
st.markdown(get_css(dark), unsafe_allow_html=True)

# ── Màu sắc header theo theme ─────────────────────────
_header_border = "rgba(255,255,255,0.08)" if dark else "#e2e8f0"
_muted          = "#64748b"
_record_color   = "#f1f5f9" if dark else "#0f172a"
_gradient       = "linear-gradient(90deg,#6366f1,#06b6d4)"


# ── Cache dữ liệu ─────────────────────────────────────
@st.cache_data(show_spinner="⏳ Đang tải dữ liệu...")
def _load() -> pd.DataFrame:
    df = load()
    for col in ("core_skills_list", "ai_skills_list", "ai_keywords_list"):
        if col not in df.columns:
            base = col.replace("_list", "")
            if base in df.columns:
                df[col] = df[base].str.split(", ")
    return df


df_full = _load()

# ──────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────
with st.sidebar:

    # Logo + tên
    st.markdown(f"""
    <div style="text-align:center;padding:12px 0 4px">
      <h1 style="font-size:1rem;font-weight:700;margin:4px 0 0">AI Job Market</h1>
      <p style="font-size:0.7rem;color:{_muted} !important;margin:0">2010 – 2025</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Toggle Light / Dark ────────────────────────────
    st.markdown("---")
    c_toggle_l, c_toggle_r = st.columns([1, 1])
    with c_toggle_l:
        st.markdown(
            f"<p style='margin:6px 0 0;font-size:0.8rem;font-weight:600;"
            f"color:{_muted} !important;'>{'Dark' if dark else 'Light'}</p>",
            unsafe_allow_html=True,
        )
    with c_toggle_r:
        if st.button(
            "Light" if dark else "Dark",
            key="theme_toggle",
            use_container_width=True,
        ):
            st.session_state.dark_mode = not dark
            st.rerun()

    # ── BỘ LỌC THỜI GIAN & LƯƠNG (cùng nhóm) ─────────
    st.markdown("---")
    st.markdown("### :material/tune: BỘ LỌC")

    # Thanh thời gian
    all_years = sorted(df_full["posting_year"].dropna().unique().tolist())
    year_range = st.select_slider(
        ":material/calendar_month: Giai đoạn (năm)",
        options=all_years,
        value=(all_years[0], all_years[-1]),
    )

    # Thanh lương — ngay dưới thời gian
    if "salary_usd" in df_full.columns:
        sal_min = int(df_full["salary_usd"].min())
        sal_max = int(df_full["salary_usd"].max())
        salary_range = st.slider(
            ":material/attach_money: Khoảng Lương (USD)",
            min_value=sal_min,
            max_value=sal_max,
            value=(sal_min, sal_max),
            step=5_000,
            format="$%d",
        )
    else:
        salary_range = None

    st.markdown("---")

    # Khu vực
    if "region" in df_full.columns:
        all_regions = sorted(df_full["region"].dropna().unique().tolist())
        selected_regions = st.multiselect(
            ":material/globe_asia: Khu Vực",
            options=all_regions,
            default=all_regions,
        )
    else:
        selected_regions = []

    # Ngành nghề
    all_industries = sorted(df_full["industry"].dropna().unique().tolist())
    selected_industries = st.multiselect(
        ":material/factory: Ngành Nghề",
        options=all_industries,
        default=all_industries,
    )

    # Giai đoạn AI
    if "industry_ai_adoption_stage" in df_full.columns:
        all_stages = ["Emerging", "Growing", "Mature"]
        selected_stages = st.multiselect(
            ":material/rocket_launch: Giai Đoạn AI Adoption",
            options=all_stages,
            default=all_stages,
        )
    else:
        selected_stages = []

    # Cấp độ
    if "seniority_level" in df_full.columns:
        all_seniority = ["Junior", "Mid", "Senior", "Lead", "Executive"]
        selected_seniority = st.multiselect(
            ":material/badge: Cấp Độ",
            options=all_seniority,
            default=all_seniority,
        )
    else:
        selected_seniority = []

    st.markdown("---")
    st.caption(":material/lightbulb: Thay đổi bộ lọc để cập nhật toàn bộ dashboard theo thời gian thực.")


# ── Áp dụng bộ lọc ────────────────────────────────────
mask = (
    df_full["posting_year"].between(year_range[0], year_range[1])
    & df_full["industry"].isin(selected_industries)
)
if selected_regions:
    mask &= df_full["region"].isin(selected_regions)
if selected_stages and "industry_ai_adoption_stage" in df_full.columns:
    mask &= df_full["industry_ai_adoption_stage"].isin(selected_stages)
if selected_seniority and "seniority_level" in df_full.columns:
    mask &= df_full["seniority_level"].isin(selected_seniority)
if salary_range and "salary_usd" in df_full.columns:
    mask &= df_full["salary_usd"].between(salary_range[0], salary_range[1])

df = df_full[mask].copy()

# ── Header ─────────────────────────────────────────────
st.markdown(f"""
<div style="
  display:flex; align-items:center; gap:14px;
  padding: 0.5rem 0 1rem;
  border-bottom: 1px solid {_header_border};
  margin-bottom: 1.2rem;
">
  <div>
    <h1 style="
      margin:0; font-size:1.6rem; font-weight:800;
      background: {_gradient};
      -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    ">AI Impact on Job Market</h1>
    <p style="margin:2px 0 0; color:{_muted} !important; font-size:0.82rem;">
      Phân tích tác động AI lên thị trường lao động toàn cầu &nbsp;·&nbsp; 2010–2025
      &nbsp;·&nbsp; {'Dark' if dark else 'Light'} Mode
    </p>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Cảnh báo filter rỗng ───────────────────────────────
if len(df) == 0:
    st.error("Không có dữ liệu phù hợp. Vui lòng mở rộng bộ lọc.")
    st.stop()

# Record count badge
total_pct = len(df) / len(df_full) * 100
st.markdown(
    f'<p style="color:{_muted} !important;font-size:0.78rem;margin:-0.6rem 0 0.8rem;">'
    f'Hiển thị <b style="color:{_record_color} !important">{len(df):,}</b> / {len(df_full):,} bản ghi '
    f'({total_pct:.1f}%)'
    f'&nbsp;·&nbsp; {year_range[0]}–{year_range[1]}'
    + (f'&nbsp;·&nbsp; ${salary_range[0]:,}–${salary_range[1]:,}' if salary_range else '')
    + '</p>',
    unsafe_allow_html=True,
)

# ── KPI Row ────────────────────────────────────────────
render_kpis(df)

st.markdown('<div style="margin:1.2rem 0 0.4rem"></div>', unsafe_allow_html=True)

# ── Tabs ───────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    ":material/dashboard: Tổng Quan",
    ":material/payments: Lương & Kỹ Năng",
    ":material/warning: Rủi Ro AI",
    ":material/public: Bản Đồ Thế Giới",
])

with tab1:
    tab_overview.render(df, dark=dark)

with tab2:
    tab_salary.render(df, dark=dark)

with tab3:
    tab_risk.render(df, dark=dark)

with tab4:
    tab_map.render(df, dark=dark)
