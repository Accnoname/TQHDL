"""
styles.py — CSS injection cho Streamlit dashboard premium.
Hỗ trợ Dark-mode (glassmorphism neon) và Light-mode (trắng sạch).
"""

# ── CSS chung cho cả hai theme ─────────────────────────
_CSS_COMMON = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}
header[data-testid="stHeader"] { display: none !important; }
.block-container {
    padding: 1.5rem 2rem 2rem !important;
    max-width: 1600px !important;
}

/* ── Tabs pill ─────────────────────────────────────── */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    border-radius: 50px !important;
    padding: 4px !important;
    gap: 2px !important;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 50px !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    padding: 6px 18px !important;
    transition: all .2s !important;
    border: none !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
    background: #6366f1 !important;
    color: white !important;
    font-weight: 700 !important;
    box-shadow: 0 2px 14px rgba(99,102,241,0.45) !important;
}

/* ── Chart containers ─────────────────────────────── */
[data-testid="stPlotlyChart"] {
    border-radius: 14px !important;
    padding: 0.2rem !important;
    transition: border-color .25s !important;
}

/* ── Metric card base ─────────────────────────────── */
[data-testid="metric-container"] {
    border-radius: 14px !important;
    padding: 1.2rem 1.4rem !important;
    backdrop-filter: blur(12px) !important;
    transition: border-color .25s, background .25s !important;
}
[data-testid="metric-container"] [data-testid="stMetricLabel"] {
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-size: 1.85rem !important;
    font-weight: 800 !important;
    line-height: 1.2 !important;
}

/* ── Sidebar multiselect tags ─────────────────────── */
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {
    background-color: #6366f1 !important;
    border-radius: 20px !important;
}

/* ── Scrollbar ────────────────────────────────────── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
</style>
"""

# ── CSS Dark mode ──────────────────────────────────────
_CSS_DARK = """
<style>
.stApp, [data-testid="stAppViewContainer"] {
    background-color: #0b0f19 !important;
}
[data-testid="stAppViewContainer"] p, 
[data-testid="stAppViewContainer"] span, 
[data-testid="stAppViewContainer"] label, 
[data-testid="stAppViewContainer"] h1, 
[data-testid="stAppViewContainer"] h2, 
[data-testid="stAppViewContainer"] h3, 
[data-testid="stAppViewContainer"] h4, 
[data-testid="stAppViewContainer"] h5, 
[data-testid="stAppViewContainer"] h6, 
div[class*="st-emotion-cache"] {
    color: #f1f5f9 !important;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#0f1629,#0b0f19) !important;
    border-right: 1px solid rgba(255,255,255,0.08) !important;
}
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.08) !important; }
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
}
[data-testid="metric-container"]:hover {
    border-color: #6366f1 !important;
    background: rgba(255,255,255,0.08) !important;
}
[data-testid="metric-container"] [data-testid="stMetricLabel"] { color: #94a3b8 !important; }
[data-testid="metric-container"] [data-testid="stMetricValue"] { color: #f1f5f9 !important; }
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
}
[data-testid="stTabs"] [data-baseweb="tab"] { color: #94a3b8 !important; }
[data-testid="stPlotlyChart"] {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
}
[data-testid="stPlotlyChart"]:hover { border-color: rgba(99,102,241,0.4) !important; }
hr { border-color: rgba(255,255,255,0.08) !important; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.15); border-radius: 99px; }

/* ── Form Inputs Dark Mode ──────────────────────────── */
.stMultiSelect div[data-baseweb="select"] > div, 
.stSelectbox div[data-baseweb="select"] > div {
    background-color: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 8px !important;
}
.stMultiSelect div[data-baseweb="select"]:hover > div, 
.stSelectbox div[data-baseweb="select"]:hover > div {
    border-color: #6366f1 !important;
}
div[data-baseweb="popover"] > div {
    background-color: #1e293b !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
}
ul[role="listbox"] li {
    background-color: transparent !important;
    color: #f1f5f9 !important;
}
ul[role="listbox"] li:hover, ul[role="listbox"] li[aria-selected="true"] {
    background-color: rgba(255,255,255,0.08) !important;
}
</style>
"""

# ── CSS Light mode ─────────────────────────────────────
_CSS_LIGHT = """
<style>
.stApp, [data-testid="stAppViewContainer"] {
    background-color: #f8fafc !important;
}
[data-testid="stAppViewContainer"] p, 
[data-testid="stAppViewContainer"] span, 
[data-testid="stAppViewContainer"] label, 
[data-testid="stAppViewContainer"] h1, 
[data-testid="stAppViewContainer"] h2, 
[data-testid="stAppViewContainer"] h3, 
[data-testid="stAppViewContainer"] h4, 
[data-testid="stAppViewContainer"] h5, 
[data-testid="stAppViewContainer"] h6, 
div[class*="st-emotion-cache"] {
    color: #0f172a !important;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#f0f4ff,#f8fafc) !important;
    border-right: 1px solid #e2e8f0 !important;
}
[data-testid="stSidebar"] hr { border-color: #e2e8f0 !important; }
[data-testid="metric-container"] {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    box-shadow: 0 1px 6px rgba(0,0,0,0.06) !important;
}
[data-testid="metric-container"]:hover {
    border-color: #6366f1 !important;
    background: #f1f5f9 !important;
}
[data-testid="metric-container"] [data-testid="stMetricLabel"] { color: #64748b !important; }
[data-testid="metric-container"] [data-testid="stMetricValue"] { color: #0f172a !important; }
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: #e2e8f0 !important;
    border: 1px solid #e2e8f0 !important;
}
[data-testid="stTabs"] [data-baseweb="tab"] { color: #64748b !important; }
[data-testid="stPlotlyChart"] {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    box-shadow: 0 1px 6px rgba(0,0,0,0.05) !important;
}
[data-testid="stPlotlyChart"]:hover { border-color: #6366f1 !important; }
hr { border-color: #e2e8f0 !important; }
::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 99px; }

/* Giữ màu chữ trắng cho các thẻ tag (multiselect) và các phần tử có background màu (nút gạt, nút tab active) */
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] span,
[data-testid="stTabs"] [aria-selected="true"] {
    color: #ffffff !important;
}
/* Dữ nguyên inline style color có !important */
[style*="color:"] {
    /* Đã được override inline ở mã Python bằng !important */
}

/* ── Form Inputs Light Mode ─────────────────────────── */
.stMultiSelect div[data-baseweb="select"] > div, 
.stSelectbox div[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 8px !important;
}
.stMultiSelect div[data-baseweb="select"]:hover > div, 
.stSelectbox div[data-baseweb="select"]:hover > div {
    border-color: #6366f1 !important;
}
div[data-baseweb="popover"] > div {
    background-color: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
}
ul[role="listbox"] li {
    background-color: transparent !important;
    color: #0f172a !important;
}
ul[role="listbox"] li:hover, ul[role="listbox"] li[aria-selected="true"] {
    background-color: #f1f5f9 !important;
}
</style>
"""

# ── Plotly overrides cho light mode ───────────────────
PLOTLY_LIGHT = dict(
    paper_bgcolor="#ffffff",
    plot_bgcolor="#f8fafc",
    font_color="#0f172a",
    title_font_color="#0f172a",
    hoverlabel=dict(
        bgcolor="#ffffff",
        bordercolor="#e2e8f0",
        font_color="#0f172a",
        font_size=12,
    ),
)
PLOTLY_LIGHT_AXIS = dict(
    gridcolor="#e2e8f0",
    zerolinecolor="#cbd5e1",
    tickfont=dict(color="#64748b"),
    linecolor="#e2e8f0",
)


def get_css(dark: bool = True) -> str:
    """Trả về CSS hoàn chỉnh theo theme."""
    return _CSS_COMMON + (_CSS_DARK if dark else _CSS_LIGHT)


# Alias backward-compat
MAIN_CSS = get_css(dark=True)

# ── Plotly base layout ─────────────────────────────────
# KO chứa legend / coloraxis_colorbar / xaxis / yaxis
# (tránh duplicate kwarg khi update_layout)
_PLOTLY_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#cbd5e1", size=12),
    title_font=dict(family="Inter", size=14, color="#f1f5f9"),
    margin=dict(l=16, r=16, t=40, b=16),
    hoverlabel=dict(
        bgcolor="#1e293b",
        bordercolor="rgba(255,255,255,0.15)",
        font_color="#f1f5f9",
        font_size=12,
    ),
)

# Alias
PLOTLY_LAYOUT = _PLOTLY_BASE

# Legend style mặc định
_LEGEND_STYLE = dict(
    bgcolor="rgba(255,255,255,0.04)",
    bordercolor="rgba(255,255,255,0.1)",
    borderwidth=1,
    font=dict(size=11),
)

# Axis style
_AXIS_STYLE = dict(
    gridcolor="rgba(255,255,255,0.06)",
    zerolinecolor="rgba(255,255,255,0.08)",
    tickfont=dict(size=11, color="#cbd5e1"),
    linecolor="rgba(255,255,255,0.1)",
)


def apply_theme(fig, height: int = 320, title: str = "",
                dark: bool = True) -> "go.Figure":
    """
    Áp dark hoặc light theme lên fig.
    Mỗi thuộc tính gọi riêng — không có duplicate keyword argument.
    """
    if dark:
        fig.update_layout(**_PLOTLY_BASE)
        fig.update_xaxes(**_AXIS_STYLE)
        fig.update_yaxes(**_AXIS_STYLE)
        fig.update_layout(legend=_LEGEND_STYLE)
        fig.update_layout(
            coloraxis_colorbar=dict(
                tickfont=dict(color="#cbd5e1"),
                title_font=dict(color="#cbd5e1"),
            )
        )
    else:
        # Light mode
        fig.update_layout(**PLOTLY_LIGHT)
        fig.update_xaxes(**PLOTLY_LIGHT_AXIS)
        fig.update_yaxes(**PLOTLY_LIGHT_AXIS)
        fig.update_layout(
            legend=dict(
                bgcolor="rgba(255,255,255,0.9)",
                bordercolor="#e2e8f0",
                borderwidth=1,
                font=dict(size=11, color="#0f172a"),
            )
        )
        fig.update_layout(
            coloraxis_colorbar=dict(
                tickfont=dict(color="#64748b"),
                title_font=dict(color="#0f172a"),
            )
        )

    fig.update_layout(height=height)
    if title:
        fig.update_layout(title_text=title)
    return fig


# Bảng màu accent
PALETTE_ACCENT = ["#6366f1", "#06b6d4", "#f59e0b", "#22c55e", "#f472b6",
                  "#a78bfa", "#34d399", "#fb923c", "#60a5fa", "#e879f9"]
PALETTE_RISK   = {"Low": "#22c55e", "Medium": "#f59e0b", "High": "#ef4444"}
PALETTE_STAGE  = {"Emerging": "#f59e0b", "Growing": "#06b6d4", "Mature": "#6366f1"}
