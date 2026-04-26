from server import create_server
from client import run_simulation

import streamlit as st
import threading
import json
with open("enable.json", "w") as f:
    json.dump({"enabled": False}, f)
from random import randint
def create_test_clients(num_clients=10, choice = 1):
    requests = []
    for _ in range(num_clients):
        if choice == 1:
            requests_per_client = randint(1, 5)
        elif choice == 2:
            requests_per_client = randint(6, 10)
        else:
            requests_per_client = randint(10, 20)
        requests.append(requests_per_client)
    return requests

# ─────────────────────────── page config ───────────────────────────
st.set_page_config(
    page_title="Socket Simulation Lab",
    page_icon="⚡",
    layout="centered",
)

# ─────────────────────────── custom CSS ────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Syne:wght@400;700;800&display=swap');

:root {
    --bg:       #0d0f14;
    --surface:  #161a22;
    --border:   #262c38;
    --accent:   #00f5a0;
    --accent2:  #00b4d8;
    --danger:   #ff4d6d;
    --warn:     #ffd166;
    --text:     #e8ecf4;
    --muted:    #6b7a99;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text);
    font-family: 'Syne', sans-serif;
}

/* hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }

h1,h2,h3 { font-family: 'Syne', sans-serif; }

/* ── hero title ── */
.hero {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
}
.hero h1 {
    font-size: 2.6rem;
    font-weight: 800;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -1px;
    margin-bottom: .3rem;
}
.hero p { color: var(--muted); font-size: .95rem; }

/* ── card ── */
.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.6rem 1.8rem;
    margin-bottom: 1.2rem;
}
.card-title {
    font-size: .7rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 1rem;
}

/* ── status badge ── */
.badge {
    display: inline-flex;
    align-items: center;
    gap: .45rem;
    padding: .3rem .9rem;
    border-radius: 999px;
    font-family: 'JetBrains Mono', monospace;
    font-size: .78rem;
    font-weight: 600;
}
.badge-off  { background:#1e2230; color:var(--muted); border:1px solid var(--border); }
.badge-on   { background:#0d2e20; color:var(--accent); border:1px solid #1a5c40; }
.dot { width:7px;height:7px;border-radius:50%;display:inline-block; }
.dot-off { background:var(--muted); }
.dot-on  { background:var(--accent);
           box-shadow:0 0 6px var(--accent);
           animation: pulse 1.6s infinite; }
@keyframes pulse {
    0%,100% { opacity:1; }
    50%      { opacity:.4; }
}

/* ── stat tiles ── */
.stat-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: .85rem;
    margin-top: 1rem;
}
.stat-tile {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    text-align: center;
}
.stat-label {
    font-size: .68rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: .35rem;
}
.stat-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--accent);
}
.stat-value.danger { color: var(--danger); }
.stat-value.warn   { color: var(--warn); }

/* ── json viewer ── */
.json-block {
    background: #0a0c11;
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.2rem 1.4rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: .78rem;
    color: #a8b4cf;
    max-height: 420px;
    overflow-y: auto;
    white-space: pre-wrap;
    word-break: break-all;
    line-height: 1.65;
}

/* ── streamlit widget overrides ── */
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
    color: #0d0f14 !important;
    border: none !important;
    border-radius: 9px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: .92rem !important;
    padding: .6rem 1.8rem !important;
    transition: opacity .2s;
    width: 100%;
}
div[data-testid="stButton"] > button:hover { opacity: .82 !important; }
div[data-testid="stButton"] > button:disabled {
    background: var(--border) !important;
    color: var(--muted) !important;
    cursor: not-allowed !important;
}

/* radio + slider labels */
.stRadio label, .stSlider label,
div[data-testid="stRadio"] label,
div[data-testid="stSlider"] label {
    color: var(--text) !important;
    font-family: 'Syne', sans-serif !important;
}

div[data-testid="stRadio"] > div > label > div {
    color: var(--text) !important;
}

/* slider accent */
.stSlider [data-baseweb="slider"] [role="slider"] {
    background: var(--accent) !important;
    border-color: var(--accent) !important;
}

/* info / warning boxes */
.stAlert { border-radius: 10px !important; }

div[data-testid="stInfo"] {
    background: #0d2230 !important;
    border-left-color: var(--accent2) !important;
    color: var(--text) !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────── session state ─────────────────────────
if "server_running" not in st.session_state:
    st.session_state.server_running = False
if "stats" not in st.session_state:
    st.session_state.stats = None
if "sim_running" not in st.session_state:
    st.session_state.sim_running = False

# ─────────────────────────── helpers ───────────────────────────────
LEVEL_CONFIG = {
    1: {"label": "Low  (1–5 req / client)",  "min_clients": 1,  "max_clients": 5,  "req_range": "1–5"},
    2: {"label": "Mid  (6–10 req / client)", "min_clients": 6,  "max_clients": 10, "req_range": "6–10"},
    3: {"label": "High (10–20 req / client)","min_clients": 10, "max_clients": 20, "req_range": "10–20"},
}

def start_server():
    t = threading.Thread(target=create_server, daemon=True)
    t.start()
    st.session_state.server_running = True

# ─────────────────────────── layout ────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>⚡ Socket Simulation Lab</h1>
  <p>Spin up a threaded HTTP server, blast it with concurrent clients, inspect the results.</p>
</div>
""", unsafe_allow_html=True)

# ── 1. Server control ───────────────────────────────────────────────
st.markdown('<div class="card"><div class="card-title">01 — Server</div>', unsafe_allow_html=True)

col_badge, col_btn = st.columns([2, 1])
with col_badge:
    if st.session_state.server_running:
        st.markdown('<span class="badge badge-on"><span class="dot dot-on"></span>Running on 127.0.0.1:8000</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="badge badge-off"><span class="dot dot-off"></span>Stopped</span>', unsafe_allow_html=True)

with col_btn:
    if not st.session_state.server_running:
        if st.button("Start Server"):
            start_server()
            st.rerun()
    else:
        st.button("Server Active", disabled=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── 2. Simulation config ────────────────────────────────────────────
st.markdown('<div class="card"><div class="card-title">02 — Simulation Config</div>', unsafe_allow_html=True)

level = st.radio(
    "Traffic level",
    options=[1, 2, 3],
    format_func=lambda x: LEVEL_CONFIG[x]["label"],
    horizontal=True,
    disabled=not st.session_state.server_running,
)

cfg = LEVEL_CONFIG[level]
num_clients = st.slider(
    f"Number of clients  (clipped to {cfg['min_clients']}–{cfg['max_clients']})",
    min_value=1,
    max_value=20,
    value=cfg["min_clients"],
    disabled=not st.session_state.server_running,
)
# clip
clipped = max(cfg["min_clients"], min(cfg["max_clients"], num_clients))
if clipped != num_clients:
    st.info(f"⚠️ Value clipped to **{clipped}** (valid range for this level: {cfg['min_clients']}–{cfg['max_clients']})")

st.markdown('</div>', unsafe_allow_html=True)

# ── 3. Run ──────────────────────────────────────────────────────────
run_col, _ = st.columns([1, 2])
with run_col:
    run_clicked = st.button(
        "▶  Run Simulation",
        disabled=(not st.session_state.server_running or st.session_state.sim_running),
    )

if run_clicked:
    requests = create_test_clients(num_clients=clipped, choice=level)
    st.session_state.sim_running = True
    with st.spinner("Simulation in progress…"):
        result = run_simulation(requests , num_clients=clipped)
    #enable_security = True
    with open("enable.json", "w") as f:
        json.dump({"enabled": True}, f)
    st.session_state.stats = result
    st.session_state.sim_running = False
    st.rerun()

# ── 4. Results ──────────────────────────────────────────────────────
if st.session_state.stats:
    s = st.session_state.stats

    st.markdown('<div class="card"><div class="card-title">03 — Results</div>', unsafe_allow_html=True)

    total   = s.get("total_requests", 0)
    success = s.get("successful_requests", 0)
    failed  = s.get("failed_requests", 0)
    thru    = s.get("throughput", "—")
    elapsed = s.get("total_time", "—")

    st.markdown(f"""
    <div class="stat-grid">
      <div class="stat-tile">
        <div class="stat-label">Total Requests</div>
        <div class="stat-value">{total}</div>
      </div>
      <div class="stat-tile">
        <div class="stat-label">Successful</div>
        <div class="stat-value">{success}</div>
      </div>
      <div class="stat-tile">
        <div class="stat-label">Failed</div>
        <div class="stat-value {'danger' if failed > 0 else ''}">{failed}</div>
      </div>
      <div class="stat-tile">
        <div class="stat-label">Throughput</div>
        <div class="stat-value warn">{thru}</div>
      </div>
      <div class="stat-tile">
        <div class="stat-label">Total Time</div>
        <div class="stat-value">{elapsed}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Per-client table ────────────────────────────────────────────
    st.markdown('<div class="card-title">Client Breakdown</div>', unsafe_allow_html=True)

    meta_keys = {"total_requests", "total_time", "throughput", "successful_requests", "failed_requests"}
    client_ids = sorted([k for k in s.keys() if k not in meta_keys], key=lambda x: int(x))

    max_reqs = max(
        (s[cid].get("requests", 0) for cid in client_ids),
        default=0
    )

    def req_cell(req_data):
        if req_data is None:
            return '<td class="tc tc-empty">—</td>'
        lat  = req_data.get("latency", None)
        ok   = req_data.get("status", False)
        lat_s = f"{lat*1000:.0f} ms" if lat is not None else "?"
        cls  = "tc-ok" if ok else "tc-fail"
        icon = "✓" if ok else "✗"
        return f'<td class="tc {cls}"><span class="req-icon">{icon}</span>{lat_s}</td>'

    req_cols = "".join(f"<th>Latency {i+1}</th>" for i in range(max_reqs))
    header = f"""
    <tr>
      <th>Client</th>
      <th>Total Reqs</th>
      <th>✓ OK</th>
      <th>✗ Fail</th>
      {req_cols}
    </tr>"""

    rows_html = ""
    for cid in client_ids:
        cd         = s[cid]
        total_r    = cd.get("requests", 0)
        req_entries = {k: v for k, v in cd.items() if k.startswith("request_")}
        ok_count   = sum(1 for v in req_entries.values() if v.get("status"))
        fail_count = total_r - ok_count

        cells = ""
        for i in range(max_reqs):
            key  = f"request_{i+1}"
            data = req_entries.get(key, None)
            cells += req_cell(data) if i < total_r else '<td class="tc tc-empty">—</td>'

        rows_html += f"""
        <tr>
          <td class="tc-id">Client {cid}</td>
          <td class="tc-num">{total_r}</td>
          <td class="tc-ok-sum">{ok_count}</td>
          <td class="tc-fail-sum">{fail_count}</td>
          {cells}
        </tr>"""

    st.markdown(f"""
    <style>
    .client-table-wrap {{
        overflow-x: auto;
        margin-top: .5rem;
        border-radius: 10px;
        border: 1px solid var(--border);
    }}
    .client-table {{
        width: 100%;
        border-collapse: collapse;
        font-family: 'JetBrains Mono', monospace;
        font-size: .75rem;
    }}
    .client-table th {{
        background: #0d0f14;
        color: var(--muted);
        font-size: .65rem;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        padding: .6rem .9rem;
        text-align: center;
        border-bottom: 1px solid var(--border);
        white-space: nowrap;
    }}
    .client-table td {{
        padding: .5rem .75rem;
        text-align: center;
        border-bottom: 1px solid #1a1f2b;
        white-space: nowrap;
        color: var(--text);
    }}
    .client-table tr:last-child td {{ border-bottom: none; }}
    .client-table tr:hover td {{ background: #1a1f2b; }}
    .tc-id       {{ color: var(--accent2) !important; font-weight: 700; text-align: left !important; padding-left: 1rem !important; }}
    .tc-num      {{ color: var(--text); }}
    .tc-ok-sum   {{ color: var(--accent); font-weight: 600; }}
    .tc-fail-sum {{ color: var(--danger); font-weight: 600; }}
    .tc          {{ font-size: .72rem; }}
    .tc-ok       {{ color: var(--accent); }}
    .tc-fail     {{ color: var(--danger); }}
    .tc-empty    {{ color: #333a4d; }}
    .req-icon    {{ margin-right: 4px; font-weight: 700; }}
    </style>
    <div class="client-table-wrap">
      <table class="client-table">
        <thead>{header}</thead>
        <tbody>{rows_html}</tbody>
      </table>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.server_running:
    st.markdown("""
    <div style="text-align:center; color:#6b7a99; padding:2rem 0; font-size:.9rem;">
        Configure the simulation above and hit <strong style="color:#e8ecf4">▶ Run Simulation</strong>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="text-align:center; color:#6b7a99; padding:2rem 0; font-size:.9rem;">
        Start the server first to unlock the simulation controls.
    </div>
    """, unsafe_allow_html=True)
#py -m streamlit run ui.py