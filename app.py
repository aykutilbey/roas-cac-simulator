import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Meta Ads Simulator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Syne:wght@400;600;700;800&display=swap');

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

/* Hide all streamlit chrome */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stSidebarCollapseButton"],
[data-testid="collapsedControl"] {
    display: none !important;
    visibility: hidden !important;
}

/* Number inputs */
[data-testid="stNumberInput"] label {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
}

[data-testid="stNumberInput"] input {
    background: var(--bg) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 1rem !important;
}

[data-testid="stNumberInput"] input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(232,255,71,0.12) !important;
}

[data-testid="stNumberInput"] button {
    background: var(--border) !important;
    border: none !important;
    color: var(--text) !important;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 20px !important;
    transition: border-color 0.2s ease !important;
}

[data-testid="stMetric"]:hover {
    border-color: var(--accent) !important;
}

[data-testid="stMetricLabel"] > div {
    color: var(--muted) !important;
    font-size: 0.7rem !important;
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
    font-size: 0.72rem !important;
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

/* ROAS card */
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

hr {
    border: none;
    border-top: 1px solid var(--border) !important;
    margin: 1.5rem 0 !important;
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
    margin: 0 0 6px 0;
    color: var(--text);
}

.main-title span { color: var(--accent); }

.subtitle {
    color: var(--muted);
    font-size: 0.85rem;
    font-family: 'DM Mono', monospace;
    margin-bottom: 28px;
}

.input-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 14px;
}

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

[data-testid="column"] { padding: 0 8px !important; }
</style>
""", unsafe_allow_html=True)

# ─── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="badge">META ADS · CAMPAIGN DASHBOARD</div>
<h1 class="main-title">Meta Ads <span>Performance</span> Simulator</h1>
<p class="subtitle">Real-time ROI projections — enter your campaign inputs below</p>
""", unsafe_allow_html=True)

# ─── Input Row ────────────────────────────────────────────────────────────────
st.markdown('<div class="input-label">📋 Campaign Parameters</div>', unsafe_allow_html=True)

col_i1, col_i2, col_i3, col_i4 = st.columns(4)

with col_i1:
    budget = st.number_input(
        "Monthly Ad Budget (₺)",
        min_value=0, max_value=10_000_000,
        value=10_000, step=1_000,
    )
with col_i2:
    cpc = st.number_input(
        "Cost Per Click / CPC (₺)",
        min_value=0.0, max_value=100_000.0,
        value=5.0, step=0.1, format="%.2f",
    )
with col_i3:
    conversion_rate = st.number_input(
        "Conversion Rate (%)",
        min_value=0.0, max_value=100.0,
        value=2.5, step=0.1, format="%.2f",
    )
with col_i4:
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

# ─── KPI Metrics ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Key Performance Indicators</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Estimated Clicks", f"{clicks:,.0f}", "Budget ÷ CPC")
with col2:
    st.metric("Estimated Customers", f"{customers:.1f}", f"CR: {conversion_rate}%")
with col3:
    st.metric("CAC · Cost per Acquisition", f"₺{cac:,.0f}", "Lower is better", delta_color="inverse")

col4, col5, col6 = st.columns(3)
with col4:
    st.metric("Total Revenue", f"₺{revenue:,.0f}", f"{customers:.1f} conversions × ₺{avg_package:,}")
with col5:
    st.metric("Net Profit", f"₺{net_profit:,.0f}", "Revenue − Ad Spend",
              delta_color="normal" if net_profit >= 0 else "inverse")
with col6:
    st.metric("ROAS", f"{roas:.2f}×", "Revenue ÷ Ad Spend",
              delta_color="normal" if roas >= 1 else "inverse")

# ─── ROAS Card ────────────────────────────────────────────────────────────────
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

net_profits_arr = []
revenues_arr    = []
customers_arr   = []

for m in budget_multipliers:
    b   = budget * m
    cl  = (b / cpc) if cpc > 0 else 0
    cu  = cl * (conversion_rate / 100)
    rev = cu * avg_package
    net_profits_arr.append(rev - b)
    revenues_arr.append(rev)
    customers_arr.append(cu)

current_idx = 3
colors = ["#ff4d4d" if p < 0 else "#e8ff47" for p in net_profits_arr]

fig = go.Figure()

fig.add_trace(go.Bar(
    name="Total Revenue",
    x=labels, y=revenues_arr,
    marker_color=["rgba(255,107,53,0.25)" if i != current_idx else "rgba(255,107,53,0.5)"
                  for i in range(len(labels))],
    marker_line_width=0,
))

fig.add_trace(go.Bar(
    name="Net Profit",
    x=labels, y=net_profits_arr,
    marker_color=colors,
    marker_line_width=0,
    text=[f"₺{v:,.0f}" for v in net_profits_arr],
    textposition="outside",
    textfont=dict(family="DM Mono, monospace", size=10, color="#f0f2f7"),
))

fig.add_hline(y=0, line_dash="dot", line_color="rgba(240,242,247,0.2)", line_width=1)

fig.add_shape(
    type="line",
    x0=current_idx - 0.5, x1=current_idx - 0.5,
    y0=0, y1=1, xref="x", yref="paper",
    line=dict(color="#e8ff47", width=1.5, dash="dash"),
)
fig.add_annotation(
    x=current_idx, y=1, xref="x", yref="paper",
    text="◀ Current Budget",
    showarrow=False,
    font=dict(family="DM Mono, monospace", size=10, color="#e8ff47"),
    yanchor="bottom", xanchor="left",
)

fig.update_layout(
    barmode="overlay",
    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Syne, sans-serif", color="#f0f2f7"),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                font=dict(family="DM Mono, monospace", size=10), bgcolor="rgba(0,0,0,0)"),
    margin=dict(l=0, r=0, t=40, b=0),
    height=380,
    xaxis=dict(gridcolor="rgba(255,255,255,0.04)", linecolor="rgba(255,255,255,0.08)",
               tickfont=dict(family="DM Mono, monospace", size=10)),
    yaxis=dict(gridcolor="rgba(255,255,255,0.05)", linecolor="rgba(255,255,255,0.08)",
               tickformat="₺,.0f", tickfont=dict(family="DM Mono, monospace", size=10), zeroline=False),
)

st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ─── Line Charts ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Customer Volume & Revenue Curve</div>', unsafe_allow_html=True)

col_a, col_b = st.columns(2)

for col, y_data, color, fill_color, title, tick_fmt in [
    (col_a, customers_arr, "#e8ff47", "rgba(232,255,71,0.06)", "Estimated Customers by Budget", ",.1f"),
    (col_b, revenues_arr,  "#ff6b35", "rgba(255,107,53,0.06)", "Total Revenue by Budget (₺)", "₺,.0f"),
]:
    with col:
        f = go.Figure()
        alt_color = "#ff6b35" if color == "#e8ff47" else "#e8ff47"
        f.add_trace(go.Scatter(
            x=labels, y=y_data,
            mode="lines+markers",
            line=dict(color=color, width=2.5),
            marker=dict(
                size=[8 if i != current_idx else 14 for i in range(len(labels))],
                color=[color if i != current_idx else alt_color for i in range(len(labels))],
                line=dict(color="#0d0f14", width=2),
            ),
            fill="tozeroy", fillcolor=fill_color,
        ))
        f.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Syne, sans-serif", color="#f0f2f7"),
            margin=dict(l=0, r=0, t=16, b=0), height=240, showlegend=False,
            title=dict(text=title, font=dict(size=11, family="DM Mono, monospace", color="#6b7280")),
            xaxis=dict(gridcolor="rgba(255,255,255,0.04)", tickfont=dict(family="DM Mono, monospace", size=9)),
            yaxis=dict(gridcolor="rgba(255,255,255,0.05)", tickfont=dict(family="DM Mono, monospace", size=9),
                       tickformat=tick_fmt),
        )
        st.plotly_chart(f, use_container_width=True, config={"displayModeBar": False})

# ─── Scenario Table ───────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Scenario Breakdown Table</div>', unsafe_allow_html=True)

df = pd.DataFrame({
    "Budget Scenario":  labels,
    "Ad Budget (₺)":    [f"₺{budget * m:,.0f}" for m in budget_multipliers],
    "Estimated Clicks": [f"{((budget * m / cpc) if cpc > 0 else 0):,.0f}" for m in budget_multipliers],
    "Customers":        [f"{c:.1f}" for c in customers_arr],
    "Revenue (₺)":      [f"₺{r:,.0f}" for r in revenues_arr],
    "Net Profit (₺)":   [f"₺{p:,.0f}" for p in net_profits_arr],
    "ROAS":             [f"{(r / (budget * m)):.2f}×" if budget * m > 0 else "—"
                         for m, r in zip(budget_multipliers, revenues_arr)],
})

st.dataframe(df, use_container_width=True, hide_index=True)

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    META ADS SIMULATOR · CAMPAIGN PERFORMANCE DASHBOARD · BUILT WITH STREAMLIT + PLOTLY
</div>
""", unsafe_allow_html=True)
