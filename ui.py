from server import create_server
from client import run_simulation

import streamlit as st
import threading
import json
import time

with open("enable.json", "w") as f:
    json.dump({"enabled": False}, f)

from random import randint

def create_test_clients(num_clients=10, choice=1):
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
    layout="wide",
)

# ─────────────────────────── CSS ────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Syne:wght@400;700;800&display=swap');

:root {
    --bg:      #0d0f14;
    --surface: #161a22;
    --border:  #262c38;
    --accent:  #00f5a0;
    --accent2: #00b4d8;
    --danger:  #ff4d6d;
    --warn:    #ffd166;
    --purple:  #c97dff;
    --text:    #e8ecf4;
    --muted:   #6b7a99;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text);
    font-family: 'Syne', sans-serif;
}
#MainMenu, footer, header { visibility: hidden; }
h1,h2,h3 { font-family: 'Syne', sans-serif; }

.hero { text-align: center; padding: 2.5rem 0 1.5rem; }
.hero h1 {
    font-size: 2.6rem; font-weight: 800;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    letter-spacing: -1px; margin-bottom: .3rem;
}
.hero p { color: var(--muted); font-size: .95rem; }

.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.6rem 1.8rem;
    margin-bottom: 1.2rem;
}
.card-title {
    font-size: .7rem; font-weight: 700;
    letter-spacing: 2px; text-transform: uppercase;
    color: var(--muted); margin-bottom: 1rem;
}

.badge {
    display: inline-flex; align-items: center; gap: .45rem;
    padding: .3rem .9rem; border-radius: 999px;
    font-family: 'JetBrains Mono', monospace;
    font-size: .78rem; font-weight: 600;
}
.badge-off { background:#1e2230; color:var(--muted); border:1px solid var(--border); }
.badge-on  { background:#0d2e20; color:var(--accent); border:1px solid #1a5c40; }
.dot { width:7px; height:7px; border-radius:50%; display:inline-block; }
.dot-off { background: var(--muted); }
.dot-on  { background: var(--accent); box-shadow: 0 0 6px var(--accent); animation: pulse 1.6s infinite; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.4} }

/* ── comparison stat grid ── */
.cmp-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    margin-bottom: 1.4rem;
}
.cmp-panel {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.1rem 1.3rem;
}
.cmp-panel.panel-plain  { border-top: 3px solid var(--accent2); }
.cmp-panel.panel-secure { border-top: 3px solid var(--purple); }
.cmp-header {
    font-size: .62rem; font-weight: 700; letter-spacing: 2px;
    text-transform: uppercase; margin-bottom: .9rem;
    display: flex; align-items: center; gap: .5rem;
}
.cmp-header.h-plain  { color: var(--accent2); }
.cmp-header.h-secure { color: var(--purple); }
.stat-row {
    display: flex; justify-content: space-between; align-items: center;
    padding: .35rem 0; border-bottom: 1px solid #1a1f2b;
}
.stat-row:last-child { border-bottom: none; }
.stat-row-label {
    font-size: .68rem; letter-spacing: 1px;
    text-transform: uppercase; color: var(--muted);
}
.stat-row-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: .95rem; font-weight: 700; color: var(--accent);
}
.stat-row-val.v-danger  { color: var(--danger); }
.stat-row-val.v-warn    { color: var(--warn); }
.stat-row-val.v-purple  { color: var(--purple); }
.stat-row-val.v-neutral { color: var(--text); }

/* delta badges */
.delta {
    font-family: 'JetBrains Mono', monospace;
    font-size: .6rem; font-weight: 700; padding: .1rem .4rem;
    border-radius: 4px; margin-left: .4rem;
}
.delta-up   { background: #0d2e20; color: var(--accent); }
.delta-down { background: #2e0d14; color: var(--danger); }
.delta-neu  { background: #1e2230; color: var(--muted); }

div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
    color: #0d0f14 !important; border: none !important;
    border-radius: 9px !important; font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important; font-size: .92rem !important;
    padding: .6rem 1.8rem !important; transition: opacity .2s; width: 100%;
}
div[data-testid="stButton"] > button:hover { opacity: .82 !important; }
div[data-testid="stButton"] > button:disabled {
    background: var(--border) !important; color: var(--muted) !important;
}

.stRadio label, .stSlider label,
div[data-testid="stRadio"] label,
div[data-testid="stSlider"] label {
    color: var(--text) !important; font-family: 'Syne', sans-serif !important;
}
div[data-testid="stRadio"] > div > label > div { color: var(--text) !important; }
.stSlider [data-baseweb="slider"] [role="slider"] {
    background: var(--accent) !important; border-color: var(--accent) !important;
}
.stAlert { border-radius: 10px !important; }
div[data-testid="stInfo"] {
    background: #0d2230 !important;
    border-left-color: var(--accent2) !important;
    color: var(--text) !important;
}

/* ── table styles ── */
.section-label {
    font-size: .65rem; font-weight: 700; letter-spacing: 2px;
    text-transform: uppercase; margin: 1.4rem 0 .55rem;
    display: flex; align-items: center; gap: .6rem; color: var(--muted);
}
.pill {
    padding: .18rem .65rem; border-radius: 999px;
    font-size: .6rem; font-weight: 700; letter-spacing: 1px;
}
.pill-plain  { background:#1e2230; color:#6b7a99; border:1px solid #262c38; }
.pill-secure { background:#1a0d20; color:var(--purple); border:1px solid #4a2260; }

.client-table-wrap {
    overflow-x: auto; border-radius: 10px;
    border: 1px solid var(--border); margin-bottom: 1.2rem;
}
.client-table-wrap.tbl-plain  { border-top: 3px solid var(--accent2); }
.client-table-wrap.tbl-secure { border-top: 3px solid var(--purple); }

.client-table {
    width: 100%; border-collapse: collapse;
    font-family: 'JetBrains Mono', monospace; font-size: .75rem;
}
.client-table th {
    background: #0d0f14; color: var(--muted);
    font-size: .63rem; letter-spacing: 1.5px; text-transform: uppercase;
    padding: .6rem .9rem; text-align: center;
    border-bottom: 1px solid var(--border); white-space: nowrap;
}
.client-table td {
    padding: .5rem .75rem; text-align: center;
    border-bottom: 1px solid #1a1f2b; white-space: nowrap; color: var(--text);
}
.client-table tr:last-child td { border-bottom: none; }
.client-table tr:hover td { background: #1a1f2b; }

.tc-id        { color: var(--accent2) !important; font-weight: 700;
                text-align: left !important; padding-left: 1rem !important; }
.tc-num       { color: var(--text); }
.tc-ok-sum    { color: var(--accent);  font-weight: 600; }
.tc-fail-sum  { color: var(--danger);  font-weight: 600; }
.tc-block-sum { color: var(--purple);  font-weight: 600; }
.tc           { font-size: .72rem; }
.tc-ok        { color: var(--accent); }
.tc-fail      { color: var(--danger); }
.tc-blocked   { color: var(--purple); }
.tc-empty     { color: #333a4d; }
.req-icon     { margin-right: 3px; font-weight: 700; }
.th-blocked   { color: var(--purple) !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────── session state ─────────────────────────
for key, default in [
    ("server_running", False),
    ("stats", None),
    ("stats1", None),
    ("sim_running", False),
]:
    if key not in st.session_state:
        st.session_state[key] = default

LEVEL_CONFIG = {
    1: {"label": "Low  (1–5 req / client)",   "min_clients": 1,  "max_clients": 5},
    2: {"label": "Mid  (6–10 req / client)",  "min_clients": 6,  "max_clients": 10},
    3: {"label": "High (10–20 req / client)", "min_clients": 10, "max_clients": 20},
}

def start_server():
    t = threading.Thread(target=create_server, daemon=True)
    t.start()
    time.sleep(0.3)
    st.session_state.server_running = True

# ─────────────────────────── layout ────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>⚡ Socket Simulation Lab</h1>
  <p>Two runs per click — plain first, then with rate limiting — compared side by side.</p>
</div>
""", unsafe_allow_html=True)

# ── 1. Server ───────────────────────────────────────────────────────
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

# ── 2. Config ───────────────────────────────────────────────────────
st.markdown('<div class="card"><div class="card-title">02 — Simulation Config</div>', unsafe_allow_html=True)
level = st.radio(
    "Traffic level", options=[1, 2, 3],
    format_func=lambda x: LEVEL_CONFIG[x]["label"],
    horizontal=True,
    disabled=not st.session_state.server_running,
)
cfg = LEVEL_CONFIG[level]
num_clients = st.slider(
    f"Number of clients  (clipped to {cfg['min_clients']}–{cfg['max_clients']})",
    min_value=1, max_value=20, value=cfg["min_clients"],
    disabled=not st.session_state.server_running,
)
clipped = max(cfg["min_clients"], min(cfg["max_clients"], num_clients))
if clipped != num_clients:
    st.info(f"⚠️ Value clipped to **{clipped}** (valid range: {cfg['min_clients']}–{cfg['max_clients']})")
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

    with st.spinner("Run 1/2 — no rate limiting…"):
        with open("enable.json", "w") as f:
            json.dump({"enabled": False}, f)
        result = run_simulation(requests, num_clients=clipped)

    with st.spinner("Run 2/2 — rate limiting active…"):
        with open("enable.json", "w") as f:
            json.dump({"enabled": True}, f)
        result1 = run_simulation(requests, num_clients=clipped)

    # reset to disabled after both runs
    with open("enable.json", "w") as f:
        json.dump({"enabled": False}, f)

    st.session_state.stats  = result
    st.session_state.stats1 = result1
    st.session_state.sim_running = False
    st.rerun()

# ── 4. Results ──────────────────────────────────────────────────────
if st.session_state.stats and st.session_state.stats1:
    r0 = st.session_state.stats   # plain run
    r1 = st.session_state.stats1  # secured run

    st.markdown('<div class="card"><div class="card-title">03 — Results</div>', unsafe_allow_html=True)

    # ── helper: delta badge ─────────────────────────────────────────
    def delta_badge(v0, v1, higher_is_better=True):
        """Compare a numeric from r1 vs r0 and return a coloured badge."""
        try:
            n0 = float(str(v0).split()[0])
            n1 = float(str(v1).split()[0])
            diff = n1 - n0
            if abs(diff) < 0.001:
                return '<span class="delta delta-neu">=</span>'
            sign  = "+" if diff > 0 else ""
            good  = (diff > 0) == higher_is_better
            cls   = "delta-up" if good else "delta-down"
            unit  = " ms" if "ms" in str(v0) else (" req/s" if "req" in str(v0) else "")
            return f'<span class="delta {cls}">{sign}{diff:.1f}{unit}</span>'
        except Exception:
            return ""

    def stat_row(label, v0, v1, cls0="", cls1="", higher_is_better=True):
        badge = delta_badge(v0, v1, higher_is_better)
        return f"""
        <div class="stat-row">
          <span class="stat-row-label">{label}</span>
          <span>
            <span class="stat-row-val {cls0}">{v0}</span>
            <span style="color:var(--muted);font-size:.7rem;margin:0 .4rem">→</span>
            <span class="stat-row-val {cls1}">{v1}</span>
            {badge}
          </span>
        </div>"""

    total0  = r0.get("total_requests", 0)
    succ0   = r0.get("successful_requests", 0)
    fail0   = r0.get("failed_requests", 0)
    thru0   = r0.get("throughput", "—")
    time0   = r0.get("total_time", "—")

    total1  = r1.get("total_requests", 0)
    succ1   = r1.get("successful_requests", 0)
    fail1   = r1.get("failed_requests", 0)
    thru1   = r1.get("throughput", "—")
    time1   = r1.get("total_time", "—")

    st.markdown(f"""
    <div class="cmp-grid">

      <div class="cmp-panel panel-plain">
        <div class="cmp-header h-plain">① No Rate Limiting</div>
        <div class="stat-row">
          <span class="stat-row-label">Total Requests</span>
          <span class="stat-row-val v-neutral">{total0}</span>
        </div>
        <div class="stat-row">
          <span class="stat-row-label">Successful</span>
          <span class="stat-row-val">{succ0}</span>
        </div>
        <div class="stat-row">
          <span class="stat-row-label">Failed</span>
          <span class="stat-row-val {'v-danger' if fail0 > 0 else 'v-neutral'}">{fail0}</span>
        </div>
        <div class="stat-row">
          <span class="stat-row-label">Throughput</span>
          <span class="stat-row-val v-warn">{thru0}</span>
        </div>
        <div class="stat-row">
          <span class="stat-row-label">Total Time</span>
          <span class="stat-row-val v-neutral">{time0}</span>
        </div>
      </div>

      <div class="cmp-panel panel-secure">
        <div class="cmp-header h-secure">② Rate Limiting Active</div>
        <div class="stat-row">
          <span class="stat-row-label">Total Requests</span>
          <span class="stat-row-val v-neutral">{total1}</span>
        </div>
        <div class="stat-row">
          <span class="stat-row-label">Successful</span>
          <span class="stat-row-val">{succ1}</span>
        </div>
        <div class="stat-row">
          <span class="stat-row-label">Failed</span>
          <span class="stat-row-val {'v-danger' if fail1 > 0 else 'v-neutral'}">{fail1}</span>
        </div>
        <div class="stat-row">
          <span class="stat-row-label">Throughput</span>
          <span class="stat-row-val v-warn">{thru1}</span>
        </div>
        <div class="stat-row">
          <span class="stat-row-label">Total Time</span>
          <span class="stat-row-val v-neutral">{time1}</span>
        </div>
      </div>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── shared helpers ───────────────────────────────────────────────
    META = {"total_requests", "total_time", "throughput", "successful_requests", "failed_requests"}

    def get_client_ids(s):
        return sorted([k for k in s.keys() if k not in META], key=lambda x: int(x))

    def req_cell(req_data, show_blocked):
        empty = '<td class="tc tc-empty">—</td>'
        if req_data is None:
            return (empty + empty) if show_blocked else empty
        lat     = req_data.get("latency", None)
        ok      = req_data.get("status", False)
        blocked = req_data.get("blocked", False)
        lat_s   = f"{lat*1000:.0f} ms" if lat is not None else "?"
        if show_blocked and blocked:
            s_cls, icon = "tc-blocked", "⊘"
        elif ok:
            s_cls, icon = "tc-ok", "✓"
        else:
            s_cls, icon = "tc-fail", "✗"
        lat_td = f'<td class="tc {s_cls}"><span class="req-icon">{icon}</span>{lat_s}</td>'
        if show_blocked:
            b_cls  = "tc-blocked" if blocked else "tc-empty"
            b_text = "⊘ yes" if blocked else "—"
            return lat_td + f'<td class="tc {b_cls}" style="font-size:.68rem">{b_text}</td>'
        return lat_td

    def build_table(s, show_blocked, tbl_cls=""):
        client_ids = get_client_ids(s)
        max_reqs   = max((s[cid].get("requests", 0) for cid in client_ids), default=0)
        empty      = '<td class="tc tc-empty">—</td>'

        req_th = ""
        for i in range(max_reqs):
            req_th += f"<th>Latency {i+1}</th>"
            if show_blocked:
                req_th += f'<th class="th-blocked">Blocked {i+1}</th>'

        blk_th = '<th class="th-blocked">⊘ Blocked</th>' if show_blocked else ""
        header = f"<tr><th>Client</th><th>Total Reqs</th><th>✓ OK</th><th>✗ Fail</th>{blk_th}{req_th}</tr>"

        rows = ""
        for cid in client_ids:
            cd          = s[cid]
            total_r     = cd.get("requests", 0)
            req_entries = {k: v for k, v in cd.items() if k.startswith("request_")}
            ok_count    = sum(1 for v in req_entries.values() if v.get("status"))
            blk_count   = sum(1 for v in req_entries.values() if v.get("blocked", False))
            fail_count  = total_r - ok_count

            cells = ""
            for i in range(max_reqs):
                key  = f"request_{i+1}"
                data = req_entries.get(key, None)
                cells += req_cell(data, show_blocked) if i < total_r else (
                    (empty + empty) if show_blocked else empty
                )

            blk_td = f'<td class="tc-block-sum">{blk_count}</td>' if show_blocked else ""
            rows += (
                f"<tr>"
                f'<td class="tc-id">Client {cid}</td>'
                f'<td class="tc-num">{total_r}</td>'
                f'<td class="tc-ok-sum">{ok_count}</td>'
                f'<td class="tc-fail-sum">{fail_count}</td>'
                f"{blk_td}{cells}"
                f"</tr>"
            )

        return (
            f'<div class="client-table-wrap {tbl_cls}">'
            f'<table class="client-table">'
            f"<thead>{header}</thead>"
            f"<tbody>{rows}</tbody>"
            f"</table></div>"
        )

    # ── Table 1 — plain run ─────────────────────────────────────────
    st.markdown("""
    <div class="section-label">
      ① Client Breakdown
      <span class="pill pill-plain">No Rate Limiting</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(build_table(r0, show_blocked=False, tbl_cls="tbl-plain"), unsafe_allow_html=True)

    # ── Table 2 — secured run ───────────────────────────────────────
    st.markdown("""
    <div class="section-label">
      ② Security View
      <span class="pill pill-secure">⚙ Rate Limiting Active</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(build_table(r1, show_blocked=True, tbl_cls="tbl-secure"), unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.server_running:
    st.markdown("""
    <div style="text-align:center;color:#6b7a99;padding:2rem 0;font-size:.9rem;">
        Configure the simulation above and hit <strong style="color:#e8ecf4">▶ Run Simulation</strong>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="text-align:center;color:#6b7a99;padding:2rem 0;font-size:.9rem;">
        Start the server first to unlock the simulation controls.
    </div>
    """, unsafe_allow_html=True)

# py -m streamlit run ui.py