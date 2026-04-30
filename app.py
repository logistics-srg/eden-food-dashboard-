import streamlit as st
import pandas as pd
from datetime import datetime, date
import plotly.express as px
import base64
import os
import streamlit.components.v1 as components

st.set_page_config(page_title="EDEN FOOD", page_icon="🍌",
                   layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
header[data-testid="stHeader"],#MainMenu,.stAppDeployButton,footer{display:none!important}
*{font-family:'Inter',sans-serif!important;box-sizing:border-box}
.block-container{padding:0!important;max-width:100%!important}
.stApp{background:#F4F6FB!important}
:root{
  --primary:#4361EE;--primary-light:#EEF2FF;--success:#10B981;--success-light:#D1FAE5;
  --warning:#F59E0B;--warning-light:#FEF3C7;--danger:#EF4444;--danger-light:#FEE2E2;
  --info:#3B82F6;--info-light:#DBEAFE;--surface:#FFFFFF;--surface-2:#F9FAFB;
  --border:#E5E7EB;--text-primary:#111827;--text-secondary:#6B7280;--text-muted:#9CA3AF;
  --shadow-sm:0 1px 2px rgba(0,0,0,0.05);
  --shadow-md:0 4px 6px -1px rgba(0,0,0,0.07),0 2px 4px -1px rgba(0,0,0,0.04);
  --shadow-lg:0 10px 15px -3px rgba(0,0,0,0.08),0 4px 6px -2px rgba(0,0,0,0.04);
  --radius-sm:8px;--radius-md:12px;--radius-lg:16px;--radius-xl:24px;--radius-full:9999px;
  --transition:all 0.2s cubic-bezier(0.4,0,0.2,1);
}
section[data-testid="stSidebar"]{
  transform:none!important;min-width:240px!important;max-width:240px!important;
  background:var(--surface)!important;border-right:1px solid var(--border)!important;
  box-shadow:var(--shadow-md)!important;visibility:visible!important;display:block!important;
}
section[data-testid="stSidebarCollapsedControl"]{display:none!important;width:0!important}
[data-testid="collapsedControl"]{display:none!important}
section[data-testid="stSidebar"] button[data-testid="baseButton-headerNoPadding"]{display:none!important}
section[data-testid="stSidebar"] *{font-family:'Inter',sans-serif!important}
section[data-testid="stSidebar"] .stButton>button{
  background:transparent!important;border:none!important;color:var(--text-secondary)!important;
  text-align:left!important;width:100%!important;padding:10px 14px!important;
  border-radius:var(--radius-sm)!important;font-size:13.5px!important;font-weight:500!important;
  transition:var(--transition)!important;margin-bottom:1px!important;
}
section[data-testid="stSidebar"] .stButton>button:hover{
  background:var(--primary-light)!important;color:var(--primary)!important;transform:translateX(2px)!important;
}
.topbar{background:var(--surface);border-bottom:1px solid var(--border);padding:18px 36px;
  display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:100;}
.topbar-title{font-size:20px;font-weight:800;color:var(--text-primary);letter-spacing:-0.5px}
.topbar-badge{background:var(--primary-light);color:var(--primary);padding:4px 12px;
  border-radius:var(--radius-full);font-size:11px;font-weight:700;}
.main-wrap{padding:28px 36px;max-width:1500px;margin:0 auto}
.kpi-grid{display:grid;grid-template-columns:repeat(6,1fr);gap:14px;margin-bottom:28px}
.kpi-card{background:var(--surface);border-radius:var(--radius-lg);padding:20px 18px;
  border:1px solid var(--border);box-shadow:var(--shadow-sm);position:relative;overflow:hidden;
  transition:var(--transition);cursor:default;}
.kpi-card::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;
  border-radius:var(--radius-lg) var(--radius-lg) 0 0;
  background:linear-gradient(90deg,var(--card-color,#4361EE),transparent);}
.kpi-card:hover{transform:translateY(-3px);box-shadow:var(--shadow-lg);border-color:rgba(67,97,238,0.15)}
.kpi-card .icon-wrap{width:38px;height:38px;border-radius:10px;display:flex;align-items:center;
  justify-content:center;font-size:18px;margin-bottom:12px;background:var(--card-bg,var(--primary-light));}
.kpi-card .kpi-val{font-size:2rem;font-weight:900;letter-spacing:-1.5px;line-height:1;margin-bottom:3px}
.kpi-card .kpi-lbl{font-size:10px;color:var(--text-muted);text-transform:uppercase;letter-spacing:1px;font-weight:700;margin-bottom:4px}
.kpi-card .kpi-sub{font-size:11px;color:var(--text-muted)}
.sec-hdr{display:flex;align-items:center;justify-content:space-between;margin:28px 0 14px;
  padding-bottom:12px;border-bottom:1px solid var(--border);}
.sec-title{font-size:14px;font-weight:700;color:var(--text-primary)}
.sec-sub{font-size:12px;color:var(--text-muted)}
.cmd-row{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius-md);
  padding:14px 18px;margin-bottom:6px;display:flex;align-items:center;
  justify-content:space-between;flex-wrap:wrap;gap:10px;transition:var(--transition);position:relative;}
.cmd-row::before{content:'';position:absolute;left:0;top:50%;transform:translateY(-50%);
  width:3px;height:0;border-radius:0 2px 2px 0;background:var(--primary);
  transition:all 0.35s cubic-bezier(0.4,0,0.2,1);}
.cmd-row:hover{box-shadow:var(--shadow-md);border-color:rgba(67,97,238,0.2);transform:translateX(2px)}
.cmd-row:hover::before{height:60%}
.pill{display:inline-flex;align-items:center;gap:5px;padding:4px 12px;
  border-radius:var(--radius-full);font-size:11px;font-weight:700;letter-spacing:0.2px}
.pill-green{background:var(--success-light);color:#065F46}
.pill-orange{background:var(--warning-light);color:#92400E}
.pill-red{background:var(--danger-light);color:#991B1B}
.pill-blue{background:var(--info-light);color:#1E40AF}
.card{background:var(--surface);border-radius:var(--radius-lg);padding:22px 24px;
  border:1px solid var(--border);box-shadow:var(--shadow-sm);margin-bottom:12px;transition:var(--transition);}
.card:hover{box-shadow:var(--shadow-md)}
.hero-wrap{position:relative;width:100%;height:320px;overflow:hidden;
  background-size:cover!important;background-position:center 50%!important;background-repeat:no-repeat!important;}
.hero-overlay{position:absolute;inset:0;
  background:linear-gradient(110deg,rgba(10,15,30,0.88) 0%,rgba(67,97,238,0.42) 55%,rgba(0,0,0,0.1) 100%);
  display:flex;align-items:center;padding:0 52px;}
.hero-text h1{font-size:34px;font-weight:900;color:#fff;letter-spacing:-1.2px;line-height:1.15;margin:0 0 10px}
.hero-text p{font-size:14px;color:rgba(255,255,255,0.78);max-width:440px;line-height:1.65;margin:0 0 22px}
.hero-badge{display:inline-flex;align-items:center;gap:7px;background:rgba(255,255,255,0.12);
  backdrop-filter:blur(12px);border:1px solid rgba(255,255,255,0.22);
  color:#fff;padding:7px 18px;border-radius:var(--radius-full);font-size:12px;font-weight:600;}
.alert{padding:11px 15px;border-radius:var(--radius-sm);font-size:12px;font-weight:600;margin:6px 0}
.alert-ok{background:var(--success-light);border-left:3px solid var(--success);color:#065F46}
.alert-warn{background:var(--warning-light);border-left:3px solid var(--warning);color:#92400E}
.alert-red{background:var(--danger-light);border-left:3px solid var(--danger);color:#991B1B}
.prog-track{background:#E5E7EB;border-radius:var(--radius-full);height:5px;overflow:hidden}
.prog-fill{height:100%;border-radius:var(--radius-full)}
.doc-zone{background:var(--surface-2);border:1.5px dashed #D1D5DB;border-radius:var(--radius-md);padding:18px}
.doc-chip{display:inline-flex;align-items:center;gap:5px;background:#fff;border:1px solid var(--border);
  border-radius:6px;padding:5px 10px;font-size:11px;color:var(--text-secondary);font-weight:500;margin:3px;}
div[data-testid="stForm"]{background:var(--surface)!important;border-radius:var(--radius-lg)!important;
  padding:26px!important;border:1px solid var(--border)!important;box-shadow:none!important;}
div[data-testid="stDataFrame"]{border-radius:var(--radius-md)!important;overflow:hidden!important}
hr{border:none!important;border-top:1px solid var(--border)!important;margin:16px 0!important}
::-webkit-scrollbar{width:5px;height:5px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:#D1D5DB;border-radius:var(--radius-full)}

/* ── TRACKING ── */
.track-card{background:var(--surface);border-radius:var(--radius-lg);border:1px solid var(--border);
  box-shadow:var(--shadow-sm);margin-bottom:14px;overflow:hidden;transition:var(--transition);cursor:pointer;}
.track-card:hover{box-shadow:var(--shadow-lg);transform:translateY(-2px)}
.track-header{padding:18px 22px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px}
.track-route{padding:0 22px 18px;overflow-x:auto}
.stage-dot{width:30px;height:30px;border-radius:50%;display:flex;align-items:center;justify-content:center;
  font-size:12px;transition:all 0.4s cubic-bezier(0.34,1.56,0.64,1);flex-shrink:0}
.stage-line{flex:1;height:2px;min-width:24px;position:relative;overflow:hidden}
.stage-line-fill{position:absolute;left:0;top:0;height:100%;border-radius:2px;transition:width 1.2s cubic-bezier(0.4,0,0.2,1)}
@keyframes shipPulse{0%,100%{transform:scale(1)}50%{transform:scale(1.15)}}
.ship-active{animation:shipPulse 2s ease-in-out infinite}
</style>
""", unsafe_allow_html=True)

# ── USERS ─────────────────────────────────────────────────────────────────────
USERS = {
    "yann":     {"password": "EdenFood2026!",  "role": "admin"},
    "eden":     {"password": "Eden@Logistik",   "role": "user"},
    "srg":      {"password": "SRG@Trading1",    "role": "user"},
    "edenfood": {"password": "Edenfood@2026",   "role": "user"},
}

for k, v in {"authenticated": False, "username": "", "role": "",
             "page": "dashboard", "new_commandes": [], "expanded_cmd": None,
             "expanded_track": set()}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── HELPERS ───────────────────────────────────────────────────────────────────
def img_to_b64(path):
    try:
        ext  = path.split(".")[-1].lower()
        mime = "jpeg" if ext in ["jpg","jpeg"] else "png"
        return f"data:image/{mime};base64,{base64.b64encode(open(path,'rb').read()).decode()}"
    except:
        return None

def apply_chart_style(fig, bgcolor="#fff"):
    fig.update_layout(
        paper_bgcolor=bgcolor, plot_bgcolor=bgcolor,
        font=dict(family="Inter", size=12, color="#111827"),
        margin=dict(t=20, b=20, l=20, r=20),
        legend=dict(font=dict(color="#111827", size=12))
    )
    fig.update_xaxes(tickfont=dict(color="#6B7280"), showgrid=False, linecolor="#E5E7EB")
    fig.update_yaxes(tickfont=dict(color="#6B7280"), gridcolor="#F3F4F6", linecolor="#F3F4F6")
    return fig

# ── DOCUMENTS ─────────────────────────────────────────────────────────────────
DOCS_ROOT = "docs"
DOC_TYPES = ["BL Draft","BL Original","Phytosanitaire","Certificat Origine",
             "Facture Proforma","Packing List","Licence DPVCT","Autre"]

def docs_path(booking):
    p = os.path.join(DOCS_ROOT, str(booking).replace("/","_").replace(" ","_"))
    os.makedirs(p, exist_ok=True)
    return p

def list_docs(booking):
    p = docs_path(booking)
    return [f for f in os.listdir(p) if not f.startswith(".")] if os.path.exists(p) else []

def save_doc(booking, uploaded_file):
    fp = os.path.join(docs_path(booking), uploaded_file.name)
    with open(fp, "wb") as f:
        f.write(uploaded_file.getbuffer())

def delete_doc(booking, filename):
    fp = os.path.join(docs_path(booking), filename)
    if os.path.exists(fp):
        os.remove(fp)

# ══════════════════════════════════════════════════════════════════════════════
# TRACKING HELPERS
# ══════════════════════════════════════════════════════════════════════════════
# Étapes avec durée cumulée en jours depuis le départ
TRANSIT_STAGES = [
    {"id": "plantation",   "icon": "🌿", "label": "Plantation",     "days": -3,  "color": "#6B7280"},
    {"id": "port_depart",  "icon": "⚓", "label": "Port départ",    "days": 0,   "color": "#4361EE"},
    {"id": "atlantique",   "icon": "🌊", "label": "Atlantique",     "days": 3,   "color": "#3B82F6"},
    {"id": "gibraltar",    "icon": "🏛️", "label": "Gibraltar",      "days": 14,  "color": "#8B5CF6"},
    {"id": "mediterranee", "icon": "🌊", "label": "Méditerranée",   "days": 17,  "color": "#0EA5E9"},
    {"id": "ghazaouet",    "icon": "⚓", "label": "Ghazaouet 🇩🇿",  "days": 21,  "color": "#10B981"},
]
TOTAL_DAYS = 21  # durée totale approximative


def parse_depart(depart_str):
    for fmt in ["%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%Y/%m/%d"]:
        try:
            return datetime.strptime(str(depart_str).strip(), fmt).date()
        except:
            continue
    return None


def get_tracking_info(depart_str):
    """Retourne (stage_idx, progress_pct, days_elapsed, eta_arrive)"""
    dep = parse_depart(depart_str)
    if not dep:
        return 0, 0, None, None

    today = date.today()
    days_elapsed = (today - dep).days
    eta = dep + __import__("datetime").timedelta(days=TOTAL_DAYS)

    # Trouver l'étape actuelle
    stage_idx = 0
    for i, s in enumerate(TRANSIT_STAGES):
        if days_elapsed >= s["days"]:
            stage_idx = i

    # Progression globale (0-100%)
    if days_elapsed < TRANSIT_STAGES[0]["days"]:
        progress = 0.0
    elif days_elapsed >= TOTAL_DAYS:
        progress = 100.0
    else:
        progress = min(100.0, max(0.0, days_elapsed / TOTAL_DAYS * 100))

    return stage_idx, progress, days_elapsed, eta


def build_stage_timeline_html(stage_idx, progress, pol):
    """Génère le HTML de la timeline des étapes"""
    html = '<div style="display:flex;align-items:center;padding:14px 0;gap:0;min-width:600px">'

    for i, s in enumerate(TRANSIT_STAGES):
        # Statut du dot
        is_done    = i < stage_idx
        is_current = i == stage_idx
        is_future  = i > stage_idx

        if is_done:
            dot_bg    = "#10B981"
            dot_border = "#10B981"
            dot_shadow = ""
            dot_content = "✓"
            lbl_color  = "#10B981"
            lbl_weight = "600"
        elif is_current:
            dot_bg    = s["color"]
            dot_border = s["color"]
            dot_shadow = f"box-shadow:0 0 0 4px {s['color']}22,0 0 12px {s['color']}44"
            dot_content = s["icon"]
            lbl_color  = s["color"]
            lbl_weight = "800"
        else:
            dot_bg    = "#F9FAFB"
            dot_border = "#E5E7EB"
            dot_shadow = ""
            dot_content = s["icon"]
            lbl_color  = "#9CA3AF"
            lbl_weight = "500"

        label = s["label"]
        if i == 0:
            flag = "🇨🇷" if "COSTA" in pol.upper() else "🇨🇴"
            label = f"{flag} {pol.split('(')[0].strip()[:5]}"

        anim = 'class="ship-active"' if is_current and i not in [0, 5] else ""

        html += f"""
        <div style="display:flex;flex-direction:column;align-items:center;gap:6px;flex-shrink:0">
          <div {anim} class="stage-dot"
            style="background:{dot_bg};border:2px solid {dot_border};{dot_shadow};color:{'#fff' if not is_future else '#9CA3AF'};font-size:{'13px' if is_done else '14px'}">
            {dot_content}
          </div>
          <div style="font-size:9px;color:{lbl_color};font-weight:{lbl_weight};text-align:center;max-width:68px;line-height:1.3">
            {label}
          </div>
        </div>"""

        if i < len(TRANSIT_STAGES) - 1:
            # Ligne entre les étapes
            line_filled = 100 if is_done else 0
            line_color  = "#10B981" if is_done else TRANSIT_STAGES[i]["color"]
            html += f"""
            <div class="stage-line" style="background:#E5E7EB;margin-bottom:16px">
              <div class="stage-line-fill" style="background:{line_color};width:{line_filled}%"></div>
            </div>"""

    html += "</div>"
    return html


def render_route_map_svg(active_ships):
    """SVG animé de la route maritime Atlantique → Méditerranée"""
    # Waypoints simplifiés sur le SVG (viewBox 0 0 800 220)
    # Départ (CR/COL) → Atlantique → Gibraltar → Méditerranée → Ghazaouet
    WAYPOINTS = [
        (55,  155),   # Costa Rica / Colombia
        (160, 145),   # Sortie Caraïbes
        (310, 120),   # Atlantique centre
        (480, 95),    # Approche Açores
        (590, 80),    # Gibraltar
        (660, 90),    # Mer Alboran
        (730, 100),   # Ghazaouet
    ]

    # Construire un path SVG cubique
    path_d = f"M {WAYPOINTS[0][0]} {WAYPOINTS[0][1]}"
    for i in range(1, len(WAYPOINTS)):
        x0, y0 = WAYPOINTS[i-1]
        x1, y1 = WAYPOINTS[i]
        cx = (x0 + x1) / 2
        path_d += f" C {cx} {y0}, {cx} {y1}, {x1} {y1}"

    # Navires animés sur la route
    ships_svg = ""
    for ship in active_ships:
        pct = ship["progress"] / 100
        # Interpolation linéaire sur les waypoints
        total_segs = len(WAYPOINTS) - 1
        seg_f = pct * total_segs
        seg_i = min(int(seg_f), total_segs - 1)
        seg_t = seg_f - seg_i
        x0, y0 = WAYPOINTS[seg_i]
        x1, y1 = WAYPOINTS[min(seg_i + 1, total_segs)]
        sx = x0 + (x1 - x0) * seg_t
        sy = y0 + (y1 - y0) * seg_t
        ships_svg += f"""
        <g transform="translate({sx-10},{sy-14})">
          <text font-size="18" style="filter:drop-shadow(0 2px 4px rgba(0,0,0,0.3))">🚢</text>
          <text x="0" y="28" font-size="8" fill="#4361EE" font-weight="700" text-anchor="middle"
            style="font-family:Inter,sans-serif">{ship['label'][:8]}</text>
        </g>"""

    svg = f"""
    <svg viewBox="0 0 800 220" xmlns="http://www.w3.org/2000/svg"
         style="width:100%;height:170px;border-radius:12px;background:linear-gradient(180deg,#0F172A 0%,#0C2340 40%,#0F3460 100%)">

      <!-- Grille océan -->
      <defs>
        <pattern id="ocean-grid" width="40" height="40" patternUnits="userSpaceOnUse">
          <path d="M 40 0 L 0 0 0 40" fill="none" stroke="rgba(255,255,255,0.04)" stroke-width="0.5"/>
        </pattern>
        <filter id="glow">
          <feGaussianBlur stdDeviation="3" result="blur"/>
          <feComposite in="SourceGraphic" in2="blur" operator="over"/>
        </filter>
      </defs>
      <rect width="800" height="220" fill="url(#ocean-grid)"/>

      <!-- Continents simplifiés -->
      <!-- Amérique centrale / Caraïbes -->
      <ellipse cx="40" cy="160" rx="38" ry="28" fill="#1E3A2F" opacity="0.7"/>
      <text x="12" y="185" font-size="9" fill="rgba(255,255,255,0.4)" font-family="Inter,sans-serif">AMÉR. CENTRALE</text>

      <!-- Europe (Gibraltar) -->
      <ellipse cx="590" cy="58" rx="28" ry="18" fill="#1A2A4A" opacity="0.7"/>
      <text x="568" y="52" font-size="8" fill="rgba(255,255,255,0.4)" font-family="Inter,sans-serif">ESPAGNE</text>

      <!-- Maroc / Algérie -->
      <rect x="560" y="108" width="240" height="50" rx="6" fill="#1E2A1A" opacity="0.7"/>
      <text x="620" y="140" font-size="9" fill="rgba(255,255,255,0.4)" font-family="Inter,sans-serif">ALGÉRIE / MAROC</text>

      <!-- Détroit Gibraltar label -->
      <line x1="590" y1="76" x2="590" y2="108" stroke="rgba(255,255,255,0.15)" stroke-width="1" stroke-dasharray="3,3"/>
      <text x="596" y="95" font-size="8" fill="rgba(255,200,0,0.7)" font-family="Inter,sans-serif">GIBRALTAR</text>

      <!-- Route principale — trait gris -->
      <path d="{path_d}" fill="none" stroke="rgba(255,255,255,0.12)" stroke-width="2" stroke-dasharray="6,4"/>

      <!-- Route active animée — gradient bleu -->
      <path d="{path_d}" fill="none" stroke="url(#routeGrad)" stroke-width="2.5" stroke-linecap="round"/>
      <defs>
        <linearGradient id="routeGrad" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0%"   stop-color="#4361EE"/>
          <stop offset="50%"  stop-color="#3B82F6"/>
          <stop offset="100%" stop-color="#10B981"/>
        </linearGradient>
      </defs>

      <!-- Points d'étape -->
      <circle cx="{WAYPOINTS[0][0]}" cy="{WAYPOINTS[0][1]}" r="5" fill="#F59E0B" filter="url(#glow)"/>
      <circle cx="{WAYPOINTS[4][0]}" cy="{WAYPOINTS[4][1]}" r="5" fill="#8B5CF6" filter="url(#glow)"/>
      <circle cx="{WAYPOINTS[6][0]}" cy="{WAYPOINTS[6][1]}" r="6" fill="#10B981" filter="url(#glow)"/>

      <!-- Labels étapes clés -->
      <text x="{WAYPOINTS[0][0]-4}" y="{WAYPOINTS[0][1]+18}" font-size="8" fill="#F59E0B"
        font-family="Inter,sans-serif" font-weight="700">DÉPART</text>
      <text x="{WAYPOINTS[6][0]-24}" y="{WAYPOINTS[6][1]+18}" font-size="8" fill="#10B981"
        font-family="Inter,sans-serif" font-weight="700">GHAZAOUET</text>

      <!-- Navires actifs -->
      {ships_svg}

      <!-- Badge légende -->
      <rect x="10" y="10" width="140" height="22" rx="6" fill="rgba(255,255,255,0.06)"/>
      <circle cx="22" cy="21" r="4" fill="#10B981"/>
      <text x="30" y="25" font-size="9" fill="rgba(255,255,255,0.7)" font-family="Inter,sans-serif">Route maritime active</text>
    </svg>"""
    return svg


# ══════════════════════════════════════════════════════════════════════════════
# LOGIN
# ══════════════════════════════════════════════════════════════════════════════
def login_page():
    logo_src = img_to_b64("logo_eden_food.jpg") or img_to_b64("logo_eden_food.png")
    fond_src = img_to_b64("fond.png") or img_to_b64("fond.jpg")
    bg_css   = f"url('{fond_src}') center/cover no-repeat fixed" if fond_src \
               else "linear-gradient(135deg,#0F172A 0%,#1E3A5F 50%,#0F172A 100%)"
    logo_html = (f'<img src="{logo_src}" style="height:52px;display:block;margin:0 auto 20px">'
                 if logo_src else '<div style="font-size:48px;text-align:center;margin-bottom:16px">🍌</div>')

    st.markdown(f"""
    <style>
    .stApp{{background:{bg_css}!important}}
    section[data-testid="stSidebar"]{{display:none!important}}
    section[data-testid="stSidebarCollapsedControl"]{{display:none!important}}
    @keyframes slideUp{{from{{opacity:0;transform:translateY(32px)}}to{{opacity:1;transform:translateY(0)}}}}
    @keyframes pulse{{0%,100%{{box-shadow:0 24px 60px rgba(0,0,0,0.35)}}50%{{box-shadow:0 28px 70px rgba(67,97,238,0.3)}}}}
    </style>
    <div style="position:relative;z-index:10;display:flex;align-items:center;
        justify-content:center;min-height:85vh;padding:20px">
      <div style="background:rgba(255,255,255,0.97);border-radius:28px;padding:52px 48px;
          max-width:420px;width:100%;text-align:center;
          box-shadow:0 24px 60px rgba(0,0,0,0.35);
          animation:slideUp 0.5s cubic-bezier(0.34,1.56,0.64,1) both,pulse 4s ease-in-out 0.5s infinite">
        {logo_html}
        <p style="font-size:23px;font-weight:900;color:#111827;margin:0 0 5px;letter-spacing:-0.6px">Eden Food</p>
        <p style="font-size:13px;color:#9CA3AF;margin:0 0 10px">Logistics Platform · Accès sécurisé</p>
        <div style="display:inline-flex;align-items:center;gap:6px;background:#D1FAE5;color:#065F46;
            padding:4px 14px;border-radius:20px;font-size:11px;font-weight:700;margin-bottom:24px">
          🟢 Système opérationnel</div>
        <div style="height:1px;background:linear-gradient(90deg,transparent,#E5E7EB,transparent);margin-bottom:22px"></div>
      </div>
    </div>""", unsafe_allow_html=True)

    components.html("""
    <script>
    (function(){
      try{
        const old=parent.document.getElementById('eden-sparkles');
        if(old)old.remove();
        const cvs=parent.document.createElement('canvas');
        cvs.id='eden-sparkles';
        cvs.style.cssText='position:fixed;top:0;left:0;width:100vw;height:100vh;pointer-events:none;z-index:2;opacity:0;transition:opacity 1.2s ease';
        parent.document.body.appendChild(cvs);
        const ctx=cvs.getContext('2d');
        function resize(){cvs.width=parent.window.innerWidth;cvs.height=parent.window.innerHeight;}
        resize();parent.window.addEventListener('resize',resize);
        setTimeout(()=>{cvs.style.opacity='1';},120);
        const N=160;
        const pts=Array.from({length:N},()=>({
          x:Math.random()*cvs.width,y:Math.random()*cvs.height,
          r:Math.random()*1.6+0.4,o:Math.random(),
          os:(Math.random()*0.007+0.003)*(Math.random()>.5?1:-1),
          vx:(Math.random()-.5)*0.4,vy:(Math.random()-.5)*0.4,
          col:Math.random()>.62?'#F5A623':'#FFFFFF'
        }));
        function draw(){
          ctx.clearRect(0,0,cvs.width,cvs.height);
          pts.forEach(p=>{
            p.x+=p.vx;p.y+=p.vy;p.o+=p.os;
            if(p.o>=1||p.o<=0.04)p.os*=-1;
            if(p.x<0)p.x=cvs.width;if(p.x>cvs.width)p.x=0;
            if(p.y<0)p.y=cvs.height;if(p.y>cvs.height)p.y=0;
            if(p.col!=='#FFFFFF'&&p.o>0.7){ctx.shadowBlur=7;ctx.shadowColor='#F5A623';}
            else{ctx.shadowBlur=0;}
            ctx.beginPath();ctx.arc(p.x,p.y,p.r,0,Math.PI*2);
            ctx.fillStyle=p.col;ctx.globalAlpha=p.o;ctx.fill();
          });
          ctx.globalAlpha=1;ctx.shadowBlur=0;requestAnimationFrame(draw);
        }
        draw();
        parent.document.addEventListener('click',function(e){
          for(let i=0;i<4;i++){
            pts.push({x:e.clientX+(Math.random()-.5)*30,y:e.clientY+(Math.random()-.5)*30,
              r:Math.random()*2+0.5,o:1,os:-(Math.random()*0.015+0.005),
              vx:(Math.random()-.5)*1.5,vy:(Math.random()-.5)*1.5,
              col:Math.random()>.5?'#F5A623':'#FFFFFF'});
            if(pts.length>N+40)pts.shift();
          }
        });
      }catch(e){console.warn('Sparkles:',e);}
    })();
    </script>
    """, height=1)

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        with st.form("login_form"):
            u   = st.text_input("", placeholder="✦ Identifiant")
            pwd = st.text_input("", type="password", placeholder="🔒 Mot de passe")
            if st.form_submit_button("Connexion →", use_container_width=True, type="primary"):
                ul = u.strip().lower()
                if ul in USERS and USERS[ul]["password"] == pwd:
                    st.session_state.update(authenticated=True, username=ul, role=USERS[ul]["role"])
                    st.rerun()
                else:
                    st.error("Identifiant ou mot de passe incorrect")

if not st.session_state.authenticated:
    login_page()
    st.stop()

# ── Suppression sparkles sur toutes les pages authentifiées ───────────────────
components.html("""
<script>
(function(){
  try{
    const c=parent.document.getElementById('eden-sparkles');
    if(c){c.style.opacity='0';setTimeout(()=>c.remove(),400);}
  }catch(e){}
})();
</script>
""", height=0)

# ── CONSTANTES ────────────────────────────────────────────────────────────────
POIDS_UNIT  = 18.14
CRTNS       = {"TURBO(COLOMBIA)": 1080, "MOIN(COSTA RICA)": 1200}
KGS_PER_CNT = {"MOIN(COSTA RICA)": 1200*18.14, "TURBO(COLOMBIA)": 1080*18.14}

def licence_to_filename(lic): return str(lic).replace(" ","_").replace("/","_") + ".pdf"
def licence_pdf_path(lic):    return os.path.join("licences", licence_to_filename(lic))

# ── DATA ──────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=60)
def load_clients():
    df = pd.read_excel("eden_food.xlsx", sheet_name="📋 BASE CLIENTS",
                       usecols=list(range(11)), header=3)
    df.columns = ["num","nom","adresse1","adresse2","ville","pays","licence",
                  "poids_total","solde_excel","cnt_cr","cnt_col"]
    return df[df["nom"].notna() & (df["nom"] != "")].copy()

@st.cache_data(ttl=60)
def load_commandes():
    df = pd.read_excel("eden_food.xlsx", sheet_name="🚢 COMMANDES",
                       usecols=list(range(13)), header=3)
    df.columns = ["num","semaine","client","booking","licence","navire","voyage",
                  "pol","depart","eta","nb_cnt","produit","statut"]
    df = df[df["client"].notna() & (df["client"] != "")].copy()
    df["nb_cnt"]      = pd.to_numeric(df["nb_cnt"], errors="coerce").fillna(0).astype(int)
    df["crtns_cnt"]   = df["pol"].apply(lambda x: CRTNS.get(str(x).strip(), 1200))
    df["total_crtns"] = df["nb_cnt"] * df["crtns_cnt"]
    df["total_kgs"]   = (df["total_crtns"] * POIDS_UNIT).round(2)
    return df

clients_base   = load_clients()
commandes_base = load_commandes()

if st.session_state.new_commandes:
    df_sess = pd.DataFrame(st.session_state.new_commandes)
    df_sess["nb_cnt"]      = pd.to_numeric(df_sess["nb_cnt"], errors="coerce").fillna(0).astype(int)
    df_sess["crtns_cnt"]   = df_sess["pol"].apply(lambda x: CRTNS.get(str(x).strip(), 1200))
    df_sess["total_crtns"] = df_sess["nb_cnt"] * df_sess["crtns_cnt"]
    df_sess["total_kgs"]   = (df_sess["total_crtns"] * POIDS_UNIT).round(2)
    commandes = pd.concat([commandes_base, df_sess], ignore_index=True)
else:
    commandes = commandes_base.copy()

clients = clients_base.copy()
clients["poids_total"] = pd.to_numeric(clients["poids_total"], errors="coerce").fillna(0)

def get_solde_reel(nom, lic, poids):
    mask = (commandes["client"]==nom)&(commandes["licence"]==lic)&\
           (~commandes["statut"].str.contains("À GÉNÉRER", na=False))
    return round(poids - commandes.loc[mask,"total_kgs"].sum(), 2)

def get_solde_prev(nom, lic, poids):
    mask = (commandes["client"]==nom)&(commandes["licence"]==lic)
    return round(poids - commandes.loc[mask,"total_kgs"].sum(), 2)

clients["solde_reel"]   = clients.apply(lambda r: get_solde_reel(r["nom"],r["licence"],r["poids_total"]), axis=1)
clients["solde_prev"]   = clients.apply(lambda r: get_solde_prev(r["nom"],r["licence"],r["poids_total"]), axis=1)
clients["cnt_reel_cr"]  = (clients["solde_reel"]/KGS_PER_CNT["MOIN(COSTA RICA)"]).round(2)
clients["cnt_reel_col"] = (clients["solde_reel"]/KGS_PER_CNT["TURBO(COLOMBIA)"]).round(2)
clients["cnt_prev_cr"]  = (clients["solde_prev"]/KGS_PER_CNT["MOIN(COSTA RICA)"]).round(2)
clients["cnt_prev_col"] = (clients["solde_prev"]/KGS_PER_CNT["TURBO(COLOMBIA)"]).round(2)

current_week_num  = datetime.now().isocalendar()[1]
current_week_str  = f"S-{current_week_num}"
commandes_semaine = commandes[commandes["semaine"]==current_week_str]

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    logo_src = img_to_b64("logo_eden_food.jpg") or img_to_b64("logo_eden_food.png")
    if logo_src:
        st.markdown(f'<div style="padding:24px 18px 14px"><img src="{logo_src}" style="height:30px"></div>',
                    unsafe_allow_html=True)
    else:
        st.markdown('<div style="padding:24px 18px 14px;font-size:16px;font-weight:900;color:#111827">🍌 EDEN FOOD</div>',
                    unsafe_allow_html=True)

    st.markdown('<div style="height:1px;background:#E5E7EB;margin:0 18px 14px"></div>', unsafe_allow_html=True)
    st.markdown('<div style="padding:0 18px 8px;font-size:10px;color:#9CA3AF;text-transform:uppercase;letter-spacing:1.5px;font-weight:700">Navigation</div>',
                unsafe_allow_html=True)

    NAV = [
        ("dashboard", "🏠", "Overview"),
        ("semaine",   "📅", f"Semaine {current_week_str}"),
        ("commandes", "🚢", "Commandes"),
        ("tracking",  "🗺️", "Tracking maritime"),   # ← NOUVEAU
        ("documents", "📁", "Documents"),
        ("licences",  "📋", "Licences DPVCT"),
        ("planning",  "👤", "Planning client"),
    ]

    for pid, icon, label in NAV:
        if st.session_state.page == pid:
            st.markdown(
                f'<div style="background:#EEF2FF;border-radius:8px;padding:10px 14px;'
                f'margin-bottom:1px;color:#4361EE;font-size:13.5px;font-weight:600;'
                f'border-left:3px solid #4361EE">{icon}&nbsp;&nbsp;{label}</div>',
                unsafe_allow_html=True)
        else:
            if st.button(f"{icon}  {label}", key=f"nav_{pid}", use_container_width=True):
                st.session_state.page = pid
                st.rerun()

    if st.session_state.role == "admin":
        st.markdown('<div style="height:1px;background:#E5E7EB;margin:10px 18px"></div>', unsafe_allow_html=True)
        st.markdown('<div style="padding:0 18px 8px;font-size:10px;color:#9CA3AF;text-transform:uppercase;letter-spacing:1.5px;font-weight:700">Admin</div>',
                    unsafe_allow_html=True)
        if st.button("➕  Nouvelle commande", key="nav_new_cmd", use_container_width=True):
            st.session_state.page = "new_cmd"
            st.rerun()

    st.markdown('<div style="height:1px;background:#E5E7EB;margin:12px 18px 8px"></div>', unsafe_allow_html=True)
    st.markdown(
        f'<div style="padding:8px 18px;display:flex;align-items:center;gap:10px">'
        f'<div style="width:32px;height:32px;border-radius:50%;background:#EEF2FF;'
        f'display:flex;align-items:center;justify-content:center;font-size:13px">👤</div>'
        f'<div><div style="font-size:12px;font-weight:700;color:#111827">{st.session_state.username.upper()}</div>'
        f'<div style="font-size:10px;color:#9CA3AF">{st.session_state.role}</div></div></div>',
        unsafe_allow_html=True)
    if st.button("🚪  Déconnexion", use_container_width=True, key="logout"):
        st.session_state.update(authenticated=False, username="")
        st.rerun()

page = st.session_state.page

# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
if page == "dashboard":
    hero_src = img_to_b64("hero.jpg") or img_to_b64("hero.png")
    logo_src = img_to_b64("logo_eden_food.jpg") or img_to_b64("logo_eden_food.png")
    logo_ov  = f'<img src="{logo_src}" style="height:36px;margin-bottom:12px;display:block">' if logo_src else ""

    if hero_src:
        st.markdown(f"""
        <div class="hero-wrap" style="background:url('{hero_src}') center 50% / cover no-repeat;">
          <div class="hero-overlay">
            <div class="hero-text">
              {logo_ov}
              <h1>Fresh from the<br>plantation to the world</h1>
              <p>Suivi en temps réel — Colombie & Costa Rica</p>
              <div class="hero-badge">🍌 {current_week_str} · {len(commandes)} expéditions actives</div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background:linear-gradient(110deg,#0F172A,#4361EE);padding:52px;overflow:hidden;position:relative;height:320px;display:flex;align-items:center;">
          <div style="position:absolute;top:-40px;right:-40px;width:300px;height:300px;
              background:rgba(255,255,255,0.04);border-radius:50%"></div>
          {logo_ov}
          <div>
          <h1 style="font-size:32px;font-weight:900;color:#fff;letter-spacing:-1px;margin:0 0 10px">
            Fresh from the plantation to the world</h1>
          <p style="font-size:14px;color:rgba(255,255,255,0.72);max-width:440px;margin:0 0 22px">
            Colombie & Costa Rica — Suivi logistique temps réel</p>
          <div class="hero-badge">🍌 {current_week_str} · {len(commandes)} expéditions</div>
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="main-wrap">', unsafe_allow_html=True)

    todo  = commandes[commandes["statut"].str.contains("À GÉNÉRER", na=False)]
    done  = commandes[commandes["statut"].str.contains("GÉNÉRÉ",    na=False)]
    alert = clients[clients["solde_reel"] < 19591.2]
    tdocs = sum(len(list_docs(b)) for b in commandes["booking"].dropna().unique())

    st.markdown(f"""
    <div class="kpi-grid">
      <div class="kpi-card" style="--card-color:#4361EE;--card-bg:#EEF2FF">
        <div class="icon-wrap">🚢</div><div class="kpi-lbl">Expéditions</div>
        <div class="kpi-val" style="color:#4361EE">{len(commandes)}</div><div class="kpi-sub">enregistrées</div>
      </div>
      <div class="kpi-card" style="--card-color:#F59E0B;--card-bg:#FEF3C7">
        <div class="icon-wrap">⏳</div><div class="kpi-lbl">À générer</div>
        <div class="kpi-val" style="color:#D97706">{len(todo)}</div><div class="kpi-sub">en attente</div>
      </div>
      <div class="kpi-card" style="--card-color:#10B981;--card-bg:#D1FAE5">
        <div class="icon-wrap">✅</div><div class="kpi-lbl">Confirmées</div>
        <div class="kpi-val" style="color:#059669">{len(done)}</div><div class="kpi-sub">générées</div>
      </div>
      <div class="kpi-card" style="--card-color:#8B5CF6;--card-bg:#EDE9FE">
        <div class="icon-wrap">📦</div><div class="kpi-lbl">CNT planifiés</div>
        <div class="kpi-val" style="color:#7C3AED">{int(todo["nb_cnt"].sum())}</div><div class="kpi-sub">conteneurs</div>
      </div>
      <div class="kpi-card" style="--card-color:#EF4444;--card-bg:#FEE2E2">
        <div class="icon-wrap">🔴</div><div class="kpi-lbl">Alertes</div>
        <div class="kpi-val" style="color:#DC2626">{len(alert)}</div><div class="kpi-sub">licences critiques</div>
      </div>
      <div class="kpi-card" style="--card-color:#3B82F6;--card-bg:#DBEAFE">
        <div class="icon-wrap">📁</div><div class="kpi-lbl">Documents</div>
        <div class="kpi-val" style="color:#2563EB">{tdocs}</div><div class="kpi-sub">uploadés</div>
      </div>
    </div>""", unsafe_allow_html=True)

    c1, c2 = st.columns([3, 2])
    with c1:
        st.markdown('<div class="sec-hdr"><span class="sec-title">Dernières expéditions</span><span class="sec-sub">10 dernières</span></div>', unsafe_allow_html=True)
        st.dataframe(commandes.tail(10)[["semaine","client","booking","pol","nb_cnt","depart","statut"]],
            use_container_width=True, hide_index=True, height=340,
            column_config={
                "semaine": st.column_config.TextColumn("Sem."),
                "client":  st.column_config.TextColumn("Client"),
                "booking": st.column_config.TextColumn("Booking"),
                "pol":     st.column_config.TextColumn("POL"),
                "nb_cnt":  st.column_config.NumberColumn("CNT", format="%d"),
                "depart":  st.column_config.TextColumn("Départ"),
                "statut":  st.column_config.TextColumn("Statut"),
            })
    with c2:
        st.markdown('<div class="sec-hdr"><span class="sec-title">Répartition POL</span></div>', unsafe_allow_html=True)
        if not commandes.empty:
            df_pol = commandes.groupby("pol")["nb_cnt"].sum().reset_index()
            fig = px.pie(df_pol, values="nb_cnt", names="pol", hole=0.65,
                         color_discrete_sequence=["#4361EE","#F59E0B"])
            fig.update_traces(textinfo="percent+label")
            fig = apply_chart_style(fig, "rgba(0,0,0,0)")
            fig.update_layout(legend=dict(orientation="h", y=-0.1))
            st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="sec-hdr"><span class="sec-title">Volume hebdomadaire</span><span class="sec-sub">CNT par semaine</span></div>', unsafe_allow_html=True)
    if not commandes.empty:
        df_sem = commandes.groupby("semaine")["nb_cnt"].sum().reset_index()
        fig2 = px.bar(df_sem, x="semaine", y="nb_cnt",
                      color_discrete_sequence=["#4361EE"],
                      labels={"semaine":"","nb_cnt":"Conteneurs"})
        fig2.update_traces(marker_cornerradius=6, marker_line_width=0)
        fig2 = apply_chart_style(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SEMAINE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "semaine":
    st.markdown(f'<div class="topbar"><div style="display:flex;align-items:center;gap:14px"><div class="topbar-title">Semaine en cours</div><div class="topbar-badge">{current_week_str}</div></div></div>', unsafe_allow_html=True)
    st.markdown('<div class="main-wrap">', unsafe_allow_html=True)

    if commandes_semaine.empty:
        st.info(f"Aucune commande pour {current_week_str}.")
    else:
        todo_s = commandes_semaine[commandes_semaine["statut"].str.contains("À GÉNÉRER", na=False)]
        done_s = commandes_semaine[commandes_semaine["statut"].str.contains("GÉNÉRÉ",    na=False)]
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:26px">
          <div class="kpi-card" style="--card-color:#4361EE;--card-bg:#EEF2FF"><div class="kpi-lbl">Total</div><div class="kpi-val" style="color:#4361EE">{len(commandes_semaine)}</div></div>
          <div class="kpi-card" style="--card-color:#F59E0B;--card-bg:#FEF3C7"><div class="kpi-lbl">⏳ À générer</div><div class="kpi-val" style="color:#D97706">{len(todo_s)}</div></div>
          <div class="kpi-card" style="--card-color:#10B981;--card-bg:#D1FAE5"><div class="kpi-lbl">✅ Confirmées</div><div class="kpi-val" style="color:#059669">{len(done_s)}</div></div>
          <div class="kpi-card" style="--card-color:#8B5CF6;--card-bg:#EDE9FE"><div class="kpi-lbl">CNT total</div><div class="kpi-val" style="color:#7C3AED">{int(commandes_semaine["nb_cnt"].sum())}</div></div>
        </div>""", unsafe_allow_html=True)

        for _, row in commandes_semaine.iterrows():
            pc = "pill-green" if "GÉNÉRÉ" in str(row["statut"]) else "pill-orange"
            nd = len(list_docs(row["booking"]))
            dp = f'<span class="pill pill-blue">📁 {nd}</span>' if nd else ""
            st.markdown(f"""
            <div class="cmd-row">
              <div style="min-width:190px">
                <div style="font-size:14px;font-weight:700;color:#111827">{row['client']}</div>
                <div style="font-size:11px;color:#9CA3AF;margin-top:3px">{row['booking']} · {row['licence']}</div>
              </div>
              <div style="text-align:center"><div style="font-size:9px;color:#9CA3AF;margin-bottom:3px;text-transform:uppercase">POL</div><div style="font-weight:700;color:#111827;font-size:12px">{row['pol']}</div></div>
              <div style="text-align:center"><div style="font-size:9px;color:#9CA3AF;margin-bottom:3px;text-transform:uppercase">CNT</div><div style="font-weight:900;color:#4361EE;font-size:22px;letter-spacing:-1px">{row['nb_cnt']}</div></div>
              <div style="text-align:center"><div style="font-size:9px;color:#9CA3AF;margin-bottom:3px;text-transform:uppercase">Départ</div><div style="font-weight:600;color:#374151;font-size:12px">{row['depart']}</div></div>
              <div style="text-align:center"><div style="font-size:9px;color:#9CA3AF;margin-bottom:3px;text-transform:uppercase">ETA</div><div style="font-weight:600;color:#374151;font-size:12px">{row['eta']}</div></div>
              <div style="display:flex;gap:6px;align-items:center">{dp}<span class="pill {pc}">{row['statut']}</span></div>
            </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# COMMANDES
# ══════════════════════════════════════════════════════════════════════════════
elif page == "commandes":
    st.markdown('<div class="topbar"><div class="topbar-title">Commandes</div></div>', unsafe_allow_html=True)
    st.markdown('<div style="background:#fff;border-bottom:1px solid #E5E7EB;padding:10px 36px">', unsafe_allow_html=True)
    fc1,fc2,fc3,fc4 = st.columns([2,2,2,1])
    with fc1:
        f_client = st.multiselect("c", commandes["client"].dropna().unique().tolist(),
                                  default=commandes["client"].dropna().unique().tolist(),
                                  label_visibility="collapsed", placeholder="🔍 Client")
    with fc2:
        f_pol = st.multiselect("p", commandes["pol"].dropna().unique().tolist(),
                               default=commandes["pol"].dropna().unique().tolist(),
                               label_visibility="collapsed", placeholder="🌍 POL")
    with fc3:
        f_statut = st.multiselect("s", commandes["statut"].dropna().unique().tolist(),
                                  default=commandes["statut"].dropna().unique().tolist(),
                                  label_visibility="collapsed", placeholder="📊 Statut")
    with fc4:
        f_sem = st.text_input("sem", placeholder="S-18", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-wrap">', unsafe_allow_html=True)

    df_filt = commandes[commandes["client"].isin(f_client) & commandes["pol"].isin(f_pol) & commandes["statut"].isin(f_statut)]
    if f_sem:
        df_filt = df_filt[df_filt["semaine"].str.contains(f_sem, case=False, na=False)]

    st.markdown(f'<div style="font-size:12px;color:#6B7280;margin-bottom:14px"><b style="color:#111827">{len(df_filt)}</b> commandes · <b style="color:#111827">{int(df_filt["nb_cnt"].sum())}</b> CNT · <b style="color:#111827">{df_filt["total_kgs"].sum():,.0f}</b> kgs</div>', unsafe_allow_html=True)

    for _, row in df_filt.iterrows():
        pc = "pill-green" if "GÉNÉRÉ" in str(row["statut"]) else "pill-orange"
        nd = len(list_docs(row["booking"]))
        dp = f'<span class="pill pill-blue">📁 {nd}</span>' if nd else '<span class="pill" style="background:#F3F4F6;color:#9CA3AF">📁 0</span>'
        st.markdown(f"""
        <div class="cmd-row">
          <div style="min-width:200px"><div style="font-size:13px;font-weight:700;color:#111827">{row['client']}</div>
          <div style="font-size:11px;color:#9CA3AF;margin-top:2px">{row['semaine']} · {row['booking']}</div></div>
          <div style="text-align:center"><div style="font-size:9px;color:#9CA3AF;margin-bottom:2px;text-transform:uppercase">Navire</div><div style="font-weight:500;color:#374151;font-size:11px">{row['navire']}</div></div>
          <div style="text-align:center"><div style="font-size:9px;color:#9CA3AF;margin-bottom:2px;text-transform:uppercase">POL</div><div style="font-weight:700;color:#111827;font-size:12px">{row['pol']}</div></div>
          <div style="text-align:center"><div style="font-size:9px;color:#9CA3AF;margin-bottom:2px;text-transform:uppercase">CNT</div><div style="font-weight:900;color:#4361EE;font-size:20px">{row['nb_cnt']}</div></div>
          <div style="text-align:center"><div style="font-size:9px;color:#9CA3AF;margin-bottom:2px;text-transform:uppercase">Départ</div><div style="font-weight:500;color:#374151;font-size:11px">{row['depart']}</div></div>
          <div style="text-align:center"><div style="font-size:9px;color:#9CA3AF;margin-bottom:2px;text-transform:uppercase">ETA</div><div style="font-weight:500;color:#374151;font-size:11px">{row['eta']}</div></div>
          <div style="display:flex;gap:6px;align-items:center">{dp}<span class="pill {pc}">{row['statut']}</span></div>
        </div>""", unsafe_allow_html=True)

        is_open = st.session_state.expanded_cmd == row['booking']
        col_btn, _ = st.columns([1,5])
        with col_btn:
            if st.button("🔼 Fermer" if is_open else "📁 Documents",
                         key=f"docbtn_{row['booking']}", use_container_width=True):
                st.session_state.expanded_cmd = None if is_open else row['booking']
                st.rerun()

        if is_open:
            st.markdown(f'<div class="doc-zone"><div style="font-size:12px;font-weight:700;color:#111827;margin-bottom:12px">📁 Documents — <span style="color:#4361EE">{row["booking"]}</span></div></div>', unsafe_allow_html=True)
            existing = list_docs(row['booking'])
            if existing:
                for doc_name in existing:
                    doc_path = os.path.join(docs_path(row['booking']), doc_name)
                    d1,d2,d3 = st.columns([4,1,1])
                    with d1: st.markdown(f'<div class="doc-chip">📄 {doc_name}</div>', unsafe_allow_html=True)
                    with d2:
                        with open(doc_path,"rb") as f:
                            st.download_button("⬇️", f.read(), file_name=doc_name,
                                key=f"dl_{row['booking']}_{doc_name}", use_container_width=True)
                    with d3:
                        if st.session_state.role == "admin":
                            if st.button("🗑️", key=f"del_{row['booking']}_{doc_name}", use_container_width=True):
                                delete_doc(row['booking'], doc_name)
                                st.rerun()
            else:
                st.caption("Aucun document — uploadez ci-dessous.")
            u1,u2 = st.columns([3,1])
            with u1:
                uploaded = st.file_uploader("", type=["pdf","xlsx","xls","docx","jpg","png"],
                                            key=f"up_{row['booking']}", label_visibility="collapsed")
            with u2:
                dtype = st.selectbox("", DOC_TYPES, key=f"dtype_{row['booking']}", label_visibility="collapsed")
            if uploaded and st.button("✅ Uploader", key=f"upconf_{row['booking']}", type="primary"):
                uploaded.name = f"{dtype.replace(' ','_')}_{uploaded.name}"
                save_doc(row['booking'], uploaded)
                st.success("✅ Uploadé !")
                st.rerun()
            st.markdown("")

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TRACKING MARITIME  ← NOUVEAU
# ══════════════════════════════════════════════════════════════════════════════
elif page == "tracking":
    st.markdown('<div class="topbar"><div style="display:flex;align-items:center;gap:14px"><div class="topbar-title">Tracking maritime</div><div class="topbar-badge">🌊 En temps réel</div></div></div>', unsafe_allow_html=True)
    st.markdown('<div class="main-wrap">', unsafe_allow_html=True)

    df_track = commandes[commandes["depart"].notna()].copy()
    en_attente_list, en_mer_list, arrives_list = [], [], []
    active_ships_for_map = []

    for _, row in df_track.iterrows():
        s_idx, prog, days_el, eta_calc = get_tracking_info(row["depart"])
        if days_el is not None and days_el < 0:
            en_attente_list.append(row)
        elif s_idx >= 5:
            arrives_list.append(row)
        else:
            en_mer_list.append(row)
            active_ships_for_map.append({"progress": prog, "label": str(row["client"])[:10]})

    st.markdown(f"""
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:24px">
      <div class="kpi-card" style="--card-color:#F59E0B;--card-bg:#FEF3C7">
        <div class="icon-wrap">⏳</div><div class="kpi-lbl">En attente départ</div>
        <div class="kpi-val" style="color:#D97706">{len(en_attente_list)}</div><div class="kpi-sub">pas encore partis</div>
      </div>
      <div class="kpi-card" style="--card-color:#3B82F6;--card-bg:#DBEAFE">
        <div class="icon-wrap">🚢</div><div class="kpi-lbl">En mer</div>
        <div class="kpi-val" style="color:#2563EB">{len(en_mer_list)}</div><div class="kpi-sub">en transit actif</div>
      </div>
      <div class="kpi-card" style="--card-color:#10B981;--card-bg:#D1FAE5">
        <div class="icon-wrap">⚓</div><div class="kpi-lbl">Arrivés Ghazaouet</div>
        <div class="kpi-val" style="color:#059669">{len(arrives_list)}</div><div class="kpi-sub">à destination</div>
      </div>
    </div>""", unsafe_allow_html=True)

    if active_ships_for_map or en_attente_list or arrives_list:
        map_svg = render_route_map_svg(active_ships_for_map)
        st.markdown(f"""
        <div style="background:#0F172A;border-radius:16px;padding:16px;margin-bottom:24px;
             box-shadow:0 8px 32px rgba(0,0,0,0.3)">
          <div style="font-size:11px;color:rgba(255,255,255,0.5);font-weight:700;
               text-transform:uppercase;letter-spacing:1.5px;margin-bottom:10px">
            🗺️ Route maritime — Amériques → Ghazaouet
          </div>
          {map_svg}
        </div>""", unsafe_allow_html=True)

    filter_track = st.selectbox("",
        ["🌊 Tous", "⏳ En attente", "🚢 En mer", "⚓ Arrivés"],
        label_visibility="collapsed")

    if filter_track == "⏳ En attente":
        rows_to_show = en_attente_list
    elif filter_track == "🚢 En mer":
        rows_to_show = en_mer_list
    elif filter_track == "⚓ Arrivés":
        rows_to_show = arrives_list
    else:
        rows_to_show = en_mer_list + en_attente_list + arrives_list

    if not rows_to_show:
        st.info("Aucune commande dans cette catégorie.")
    else:
        for row in rows_to_show:
            s_idx, prog, days_el, eta_calc = get_tracking_info(row["depart"])
            current_s = TRANSIT_STAGES[min(s_idx, len(TRANSIT_STAGES) - 1)]

            if s_idx >= 5:
                card_color = "#10B981"
                card_bg    = "#D1FAE5"
                status_txt = "⚓ Arrivé à Ghazaouet"
            elif s_idx >= 2:
                card_color = "#3B82F6"
                card_bg    = "#DBEAFE"
                status_txt = f"🚢 {current_s['label']}"
            elif s_idx == 1:
                card_color = "#4361EE"
                card_bg    = "#EEF2FF"
                status_txt = "⚓ Port de départ"
            else:
                card_color = "#F59E0B"
                card_bg    = "#FEF3C7"
                status_txt = "⏳ Avant départ"

            days_label = f"J+{days_el}" if days_el is not None and days_el >= 0 else (
                         f"Départ dans {abs(days_el)}j" if days_el is not None else "—")
            eta_label  = eta_calc.strftime("%d/%m/%Y") if eta_calc else "—"
            timeline_html = build_stage_timeline_html(s_idx, prog, str(row["pol"]))

            bkey = str(row["booking"]).replace(" ", "_")
            is_open = bkey in st.session_state.expanded_track

            st.markdown(f"""
            <div class="track-card" style="border-top:3px solid {card_color}">
              <div class="track-header">
                <div>
                  <div style="font-size:15px;font-weight:800;color:#111827">{row['client']}</div>
                  <div style="font-size:11px;color:#9CA3AF;margin-top:3px">
                    {row['navire']} · {row['booking']} · {row['pol'].split('(')[0].strip()}
                  </div>
                </div>
                <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap">
                  <div style="text-align:center">
                    <div style="font-size:9px;color:#9CA3AF;text-transform:uppercase;margin-bottom:2px">Départ</div>
                    <div style="font-size:12px;font-weight:700;color:#374151">{row['depart']}</div>
                  </div>
                  <div style="text-align:center">
                    <div style="font-size:9px;color:#9CA3AF;text-transform:uppercase;margin-bottom:2px">ETA Ghaz.</div>
                    <div style="font-size:12px;font-weight:700;color:#374151">{eta_label}</div>
                  </div>
                  <div style="text-align:center">
                    <div style="font-size:9px;color:#9CA3AF;text-transform:uppercase;margin-bottom:2px">Progression</div>
                    <div style="font-size:16px;font-weight:900;color:{card_color}">{prog:.0f}%</div>
                  </div>
                  <span class="pill" style="background:{card_bg};color:{card_color}">{status_txt}</span>
                  <span style="font-size:11px;font-weight:700;color:{card_color};background:{card_bg};
                    padding:4px 10px;border-radius:20px">{days_label}</span>
                </div>
              </div>
              <div style="padding:0 22px 6px">
                <div class="prog-track" style="height:6px">
                  <div class="prog-fill" style="background:linear-gradient(90deg,{card_color},{card_color}88);width:{prog}%"></div>
                </div>
              </div>
            </div>""", unsafe_allow_html=True)

            btn_lbl = "🔼 Masquer étapes" if is_open else "🔽 Voir étapes détaillées"
            if st.button(btn_lbl, key=f"track_toggle_{bkey}", use_container_width=False):
                if is_open:
                    st.session_state.expanded_track.discard(bkey)
                else:
                    st.session_state.expanded_track.add(bkey)
                st.rerun()

            if is_open:
                st.markdown(f"""
                <div style="background:#F9FAFB;border:1px solid #E5E7EB;border-radius:12px;
                     padding:18px 22px;margin-bottom:10px;overflow-x:auto">
                  <div style="font-size:11px;color:#9CA3AF;font-weight:700;
                       text-transform:uppercase;letter-spacing:1px;margin-bottom:14px">
                    Étapes — {row['booking']}
                  </div>
                  {timeline_html}
                  <div style="margin-top:16px;display:grid;grid-template-columns:repeat(4,1fr);gap:10px">
                    <div style="background:#fff;border-radius:10px;padding:12px;border:1px solid #E5E7EB">
                      <div style="font-size:9px;color:#9CA3AF;text-transform:uppercase;font-weight:700;margin-bottom:4px">CNT</div>
                      <div style="font-size:18px;font-weight:900;color:#4361EE">{row['nb_cnt']}</div>
                    </div>
                    <div style="background:#fff;border-radius:10px;padding:12px;border:1px solid #E5E7EB">
                      <div style="font-size:9px;color:#9CA3AF;text-transform:uppercase;font-weight:700;margin-bottom:4px">Total kgs</div>
                      <div style="font-size:14px;font-weight:800;color:#111827">{row['total_kgs']:,.0f}</div>
                    </div>
                    <div style="background:#fff;border-radius:10px;padding:12px;border:1px solid #E5E7EB">
                      <div style="font-size:9px;color:#9CA3AF;text-transform:uppercase;font-weight:700;margin-bottom:4px">Semaine</div>
                      <div style="font-size:14px;font-weight:800;color:#111827">{row['semaine']}</div>
                    </div>
                    <div style="background:#fff;border-radius:10px;padding:12px;border:1px solid #E5E7EB">
                      <div style="font-size:9px;color:#9CA3AF;text-transform:uppercase;font-weight:700;margin-bottom:4px">Produit</div>
                      <div style="font-size:14px;font-weight:800;color:#111827">{row['produit']}</div>
                    </div>
                  </div>
                </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# DOCUMENTS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "documents":
    st.markdown('<div class="topbar"><div class="topbar-title">Documents</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="main-wrap">', unsafe_allow_html=True)

    all_b  = commandes["booking"].dropna().unique()
    tdocs  = sum(len(list_docs(b)) for b in all_b)
    c_avec = sum(1 for b in all_b if len(list_docs(b)) > 0)
    c_sans = len(all_b) - c_avec

    st.markdown(f"""
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:26px">
      <div class="kpi-card" style="--card-color:#3B82F6;--card-bg:#DBEAFE"><div class="icon-wrap">📁</div><div class="kpi-lbl">Total documents</div><div class="kpi-val" style="color:#2563EB">{tdocs}</div></div>
      <div class="kpi-card" style="--card-color:#10B981;--card-bg:#D1FAE5"><div class="icon-wrap">✅</div><div class="kpi-lbl">Documentées</div><div class="kpi-val" style="color:#059669">{c_avec}</div><div class="kpi-sub">avec docs</div></div>
      <div class="kpi-card" style="--card-color:#F59E0B;--card-bg:#FEF3C7"><div class="icon-wrap">⚠️</div><div class="kpi-lbl">Sans documents</div><div class="kpi-val" style="color:#D97706">{c_sans}</div><div class="kpi-sub">à compléter</div></div>
    </div>""", unsafe_allow_html=True)

    search = st.text_input("", placeholder="🔍 Rechercher par booking ou client...", label_visibility="collapsed")

    for _, row in commandes.iterrows():
        if search and search.lower() not in str(row["booking"]).lower() and search.lower() not in str(row["client"]).lower():
            continue
        docs = list_docs(row["booking"])
        n    = len(docs)
        clr  = "#10B981" if n >= 3 else ("#F59E0B" if n >= 1 else "#EF4444")
        lbl  = f"✅ {n} doc{'s' if n>1 else ''}" if n else "⚠️ Aucun"
        st.markdown(f"""
        <div class="cmd-row" style="border-left:3px solid {clr}">
          <div style="min-width:220px"><div style="font-size:13px;font-weight:700;color:#111827">{row['client']}</div>
          <div style="font-size:11px;color:#9CA3AF">{row['booking']} · {row['semaine']}</div></div>
          <span style="color:{clr};font-weight:700;font-size:12px">{lbl}</span>
          <div style="flex:1;display:flex;flex-wrap:wrap;gap:3px">
            {"".join([f'<span class="doc-chip">📄 {d}</span>' for d in docs]) if docs else '<span style="color:#9CA3AF;font-size:11px;font-style:italic">Aucun fichier</span>'}
          </div>
        </div>""", unsafe_allow_html=True)

        with st.expander(f"📤 Upload · {row['booking']}", expanded=False):
            u1,u2 = st.columns([3,1])
            with u1:
                upf = st.file_uploader("", type=["pdf","xlsx","xls","docx","jpg","png"],
                                       key=f"gup_{row['booking']}", label_visibility="collapsed")
            with u2:
                dtype = st.selectbox("", DOC_TYPES, key=f"gdtype_{row['booking']}", label_visibility="collapsed")
            if upf and st.button("✅ Uploader", key=f"gupconf_{row['booking']}", type="primary"):
                upf.name = f"{dtype.replace(' ','_')}_{upf.name}"
                save_doc(row["booking"], upf)
                st.success("✅ Uploadé !")
                st.rerun()
            if docs:
                for doc_name in docs:
                    dp = os.path.join(docs_path(row["booking"]), doc_name)
                    c1, c2 = st.columns([4, 1])
                    with c1: st.markdown(f"`{doc_name}`")
                    with c2:
                        with open(dp, "rb") as f:
                            st.download_button("⬇️", f.read(), file_name=doc_name,
                                key=f"gdl_{row['booking']}_{doc_name}", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# LICENCES
# ══════════════════════════════════════════════════════════════════════════════
elif page == "licences":
    st.markdown('<div class="topbar"><div class="topbar-title">Licences DPVCT</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="main-wrap">', unsafe_allow_html=True)

    for _, row in clients.iterrows():
        pr = max(0, min(100, row["solde_reel"]/row["poids_total"]*100)) if row["poids_total"] > 0 else 0
        pp = max(0, min(100, row["solde_prev"]/row["poids_total"]*100)) if row["poids_total"] > 0 else 0
        pc = "#10B981" if pr > 30 else ("#F59E0B" if pr > 10 else "#EF4444")

        if   row["solde_reel"] < 0:       badge = '<span class="pill pill-red">❌ DÉPASSEMENT</span>'
        elif row["solde_reel"] < 19591.2: badge = '<span class="pill pill-red">🔴 CRITIQUE</span>'
        elif row["solde_reel"] < 58773.6: badge = '<span class="pill pill-orange">⚠️ ATTENTION</span>'
        else:                              badge = '<span class="pill pill-green">✅ OK</span>'

        pdf_path   = licence_pdf_path(row["licence"])
        pdf_exists = os.path.exists(pdf_path)

        st.markdown(f"""
        <div class="card">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px;margin-bottom:16px">
            <div><div style="font-size:16px;font-weight:800;color:#111827">{row['nom']}</div>
            <div style="font-size:12px;color:#9CA3AF;margin-top:3px">🔑 {row['licence']} · {row['pays']}</div></div>
            {badge}
          </div>
          <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:14px">
            <div style="background:#F9FAFB;border-radius:10px;padding:14px">
              <div style="font-size:9px;color:#9CA3AF;text-transform:uppercase;font-weight:700;margin-bottom:4px">Poids total</div>
              <div style="font-size:19px;font-weight:800;color:#111827">{row['poids_total']:,.0f} <span style="font-size:12px;color:#9CA3AF">kgs</span></div>
            </div>
            <div style="background:#EEF2FF;border-radius:10px;padding:14px">
              <div style="font-size:9px;color:#4361EE;text-transform:uppercase;font-weight:700;margin-bottom:4px">Solde réel</div>
              <div style="font-size:19px;font-weight:800;color:#4361EE">{row['solde_reel']:,.0f} <span style="font-size:12px">kgs</span></div>
            </div>
            <div style="background:#FEF3C7;border-radius:10px;padding:14px">
              <div style="font-size:9px;color:#D97706;text-transform:uppercase;font-weight:700;margin-bottom:4px">Solde prévi.</div>
              <div style="font-size:19px;font-weight:800;color:#D97706">{row['solde_prev']:,.0f} <span style="font-size:12px">kgs</span></div>
            </div>
          </div>
          <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:14px">
            <div style="background:#EEF2FF;border-radius:10px;padding:12px;text-align:center">
              <div style="font-size:9px;color:#4361EE;font-weight:700;text-transform:uppercase;margin-bottom:4px">🇨🇷 CR Réel</div>
              <div style="font-size:20px;font-weight:900;color:#4361EE">{row['cnt_reel_cr']:.1f}</div>
              <div style="font-size:9px;color:#9CA3AF">CNT</div>
            </div>
            <div style="background:#FEF3C7;border-radius:10px;padding:12px;text-align:center">
              <div style="font-size:9px;color:#D97706;font-weight:700;text-transform:uppercase;margin-bottom:4px">🇨🇷 CR Prév.</div>
              <div style="font-size:20px;font-weight:900;color:#D97706">{row['cnt_prev_cr']:.1f}</div>
              <div style="font-size:9px;color:#9CA3AF">CNT</div>
            </div>
            <div style="background:#EEF2FF;border-radius:10px;padding:12px;text-align:center">
              <div style="font-size:9px;color:#4361EE;font-weight:700;text-transform:uppercase;margin-bottom:4px">🇨🇴 COL Réel</div>
              <div style="font-size:20px;font-weight:900;color:#4361EE">{row['cnt_reel_col']:.1f}</div>
              <div style="font-size:9px;color:#9CA3AF">CNT</div>
            </div>
            <div style="background:#FEF3C7;border-radius:10px;padding:12px;text-align:center">
              <div style="font-size:9px;color:#D97706;font-weight:700;text-transform:uppercase;margin-bottom:4px">🇨🇴 COL Prév.</div>
              <div style="font-size:20px;font-weight:900;color:#D97706">{row['cnt_prev_col']:.1f}</div>
              <div style="font-size:9px;color:#9CA3AF">CNT</div>
            </div>
          </div>
          <div style="margin-bottom:8px">
            <div style="display:flex;justify-content:space-between;margin-bottom:4px">
              <span style="font-size:11px;color:#6B7280">Solde réel</span>
              <span style="font-size:11px;font-weight:700;color:{pc}">{pr:.0f}%</span>
            </div>
            <div class="prog-track"><div class="prog-fill" style="background:{pc};width:{pr}%"></div></div>
          </div>
          <div>
            <div style="display:flex;justify-content:space-between;margin-bottom:4px">
              <span style="font-size:11px;color:#6B7280">Solde prévisionnel</span>
              <span style="font-size:11px;font-weight:700;color:#D97706">{pp:.0f}%</span>
            </div>
            <div class="prog-track"><div class="prog-fill" style="background:#F59E0B;width:{pp}%"></div></div>
          </div>
        </div>""", unsafe_allow_html=True)

        if pdf_exists:
            with open(pdf_path, "rb") as f:
                pdf_data = f.read()
            c, _ = st.columns([2, 5])
            with c:
                st.download_button(f"📄 {row['licence']}", pdf_data,
                    file_name=licence_to_filename(row["licence"]),
                    mime="application/pdf", key=f"pdf_{row['licence']}", use_container_width=True)
        else:
            st.caption(f"⚠️ PDF manquant → `{pdf_path}`")
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PLANNING CLIENT
# ══════════════════════════════════════════════════════════════════════════════
elif page == "planning":
    st.markdown('<div class="topbar"><div class="topbar-title">Planning client</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="main-wrap">', unsafe_allow_html=True)

    client_sel = st.selectbox("", sorted(commandes["client"].dropna().unique().tolist()),
                               label_visibility="collapsed")
    if client_sel:
        df_c = commandes[commandes["client"] == client_sel].copy()

        st.markdown(f"""
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:26px">
          <div class="kpi-card" style="--card-color:#4361EE;--card-bg:#EEF2FF"><div class="kpi-lbl">Total CNT</div><div class="kpi-val" style="color:#4361EE">{int(df_c["nb_cnt"].sum())}</div></div>
          <div class="kpi-card" style="--card-color:#8B5CF6;--card-bg:#EDE9FE"><div class="kpi-lbl">Total kgs</div><div class="kpi-val" style="color:#7C3AED;font-size:1.5rem">{df_c["total_kgs"].sum():,.0f}</div></div>
          <div class="kpi-card" style="--card-color:#F59E0B;--card-bg:#FEF3C7"><div class="kpi-lbl">⏳ En cours</div><div class="kpi-val" style="color:#D97706">{len(df_c[df_c["statut"].str.contains("À GÉNÉRER", na=False)])}</div></div>
          <div class="kpi-card" style="--card-color:#10B981;--card-bg:#D1FAE5"><div class="kpi-lbl">✅ Confirmées</div><div class="kpi-val" style="color:#059669">{len(df_c[df_c["statut"].str.contains("GÉNÉRÉ", na=False)])}</div></div>
        </div>""", unsafe_allow_html=True)

        for _, row in df_c.sort_values("semaine", ascending=False).iterrows():
            pc = "pill-green" if "GÉNÉRÉ" in str(row["statut"]) else "pill-orange"
            nd = len(list_docs(row["booking"]))
            st.markdown(f"""
            <div class="cmd-row">
              <div><div style="font-size:13px;font-weight:700;color:#111827">{row['booking']}</div>
              <div style="font-size:11px;color:#9CA3AF">{row['semaine']} · {row['licence']}</div></div>
              <div style="text-align:center"><div style="font-size:9px;color:#9CA3AF;margin-bottom:2px">POL</div><div style="font-weight:700;color:#111827">{row['pol']}</div></div>
              <div style="text-align:center"><div style="font-size:9px;color:#9CA3AF;margin-bottom:2px">CNT</div><div style="font-weight:900;color:#4361EE;font-size:20px">{row['nb_cnt']}</div></div>
              <div style="text-align:center"><div style="font-size:9px;color:#9CA3AF;margin-bottom:2px">Départ</div><div style="font-weight:500;color:#374151;font-size:12px">{row['depart']}</div></div>
              <div style="text-align:center"><div style="font-size:9px;color:#9CA3AF;margin-bottom:2px">ETA</div><div style="font-weight:500;color:#374151;font-size:12px">{row['eta']}</div></div>
              <span class="pill pill-blue">📁 {nd}</span>
              <span class="pill {pc}">{row['statut']}</span>
            </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# NOUVELLE COMMANDE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "new_cmd":
    if st.session_state.role != "admin":
        st.error("⛔ Accès réservé aux administrateurs")
        st.stop()

    st.markdown('<div class="topbar"><div class="topbar-title">Nouvelle commande</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="main-wrap">', unsafe_allow_html=True)

    with st.form("form_cmd", clear_on_submit=True):
        f1, f2 = st.columns(2)
        with f1:
            sem        = st.text_input("Semaine *", placeholder="S-26")
            client_sel = st.selectbox("Client *", sorted(clients["nom"].unique().tolist()))
            booking    = st.text_input("Booking *", placeholder="LHV4005547")
            lic_dispo  = clients[clients["nom"] == client_sel]["licence"].tolist()
            lic_sel    = st.selectbox("Licence *", lic_dispo)
        with f2:
            navire  = st.text_input("Navire *", placeholder="CMA CGM EXCELLENCE")
            voyage  = st.text_input("Voyage *", placeholder="0DVOPN1MA")
            pol_sel = st.selectbox("POL *", list(CRTNS.keys()))
            nb_cnt  = st.number_input("CNT *", min_value=1, max_value=100, value=1)

        f3, f4, f5 = st.columns(3)
        with f3: depart  = st.date_input("Départ *", value=date.today())
        with f4: eta     = st.date_input("ETA *",    value=date.today())
        with f5: produit = st.selectbox("Produit *", ["BANANE","ANANAS","MANGUE","AUTRE"])

        crtns_cnt   = CRTNS[pol_sel]
        total_kgs   = round(nb_cnt * crtns_cnt * POIDS_UNIT, 2)
        lic_row     = clients[(clients["nom"] == client_sel) & (clients["licence"] == lic_sel)]
        solde_avant = float(lic_row["solde_reel"].values[0]) if len(lic_row) > 0 else 0
        solde_apres = round(solde_avant - total_kgs, 2)
        cnt_a_cr    = round(solde_apres / KGS_PER_CNT["MOIN(COSTA RICA)"], 2)
        cnt_a_col   = round(solde_apres / KGS_PER_CNT["TURBO(COLOMBIA)"], 2)

        st.markdown("---")
        p1, p2, p3, p4, p5, p6 = st.columns(6)
        p1.metric("Cartons/CNT",     f"{crtns_cnt:,}")
        p2.metric("Total cartons",   f"{nb_cnt * crtns_cnt:,}")
        p3.metric("Total kgs",       f"{total_kgs:,.0f}")
        p4.metric("Solde après",     f"{solde_apres:,.0f}", delta=f"{-total_kgs:,.0f}", delta_color="inverse")
        p5.metric("CNT restants 🇨🇷", f"{cnt_a_cr:.1f}")
        p6.metric("CNT restants 🇨🇴", f"{cnt_a_col:.1f}")

        if   solde_apres < 0:       st.markdown('<div class="alert alert-red">⚠️ Solde insuffisant</div>', unsafe_allow_html=True)
        elif solde_apres < 19591.2: st.markdown('<div class="alert alert-warn">🟠 Solde critique</div>', unsafe_allow_html=True)
        else:                        st.markdown('<div class="alert alert-ok">✅ Solde suffisant</div>', unsafe_allow_html=True)

        if st.form_submit_button("✅ Enregistrer", use_container_width=True,
                                 type="primary", disabled=(solde_apres < 0)):
            st.session_state.new_commandes.append({
                "num": "", "semaine": sem, "client": client_sel, "booking": booking,
                "licence": lic_sel, "navire": navire, "voyage": voyage, "pol": pol_sel,
                "depart": depart.strftime("%d/%m/%Y"), "eta": eta.strftime("%d/%m/%Y"),
                "nb_cnt": nb_cnt, "produit": produit, "statut": "⏳ À GÉNÉRER"
            })
            st.cache_data.clear()
            st.success(f"✅ Commande {booking} enregistrée !")
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
