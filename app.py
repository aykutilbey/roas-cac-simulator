import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Meta Ads Simulator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Syne:wght@400;600;700;800&display=swap');

/* Root variables */
:root {
    --bg: #0d0f14;
    --surface: #13161e;
    --border: #1e2230;
    --accent: #e8ff47;
    --accent2: #ff6b35;
    --text: #f0f2f7;
    --muted: #6b7280;
}

html, body, [data-testid="stApp"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Syne', sans-serif;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] * {
    color: var(--text) !important;
    font-family: 'Syne', sans-serif !important;
}

/* Sliders */
.stSlider > div > div > div > div {
    background: var(--accent) !important;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 20px !important;
    position: relative !important;
    overflow: hidden !important;
    transition: border-color 0.2s ease !important;
}

[data-testid="stMetric"]:hover {
    border-color: var(--accent) !important;
}

[data-testid="stMetricLabel"] > div {
    color: var(--muted) !important;
    font-size: 0.72rem !important;
    font-family: 'DM Mono', monospace !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}

[data-testid="stMetricValue"] {
    color: var(--text) !important;
    font-size: 1.6rem !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
}

[data-testid="stMetricDelta"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
}

/* Header */
.header-container {
    display: flex;
    align-items: flex-end;
    gap: 16px;
    margin-bottom: 2rem;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid var(--border);
}

.badge {
    display: inline-block;
    background: var(--accent);
    color: #0d0f14;
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.1em;
    padding: 4px 10px;
    border-radius: 4px;
    margin-bottom: 8px;
}

.main-title {
    font-size: 2.4rem;
    font-weight: 800;
    line-height: 1.1;
    margin: 0;
    color: var(--text);
}

.main-title span {
    color: var(--accent);
}

.subtitle {
    color: var(--muted);
    font-size: 0.85rem;
    margin-top: 6px;
    font-family: 'DM Mono', monospace;
}

/* Section titles */
.section-title {
    font-size: 0.7rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    font-family: 'DM Mono', monospace;
    margin-bottom: 12px;
    margin-top: 32px;
    padding-bottom: 6px;
    border-bottom: 1px solid var(--border);
}

/* ROAS highlight card */
.roas-card {
    background: linear-gradient(135deg, #1a1f2e 0%, #13161e 100%);
    border: 1px solid var(--accent);
    border-radius: 12px;
    padding: 24px 28px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 16px;
}

.roas-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--muted);
}

.roas-value {
    font-size: 3rem;
    font-weight: 800;
    color: var(--accent);
    line-height: 1;
}

.roas-desc {
    font-size: 0.78rem;
    color: var(--muted);
    margin-top: 4px;
    font-family: 'DM Mono', monospace;
}

/* Divider */
hr {
    border: none;
    border-top: 1px solid var(--border) !important;
    margin: 1.5rem 0 !important;
}

/* Sidebar title */
.sidebar-logo {
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--accent);
    letter-spacing: 0.05em;
    padding: 4px 0 16px 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 20px;
}

/* Footer */
.footer {
    margin-top: 40px;
    padding-top: 16px;
    border-top: 1px solid var(--border);
    color: var(--muted);
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.06em;
    text-align: center;
}

/* Plotly chart container */
.js-plotly-plot .plotly .modebar {
    background: transparent !important;
}

/* Remove default streamlit branding */
#MainMenu, footer {visibility: hidden;}
[data-testid="stToolbar"] {visibility: hidden;}

/* Column gaps */
[data-testid="column"] {
    padding: 0 6px !important;
}
</style>
""", unsafe_allow_html=True)

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-logo">📊 META ADS SIMULATOR</div>', unsafe_allow_html=True)
    st.markdown("**Campaign Parameters**")
    st.markdown(
        '<p style="font-family:\'DM Mono\',monospace;font-size:0.65rem;color:#6b7280;margin-top:-8px;">'
        "Enter your campaign values manually.</p>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    budget = st.number_input(
        "Monthly Ad Budget (₺)",
        min_value=0, max_value=10_000_000,
        value=10_000, step=1_000,
    )

    cpc = st.number_input(
        "Cost Per Click / CPC (₺)",
        min_value=0.0, max_value=100_000.0,
        value=5.0, step=0.1, format="%.2f",
    )

    conversion_rate = st.number_input(
        "Conversion Rate (%)",
        min_value=0.0, max_value=100.0,
        value=2.5, step=0.1, format="%.2f",
    )

    avg_package = st.number_input(
        "Average Deal Value (₺)",
        min_value=0, max_value=10_000_000,
        value=15_000, step=500,
    )

    st.markdown("---")

# ─── Calculations ─────────────────────────────────────────────────────────────
clicks     = (budget / cpc) if cpc > 0 else 0
customers  = clicks * (conversion_rate / 100)
cac        = (budget / customers) if customers > 0 else 0
revenue    = customers * avg_package
net_profit = revenue - budget
roas       = (revenue / budget) if budget > 0 else 0

# ─── Main Content ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-container">
    <div>
        <div class="badge">META ADS · CAMPAIGN DASHBOARD</div>
        <h1 class="main-title">Meta Ads <span>Performance</span><br>Simulator</h1>
        <p class="subtitle">Real-time ROI projections based on your campaign inputs</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── KPI Metrics ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Key Performance Indicators</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(
        label="Estimated Clicks",
        value=f"{clicks:,.0f}",
        delta=f"Budget ÷ CPC",
    )
with col2:
    st.metric(
        label="Estimated Customers",
        value=f"{customers:.1f}",
        delta=f"CR: {conversion_rate}%",
    )
with col3:
    st.metric(
        label="CAC · Cost per Acquisition",
        value=f"₺{cac:,.0f}",
        delta="Lower is better",
        delta_color="inverse",
    )

col4, col5, col6 = st.columns(3)
with col4:
    st.metric(
        label="Total Revenue",
        value=f"₺{revenue:,.0f}",
        delta=f"{customers:.1f} conversions × ₺{avg_package:,}",
    )
with col5:
    profit_color = "normal" if net_profit >= 0 else "inverse"
    st.metric(
        label="Net Profit",
        value=f"₺{net_profit:,.0f}",
        delta="Revenue - Ad Spend",
        delta_color=profit_color,
    )
with col6:
    st.metric(
        label="ROAS",
        value=f"{roas:.2f}×",
        delta="Revenue ÷ Ad Spend",
        delta_color="normal" if roas >= 1 else "inverse",
    )

# ─── ROAS Interpretation ──────────────────────────────────────────────────────
if roas >= 3:
    roas_comment = "🟢 Excellent — Strong positive return"
elif roas >= 1:
    roas_comment = "🟡 Profitable — Room for optimization"
else:
    roas_comment = "🔴 Unprofitable — Revise your strategy"

st.markdown(f"""
<div class="roas-card">
    <div>
        <div class="roas-label">Return on Ad Spend</div>
        <div class="roas-value">{roas:.2f}×</div>
        <div class="roas-desc">{roas_comment}</div>
    </div>
    <div style="text-align:right;">
        <div style="font-family:'DM Mono',monospace;font-size:0.7rem;color:#6b7280;margin-bottom:6px;">FOR EVERY ₺1 SPENT</div>
        <div style="font-size:1.8rem;font-weight:800;color:#f0f2f7;">₺{roas:.2f}</div>
        <div style="font-family:'DM Mono',monospace;font-size:0.7rem;color:#6b7280;">RETURNED</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Budget Sensitivity Chart ─────────────────────────────────────────────────
st.markdown('<div class="section-title">Budget Sensitivity Analysis</div>', unsafe_allow_html=True)

budget_multipliers = np.array([0.25, 0.50, 0.75, 1.00, 1.25, 1.50, 1.75, 2.00])
labels = ["-75%", "-50%", "-25%", "Current", "+25%", "+50%", "+75%", "+100%"]

net_profits  = []
revenues_arr = []
customers_arr = []

for m in budget_multipliers:
    b        = budget * m
    cl       = (b / cpc) if cpc > 0 else 0
    cu       = cl * (conversion_rate / 100)
    rev      = cu * avg_package
    np_val   = rev - b
    net_profits.append(np_val)
    revenues_arr.append(rev)
    customers_arr.append(cu)

colors = ["#ff4d4d" if p < 0 else "#e8ff47" for p in net_profits]
current_idx = 3  # index for "Current"

fig = go.Figure()

# Revenue bars (background)
fig.add_trace(go.Bar(
    name="Total Revenue",
    x=labels,
    y=revenues_arr,
    marker_color=["rgba(255,107,53,0.25)" if i != current_idx else "rgba(255,107,53,0.45)"
                  for i in range(len(labels))],
    marker_line_width=0,
))

# Net Profit bars
fig.add_trace(go.Bar(
    name="Net Profit",
    x=labels,
    y=net_profits,
    marker_color=colors,
    marker_line_width=0,
    text=[f"₺{v:,.0f}" for v in net_profits],
    textposition="outside",
    textfont=dict(family="DM Mono, monospace", size=10, color="#f0f2f7"),
))

# Zero line
fig.add_hline(
    y=0,
    line_dash="dot",
    line_color="rgba(240,242,247,0.2)",
    line_width=1,
)

# Current budget marker (index 3 = "Current" label)
fig.add_shape(
    type="line",
    x0=current_idx, x1=current_idx,
    y0=0, y1=1,
    xref="x", yref="paper",
    line=dict(color="#e8ff47", width=1.5, dash="dash"),
)
fig.add_annotation(
    x=current_idx, y=1,
    xref="x", yref="paper",
    text="Current Budget",
    showarrow=False,
    font=dict(family="DM Mono, monospace", size=10, color="#e8ff47"),
    yanchor="bottom",
    xanchor="center",
)

fig.update_layout(
    barmode="overlay",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Syne, sans-serif", color="#f0f2f7"),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        font=dict(family="DM Mono, monospace", size=10),
        bgcolor="rgba(0,0,0,0)",
    ),
    margin=dict(l=0, r=0, t=40, b=0),
    height=380,
    xaxis=dict(
        gridcolor="rgba(255,255,255,0.04)",
        linecolor="rgba(255,255,255,0.08)",
        tickfont=dict(family="DM Mono, monospace", size=10),
    ),
    yaxis=dict(
        gridcolor="rgba(255,255,255,0.05)",
        linecolor="rgba(255,255,255,0.08)",
        tickformat="₺,.0f",
        tickfont=dict(family="DM Mono, monospace", size=10),
        zeroline=False,
    ),
)

st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ─── Customers vs Budget Line Chart ───────────────────────────────────────────
st.markdown('<div class="section-title">Customer Volume & Revenue Curve</div>', unsafe_allow_html=True)

col_a, col_b = st.columns(2)

with col_a:
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=labels,
        y=customers_arr,
        mode="lines+markers",
        line=dict(color="#e8ff47", width=2.5),
        marker=dict(
            size=[8 if i != current_idx else 14 for i in range(len(labels))],
            color=["#e8ff47" if i != current_idx else "#ff6b35" for i in range(len(labels))],
            line=dict(color="#0d0f14", width=2),
        ),
        fill="tozeroy",
        fillcolor="rgba(232,255,71,0.06)",
        name="Customers",
    ))
    fig2.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Syne, sans-serif", color="#f0f2f7"),
        margin=dict(l=0, r=0, t=16, b=0),
        height=240,
        showlegend=False,
        title=dict(text="Estimated Customers by Budget", font=dict(size=12, family="DM Mono, monospace", color="#6b7280")),
        xaxis=dict(gridcolor="rgba(255,255,255,0.04)", tickfont=dict(family="DM Mono, monospace", size=9)),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", tickfont=dict(family="DM Mono, monospace", size=9)),
    )
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

with col_b:
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(
        x=labels,
        y=revenues_arr,
        mode="lines+markers",
        line=dict(color="#ff6b35", width=2.5),
        marker=dict(
            size=[8 if i != current_idx else 14 for i in range(len(labels))],
            color=["#ff6b35" if i != current_idx else "#e8ff47" for i in range(len(labels))],
            line=dict(color="#0d0f14", width=2),
        ),
        fill="tozeroy",
        fillcolor="rgba(255,107,53,0.06)",
        name="Revenue",
    ))
    fig3.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Syne, sans-serif", color="#f0f2f7"),
        margin=dict(l=0, r=0, t=16, b=0),
        height=240,
        showlegend=False,
        title=dict(text="Total Revenue by Budget (₺)", font=dict(size=12, family="DM Mono, monospace", color="#6b7280")),
        xaxis=dict(gridcolor="rgba(255,255,255,0.04)", tickfont=dict(family="DM Mono, monospace", size=9)),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", tickformat="₺,.0f", tickfont=dict(family="DM Mono, monospace", size=9)),
    )
    st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

# ─── Scenario Summary Table ───────────────────────────────────────────────────
st.markdown('<div class="section-title">Scenario Breakdown Table</div>', unsafe_allow_html=True)

df = pd.DataFrame({
    "Budget Scenario": labels,
    "Ad Budget (₺)": [f"₺{budget * m:,.0f}" for m in budget_multipliers],
    "Estimated Clicks": [f"{((budget * m / cpc) if cpc > 0 else 0):,.0f}" for m in budget_multipliers],
    "Customers": [f"{c:.1f}" for c in customers_arr],
    "Revenue (₺)": [f"₺{r:,.0f}" for r in revenues_arr],
    "Net Profit (₺)": [f"₺{p:,.0f}" for p in net_profits],
    "ROAS": [f"{r / (budget * m):.2f}×" for m, r in zip(budget_multipliers, revenues_arr)],
})

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
)

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    META ADS SIMULATOR · CAMPAIGN PERFORMANCE DASHBOARD · BUILT WITH STREAMLIT + PLOTLY
</div>
""", unsafe_allow_html=True)
