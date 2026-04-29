import streamlit as st
import pandas as pd
from datetime import datetime, date
import plotly.express as px
import base64
import os

st.set_page_config(page_title="EDEN FOOD", page_icon="🍌", layout="wide",
                   initial_sidebar_state="expanded")

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

header[data-testid="stHeader"],#MainMenu,.stAppDeployButton,footer{display:none!important}

/* ── SIDEBAR TOUJOURS VISIBLE ── */
section[data-testid="stSidebar"]{
    transform:none!important;
    min-width:260px!important;
    max-width:260px!important;
    background:#111!important;
    border-right:none!important;
    position:relative!important;
    visibility:visible!important;
    display:block!important;
}
section[data-testid="stSidebarCollapsedControl"]{display:none!important;width:0!important}
[data-testid="collapsedControl"]{display:none!important}
section[data-testid="stSidebar"] button[data-testid="baseButton-headerNoPadding"]{display:none!important}

section[data-testid="stSidebar"] *{font-family:'Inter',sans-serif!important}
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label{color:#F5F5F7!important}
section[data-testid="stSidebar"] .stButton>button{
    background:transparent!important;border:none!important;
    color:rgba(255,255,255,0.75)!important;text-align:left!important;
    width:100%!important;padding:11px 18px!important;border-radius:10px!important;
    font-size:14px!important;font-weight:500!important;
    transition:all 0.2s!important;margin-bottom:3px!important;
}
section[data-testid="stSidebar"] .stButton>button:hover{
    background:rgba(255,255,255,0.08)!important;color:#fff!important;
}

/* ── GLOBAL ── */
* {font-family:'Inter',sans-serif!important}
.stApp{background:#FAFAFA}
.block-container{padding:0!important;max-width:100%!important}

/* ── HERO ── */
.hero-wrap{position:relative;width:100%;height:420px;overflow:hidden}
.hero-wrap img{width:100%;height:100%;object-fit:cover;object-position:center 40%}
.hero-overlay{
    position:absolute;inset:0;
    background:linear-gradient(to right,rgba(0,0,0,0.70) 0%,rgba(0,0,0,0.20) 65%,rgba(0,0,0,0.0) 100%);
    display:flex;align-items:center;padding:0 64px;
}
.hero-text h1{font-size:44px;font-weight:800;color:#fff;letter-spacing:-1.5px;line-height:1.1;margin:0 0 12px}
.hero-text p{font-size:16px;color:rgba(255,255,255,0.82);font-weight:400;margin:0 0 28px;max-width:480px;line-height:1.6}
.hero-badge{
    display:inline-flex;align-items:center;gap:8px;
    background:rgba(255,255,255,0.15);backdrop-filter:blur(12px);
    border:1px solid rgba(255,255,255,0.25);
    color:#fff;padding:8px 20px;border-radius:30px;font-size:13px;font-weight:600;
}

/* ── LAYOUT ── */
.main-content{padding:40px 48px;max-width:1400px;margin:0 auto}
.page-hdr{padding:40px 48px 0;max-width:1400px;margin:0 auto}
.page-title{font-size:30px;font-weight:800;color:#1D1D1F;letter-spacing:-0.8px;margin:0 0 4px}
.page-sub{font-size:14px;color:#6E6E73;margin:0;font-weight:400}
.week-badge{background:#0071E3;color:#fff;padding:4px 14px;border-radius:20px;font-size:12px;font-weight:700;display:inline-block}
.sec-hdr{font-size:11px;font-weight:700;color:#8E8E93;text-transform:uppercase;letter-spacing:1.2px;margin:32px 0 14px;padding-bottom:10px;border-bottom:1px solid #E5E5EA}

/* ── CARDS ── */
.kpi-grid{display:grid;grid-template-columns:repeat(6,1fr);gap:14px;margin-bottom:36px}
.kpi-card{background:#fff;border-radius:16px;padding:20px 18px;box-shadow:0 1px 3px rgba(0,0,0,0.05),0 4px 12px rgba(0,0,0,0.04);border:1px solid rgba(0,0,0,0.05);transition:transform 0.15s,box-shadow 0.15s}
.kpi-card:hover{transform:translateY(-2px);box-shadow:0 4px 20px rgba(0,0,0,0.08)}
.kpi-lbl{font-size:10px;color:#8E8E93;text-transform:uppercase;letter-spacing:0.9px;font-weight:700;margin-bottom:8px}
.kpi-num{font-size:2rem;font-weight:800;letter-spacing:-1px;line-height:1;margin-bottom:4px}
.kpi-sub{font-size:11px;color:#AEAEB2;font-weight:500}
.card{background:#fff;border-radius:16px;padding:24px;box-shadow:0 1px 3px rgba(0,0,0,0.05),0 4px 12px rgba(0,0,0,0.04);border:1px solid rgba(0,0,0,0.05);margin-bottom:14px}

/* ── ALERTS ── */
.alert-red{background:#FFF2F2;border-left:3px solid #FF3B30;padding:12px 16px;border-radius:10px;color:#C62828;font-size:13px;margin:8px 0;font-weight:600}
.alert-ok{background:#F1FAF4;border-left:3px solid #34C759;padding:12px 16px;border-radius:10px;color:#1B5E20;font-size:13px;margin:8px 0;font-weight:600}
.alert-warn{background:#FFFBF0;border-left:3px solid #FF9F0A;padding:12px 16px;border-radius:10px;color:#7A4F00;font-size:13px;margin:8px 0;font-weight:600}

/* ── FORM ── */
div[data-testid="stForm"]{background:#fff!important;border-radius:16px!important;padding:28px!important;box-shadow:0 1px 3px rgba(0,0,0,0.05)!important;border:1px solid rgba(0,0,0,0.06)!important}
hr{border:none!important;border-top:1px solid #E5E5EA!important;margin:16px 0!important}
div[data-testid="stDataFrame"]{border-radius:12px!important;overflow:hidden!important}
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
             "page": "dashboard", "new_commandes": []}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── HELPERS ───────────────────────────────────────────────────────────────────
def img_to_b64(path):
    try:
        ext  = path.split(".")[-1].lower()
        mime = "jpeg" if ext in ["jpg", "jpeg"] else "png"
        b64  = base64.b64encode(open(path, "rb").read()).decode()
        return f"data:image/{mime};base64,{b64}"
    except:
        return None

CHART_FONT = dict(family="Inter, Arial", size=12, color="#1D1D1F")

def apply_chart_style(fig, bgcolor="#fff"):
    fig.update_layout(
        paper_bgcolor=bgcolor, plot_bgcolor=bgcolor, font=CHART_FONT,
        margin=dict(t=20, b=20, l=20, r=20),
        legend=dict(font=dict(color="#1D1D1F", size=12)),
    )
    fig.update_xaxes(tickfont=dict(color="#1D1D1F"), title_font=dict(color="#1D1D1F"), showgrid=False)
    fig.update_yaxes(tickfont=dict(color="#1D1D1F"), title_font=dict(color="#1D1D1F"), gridcolor="#F0F0F0")
    return fig

# ── LOGIN ─────────────────────────────────────────────────────────────────────
def login_page():
    logo_src = img_to_b64("logo_eden_food.jpg") or img_to_b64("logo_eden_food.png")
    logo_html = (f'<img src="{logo_src}" style="height:56px;margin-bottom:24px;'
                 f'display:block;margin-left:auto;margin-right:auto">'
                 if logo_src else '<div style="font-size:48px;margin-bottom:20px;text-align:center">🍌</div>')

    fond_src = img_to_b64("fond.png") or img_to_b64("fond.jpg")
    bg_css   = f"url('{fond_src}') center center / cover no-repeat fixed" if fond_src \
               else "linear-gradient(135deg,#1a1a2e 0%,#16213e 50%,#0f3460 100%)"

    st.markdown(f"""
    <style>
    .stApp{{background:{bg_css}!important}}
    section[data-testid="stSidebar"]{{display:none!important}}
    section[data-testid="stSidebarCollapsedControl"]{{display:none!important}}
    .login-overlay{{position:fixed;inset:0;background:rgba(0,0,0,0.54);backdrop-filter:blur(3px);z-index:0;pointer-events:none}}
    </style>
    <div class="login-overlay"></div>
    <div style="position:relative;z-index:1;display:flex;align-items:center;
        justify-content:center;min-height:82vh;">
      <div style="background:rgba(255,255,255,0.97);border-radius:28px;
          padding:52px 44px;max-width:420px;width:90%;text-align:center;
          box-shadow:0 32px 80px rgba(0,0,0,0.45);">
        {logo_html}
        <p style="font-size:24px;font-weight:800;color:#1D1D1F;margin:0 0 6px;letter-spacing:-0.5px">Eden Food</p>
        <p style="font-size:14px;color:#6E6E73;margin:0 0 32px;font-weight:400">Logistics Platform · Accès sécurisé</p>
      </div>
    </div>""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        with st.form("login"):
            u = st.text_input("Identifiant", placeholder="ex: yann")
            p = st.text_input("Mot de passe", type="password")
            if st.form_submit_button("Connexion →", use_container_width=True, type="primary"):
                ul = u.strip().lower()
                if ul in USERS and USERS[ul]["password"] == p:
                    st.session_state.update(authenticated=True, username=ul, role=USERS[ul]["role"])
                    st.rerun()
                else:
                    st.error("Identifiant ou mot de passe incorrect")

if not st.session_state.authenticated:
    login_page()
    st.stop()

# ── CONSTANTES ────────────────────────────────────────────────────────────────
POIDS_UNIT  = 18.14
CRTNS       = {"TURBO(COLOMBIA)": 1080, "MOIN(COSTA RICA)": 1200}
KGS_PER_CNT = {"MOIN(COSTA RICA)": 1200 * 18.14, "TURBO(COLOMBIA)": 1080 * 18.14}

def licence_to_filename(lic):
    return str(lic).replace(" ", "_").replace("/", "_") + ".pdf"

def licence_pdf_path(lic):
    return os.path.join("licences", licence_to_filename(lic))

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
    mask = (commandes["client"] == nom) & (commandes["licence"] == lic) & \
           (~commandes["statut"].str.contains("À GÉNÉRER", na=False))
    return round(poids - commandes.loc[mask, "total_kgs"].sum(), 2)

def get_solde_prev(nom, lic, poids):
    mask = (commandes["client"] == nom) & (commandes["licence"] == lic)
    return round(poids - commandes.loc[mask, "total_kgs"].sum(), 2)

clients["solde_reel"]   = clients.apply(lambda r: get_solde_reel(r["nom"], r["licence"], r["poids_total"]), axis=1)
clients["solde_prev"]   = clients.apply(lambda r: get_solde_prev(r["nom"], r["licence"], r["poids_total"]), axis=1)
clients["cnt_reel_cr"]  = (clients["solde_reel"] / KGS_PER_CNT["MOIN(COSTA RICA)"]).round(2)
clients["cnt_reel_col"] = (clients["solde_reel"] / KGS_PER_CNT["TURBO(COLOMBIA)"]).round(2)
clients["cnt_prev_cr"]  = (clients["solde_prev"] / KGS_PER_CNT["MOIN(COSTA RICA)"]).round(2)
clients["cnt_prev_col"] = (clients["solde_prev"] / KGS_PER_CNT["TURBO(COLOMBIA)"]).round(2)

current_week_num  = datetime.now().isocalendar()[1]
current_week_str  = f"S-{current_week_num}"
commandes_semaine = commandes[commandes["semaine"] == current_week_str]

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    logo_src = img_to_b64("logo_eden_food.jpg") or img_to_b64("logo_eden_food.png")
    if logo_src:
        st.markdown(f'<div style="padding:28px 20px 16px"><img src="{logo_src}" style="height:36px"></div>',
                    unsafe_allow_html=True)
    else:
        st.markdown('<div style="padding:28px 20px 16px;color:#fff;font-size:17px;font-weight:800">🍌 EDEN FOOD</div>',
                    unsafe_allow_html=True)

    st.markdown('<div style="height:1px;background:rgba(255,255,255,0.08);margin:0 20px 16px"></div>',
                unsafe_allow_html=True)
    st.markdown('<div style="padding:0 20px 8px;font-size:10px;color:rgba(255,255,255,0.3);'
                'text-transform:uppercase;letter-spacing:1.2px;font-weight:700">Navigation</div>',
                unsafe_allow_html=True)

    NAV = [
        ("dashboard", "🏠", "Dashboard"),
        ("semaine",   "📅", f"Semaine {current_week_str}"),
        ("licences",  "📋", "Licences DPVCT"),
        ("commandes", "🚢", "Commandes"),
        ("planning",  "👤", "Planning client"),
        ("new_cmd",   "➕", "Nouvelle commande"),
    ]
    for pid, icon, label in NAV:
        if st.button(f"{icon}  {label}", key=f"nav_{pid}", use_container_width=True):
            st.session_state.page = pid
            st.rerun()

    st.markdown('<div style="height:1px;background:rgba(255,255,255,0.08);margin:16px 20px 12px"></div>',
                unsafe_allow_html=True)
    st.markdown(f'<div style="padding:4px 20px;color:rgba(255,255,255,0.3);font-size:11px;font-weight:500">'
                f'👤 {st.session_state.username.upper()} · {st.session_state.role}</div>',
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
    logo_ov  = f'<img src="{logo_src}" style="height:42px;margin-bottom:18px;display:block">' if logo_src else ""

    if hero_src:
        st.markdown(f"""
        <div class="hero-wrap">
          <img src="{hero_src}" alt="Eden Food">
          <div class="hero-overlay">
            <div class="hero-text">
              {logo_ov}
              <h1>Fresh from the<br>plantation to the world</h1>
              <p>Suivi en temps réel de vos expéditions, licences DPVCT<br>et planning conteneurs — Colombie & Costa Rica.</p>
              <div class="hero-badge">🍌 &nbsp;{current_week_str} &nbsp;·&nbsp; {len(commandes)} expéditions actives</div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0a1628,#0f3460);padding:64px;margin-bottom:0">
          {logo_ov}
          <h1 style="font-size:42px;font-weight:800;color:#fff;letter-spacing:-1px;margin:0 0 12px">
            Fresh from the plantation to the world</h1>
          <p style="font-size:16px;color:rgba(255,255,255,0.7);margin:0 0 24px;max-width:500px">
            Colombie & Costa Rica — Suivi logistique en temps réel</p>
          <div class="hero-badge">🍌 &nbsp;{current_week_str} &nbsp;·&nbsp; {len(commandes)} expéditions actives</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="main-content">', unsafe_allow_html=True)

    todo   = commandes[commandes["statut"].str.contains("À GÉNÉRER", na=False)]
    done   = commandes[commandes["statut"].str.contains("GÉNÉRÉ",    na=False)]
    alerte = clients[clients["solde_reel"] < 19591.2]

    st.markdown(f"""
    <div class="kpi-grid">
      <div class="kpi-card"><div class="kpi-lbl">Expéditions</div><div class="kpi-num" style="color:#0071E3">{len(commandes)}</div><div class="kpi-sub">total enregistrées</div></div>
      <div class="kpi-card"><div class="kpi-lbl">⏳ À générer</div><div class="kpi-num" style="color:#FF9F0A">{len(todo)}</div><div class="kpi-sub">en attente</div></div>
      <div class="kpi-card"><div class="kpi-lbl">✅ Confirmées</div><div class="kpi-num" style="color:#34C759">{len(done)}</div><div class="kpi-sub">générées</div></div>
      <div class="kpi-card"><div class="kpi-lbl">CNT planifiés</div><div class="kpi-num" style="color:#5856D6">{int(todo["nb_cnt"].sum())}</div><div class="kpi-sub">conteneurs</div></div>
      <div class="kpi-card"><div class="kpi-lbl">🔴 Alertes</div><div class="kpi-num" style="color:#FF3B30">{len(alerte)}</div><div class="kpi-sub">licences critiques</div></div>
      <div class="kpi-card"><div class="kpi-lbl">{current_week_str}</div><div class="kpi-num" style="color:#1D1D1F">{len(commandes_semaine)}</div><div class="kpi-sub">cette semaine</div></div>
    </div>""", unsafe_allow_html=True)

    c1, c2 = st.columns([3, 2])
    with c1:
        st.markdown('<div class="sec-hdr">Dernières expéditions</div>', unsafe_allow_html=True)
        st.dataframe(
            commandes.tail(8)[["semaine","client","booking","pol","nb_cnt","depart","statut"]],
            use_container_width=True, hide_index=True, height=300,
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
        st.markdown('<div class="sec-hdr">Répartition POL</div>', unsafe_allow_html=True)
        if not commandes.empty:
            df_pol = commandes.groupby("pol")["nb_cnt"].sum().reset_index()
            fig = px.pie(df_pol, values="nb_cnt", names="pol", hole=0.65,
                         color_discrete_sequence=["#0071E3","#FF9F0A"])
            fig.update_traces(textinfo="percent+label", textfont=dict(color="#1D1D1F", size=12))
            fig = apply_chart_style(fig, "rgba(0,0,0,0)")
            fig.update_layout(legend=dict(orientation="h", y=-0.15, font=dict(color="#1D1D1F")))
            st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="sec-hdr">Volume hebdomadaire (CNT)</div>', unsafe_allow_html=True)
    if not commandes.empty:
        df_sem = commandes.groupby("semaine")["nb_cnt"].sum().reset_index()
        fig2   = px.bar(df_sem, x="semaine", y="nb_cnt",
                        color_discrete_sequence=["#0071E3"],
                        labels={"semaine": "Semaine", "nb_cnt": "Conteneurs"})
        fig2.update_traces(marker_cornerradius=8)
        fig2 = apply_chart_style(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SEMAINE EN COURS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "semaine":
    st.markdown(f"""
    <div class="page-hdr">
      <p class="page-title">Semaine en cours — {current_week_str}</p>
      <p class="page-sub">Commandes de la semaine {current_week_num} · {datetime.now().year}</p>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="main-content" style="padding-top:24px">', unsafe_allow_html=True)

    if commandes_semaine.empty:
        st.info(f"Aucune commande pour {current_week_str}.")
    else:
        todo_s = commandes_semaine[commandes_semaine["statut"].str.contains("À GÉNÉRER", na=False)]
        done_s = commandes_semaine[commandes_semaine["statut"].str.contains("GÉNÉRÉ",    na=False)]

        st.markdown(f"""
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:32px">
          <div class="kpi-card"><div class="kpi-lbl">Total commandes</div><div class="kpi-num" style="color:#0071E3">{len(commandes_semaine)}</div></div>
          <div class="kpi-card"><div class="kpi-lbl">⏳ À générer</div><div class="kpi-num" style="color:#FF9F0A">{len(todo_s)}</div></div>
          <div class="kpi-card"><div class="kpi-lbl">✅ Confirmées</div><div class="kpi-num" style="color:#34C759">{len(done_s)}</div></div>
          <div class="kpi-card"><div class="kpi-lbl">CNT total</div><div class="kpi-num" style="color:#5856D6">{int(commandes_semaine["nb_cnt"].sum())}</div></div>
        </div>""", unsafe_allow_html=True)

        st.markdown('<div class="sec-hdr">Détail des commandes</div>', unsafe_allow_html=True)
        for _, row in commandes_semaine.iterrows():
            sc = "#34C759" if "GÉNÉRÉ" in str(row["statut"]) else "#FF9F0A"
            sb = "#F1FAF4" if "GÉNÉRÉ" in str(row["statut"]) else "#FFFBF0"
            st.markdown(f"""
            <div class="card" style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px">
              <div>
                <div style="font-size:15px;font-weight:700;color:#1D1D1F">{row['client']}</div>
                <div style="font-size:12px;color:#6E6E73;margin-top:3px">📦 {row['booking']} &nbsp;·&nbsp; 🔑 {row['licence']}</div>
              </div>
              <div style="text-align:center"><div style="font-size:10px;color:#8E8E93;margin-bottom:3px">POL</div><div style="font-weight:700;color:#1D1D1F">{row['pol']}</div></div>
              <div style="text-align:center"><div style="font-size:10px;color:#8E8E93;margin-bottom:3px">CNT</div><div style="font-weight:800;color:#0071E3;font-size:20px">{row['nb_cnt']}</div></div>
              <div style="text-align:center"><div style="font-size:10px;color:#8E8E93;margin-bottom:3px">Départ</div><div style="font-weight:600;color:#1D1D1F">{row['depart']}</div></div>
              <div style="text-align:center"><div style="font-size:10px;color:#8E8E93;margin-bottom:3px">ETA</div><div style="font-weight:600;color:#1D1D1F">{row['eta']}</div></div>
              <div style="background:{sb};color:{sc};padding:7px 18px;border-radius:20px;font-size:12px;font-weight:700">{row['statut']}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# LICENCES DPVCT
# ══════════════════════════════════════════════════════════════════════════════
elif page == "licences":
    st.markdown("""
    <div class="page-hdr">
      <p class="page-title">Licences DPVCT</p>
      <p class="page-sub">Soldes réels & prévisionnels · Capacité en conteneurs · PDF téléchargeables</p>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="main-content" style="padding-top:24px">', unsafe_allow_html=True)

    for _, row in clients.iterrows():
        pct_reel = max(0, min(100, row["solde_reel"] / row["poids_total"] * 100)) if row["poids_total"] > 0 else 0
        pct_prev = max(0, min(100, row["solde_prev"] / row["poids_total"] * 100)) if row["poids_total"] > 0 else 0

        if   row["solde_reel"] < 0:       badge = '<span style="background:#FF3B30;color:#fff;padding:5px 14px;border-radius:20px;font-size:11px;font-weight:700">❌ DÉPASSEMENT</span>'
        elif row["solde_reel"] < 19591.2: badge = '<span style="background:#FF3B30;color:#fff;padding:5px 14px;border-radius:20px;font-size:11px;font-weight:700">🔴 CRITIQUE</span>'
        elif row["solde_reel"] < 58773.6: badge = '<span style="background:#FF9F0A;color:#fff;padding:5px 14px;border-radius:20px;font-size:11px;font-weight:700">⚠️ ATTENTION</span>'
        else:                              badge = '<span style="background:#34C759;color:#fff;padding:5px 14px;border-radius:20px;font-size:11px;font-weight:700">✅ OK</span>'

        pdf_path   = licence_pdf_path(row["licence"])
        pdf_exists = os.path.exists(pdf_path)

        st.markdown(f"""
        <div class="card">
          <div style="display:flex;align-items:flex-start;justify-content:space-between;flex-wrap:wrap;gap:10px;margin-bottom:20px">
            <div>
              <div style="font-size:17px;font-weight:800;color:#1D1D1F">{row['nom']}</div>
              <div style="font-size:13px;color:#6E6E73;margin-top:4px">🔑 {row['licence']} &nbsp;·&nbsp; {row['pays']}</div>
            </div>
            {badge}
          </div>
          <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:20px">
            <div style="background:#F5F5F7;border-radius:12px;padding:16px">
              <div style="font-size:10px;color:#6E6E73;text-transform:uppercase;letter-spacing:0.8px;font-weight:700;margin-bottom:6px">Poids total</div>
              <div style="font-size:22px;font-weight:800;color:#1D1D1F">{row['poids_total']:,.0f}<span style="font-size:13px;font-weight:500;color:#6E6E73"> kgs</span></div>
            </div>
            <div style="background:#EAF4FF;border-radius:12px;padding:16px">
              <div style="font-size:10px;color:#0071E3;text-transform:uppercase;letter-spacing:0.8px;font-weight:700;margin-bottom:6px">Solde réel</div>
              <div style="font-size:22px;font-weight:800;color:#0071E3">{row['solde_reel']:,.0f}<span style="font-size:13px;font-weight:500"> kgs</span></div>
            </div>
            <div style="background:#FFF8EC;border-radius:12px;padding:16px">
              <div style="font-size:10px;color:#FF9F0A;text-transform:uppercase;letter-spacing:0.8px;font-weight:700;margin-bottom:6px">Solde prévisionnel</div>
              <div style="font-size:22px;font-weight:800;color:#FF9F0A">{row['solde_prev']:,.0f}<span style="font-size:13px;font-weight:500"> kgs</span></div>
            </div>
          </div>
          <div style="margin-bottom:20px">
            <div style="font-size:10px;color:#8E8E93;text-transform:uppercase;letter-spacing:1px;font-weight:700;margin-bottom:12px">Capacité restante en conteneurs</div>
            <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px">
              <div style="background:#EAF4FF;border-radius:12px;padding:14px;text-align:center">
                <div style="font-size:9px;color:#0071E3;font-weight:700;text-transform:uppercase;margin-bottom:6px">🇨🇷 CR · Réel</div>
                <div style="font-size:24px;font-weight:900;color:#0071E3;line-height:1">{row['cnt_reel_cr']:.1f}</div>
                <div style="font-size:10px;color:#6E6E73;margin-top:3px">CNT · MOIN</div>
              </div>
              <div style="background:#FFF8EC;border-radius:12px;padding:14px;text-align:center">
                <div style="font-size:9px;color:#FF9F0A;font-weight:700;text-transform:uppercase;margin-bottom:6px">🇨🇷 CR · Prév.</div>
                <div style="font-size:24px;font-weight:900;color:#FF9F0A;line-height:1">{row['cnt_prev_cr']:.1f}</div>
                <div style="font-size:10px;color:#6E6E73;margin-top:3px">CNT · MOIN</div>
              </div>
              <div style="background:#EAF4FF;border-radius:12px;padding:14px;text-align:center">
                <div style="font-size:9px;color:#0071E3;font-weight:700;text-transform:uppercase;margin-bottom:6px">🇨🇴 COL · Réel</div>
                <div style="font-size:24px;font-weight:900;color:#0071E3;line-height:1">{row['cnt_reel_col']:.1f}</div>
                <div style="font-size:10px;color:#6E6E73;margin-top:3px">CNT · TURBO</div>
              </div>
              <div style="background:#FFF8EC;border-radius:12px;padding:14px;text-align:center">
                <div style="font-size:9px;color:#FF9F0A;font-weight:700;text-transform:uppercase;margin-bottom:6px">🇨🇴 COL · Prév.</div>
                <div style="font-size:24px;font-weight:900;color:#FF9F0A;line-height:1">{row['cnt_prev_col']:.1f}</div>
                <div style="font-size:10px;color:#6E6E73;margin-top:3px">CNT · TURBO</div>
              </div>
            </div>
          </div>
          <div style="margin-bottom:10px">
            <div style="display:flex;justify-content:space-between;margin-bottom:5px">
              <span style="font-size:11px;color:#6E6E73;font-weight:500">Solde réel</span>
              <span style="font-size:11px;color:#0071E3;font-weight:700">{pct_reel:.0f}% disponible</span>
            </div>
            <div style="background:#E5E5EA;border-radius:8px;height:6px"><div style="background:#0071E3;width:{pct_reel}%;height:100%;border-radius:8px"></div></div>
          </div>
          <div>
            <div style="display:flex;justify-content:space-between;margin-bottom:5px">
              <span style="font-size:11px;color:#6E6E73;font-weight:500">Solde prévisionnel</span>
              <span style="font-size:11px;color:#FF9F0A;font-weight:700">{pct_prev:.0f}% disponible</span>
            </div>
            <div style="background:#E5E5EA;border-radius:8px;height:6px"><div style="background:#FF9F0A;width:{pct_prev}%;height:100%;border-radius:8px"></div></div>
          </div>
        </div>""", unsafe_allow_html=True)

        if pdf_exists:
            with open(pdf_path, "rb") as f:
                pdf_data = f.read()
            col_pdf, _ = st.columns([2, 5])
            with col_pdf:
                st.download_button(
                    label=f"📄 Télécharger {row['licence']}",
                    data=pdf_data,
                    file_name=licence_to_filename(row["licence"]),
                    mime="application/pdf",
                    key=f"pdf_{row['licence']}",
                    use_container_width=True
                )
        else:
            st.caption(f"⚠️ PDF non trouvé → uploade `{pdf_path}` sur GitHub")

        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# COMMANDES
# ══════════════════════════════════════════════════════════════════════════════
elif page == "commandes":
    st.markdown("""
    <div class="page-hdr">
      <p class="page-title">Commandes</p>
      <p class="page-sub">Toutes les expéditions enregistrées</p>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="main-content" style="padding-top:24px">', unsafe_allow_html=True)

    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        f_statut = st.multiselect("Statut", commandes["statut"].dropna().unique().tolist(),
                                  default=commandes["statut"].dropna().unique().tolist())
    with fc2:
        f_pol    = st.multiselect("POL",    commandes["pol"].dropna().unique().tolist(),
                                  default=commandes["pol"].dropna().unique().tolist())
    with fc3:
        f_client = st.multiselect("Client", commandes["client"].dropna().unique().tolist(),
                                  default=commandes["client"].dropna().unique().tolist())

    df_filt = commandes[
        commandes["statut"].isin(f_statut) &
        commandes["pol"].isin(f_pol) &
        commandes["client"].isin(f_client)
    ][["semaine","booking","client","navire","pol","depart","eta","nb_cnt","total_kgs","licence","statut"]]

    st.dataframe(df_filt, use_container_width=True, height=480, hide_index=True,
        column_config={
            "semaine":   st.column_config.TextColumn("Sem."),
            "booking":   st.column_config.TextColumn("Booking"),
            "client":    st.column_config.TextColumn("Client"),
            "navire":    st.column_config.TextColumn("Navire"),
            "pol":       st.column_config.TextColumn("POL"),
            "depart":    st.column_config.TextColumn("Départ"),
            "eta":       st.column_config.TextColumn("ETA"),
            "nb_cnt":    st.column_config.NumberColumn("CNT", format="%d"),
            "total_kgs": st.column_config.NumberColumn("Kgs", format="%.0f"),
            "licence":   st.column_config.TextColumn("Licence"),
            "statut":    st.column_config.TextColumn("Statut"),
        })
    st.caption(f"**{len(df_filt)} commandes** · {int(df_filt['nb_cnt'].sum())} CNT · {df_filt['total_kgs'].sum():,.0f} kgs")

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PLANNING CLIENT
# ══════════════════════════════════════════════════════════════════════════════
elif page == "planning":
    st.markdown("""
    <div class="page-hdr">
      <p class="page-title">Planning client</p>
      <p class="page-sub">Historique et commandes en cours par client</p>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="main-content" style="padding-top:24px">', unsafe_allow_html=True)

    client_sel = st.selectbox("Sélectionner un client",
                               sorted(commandes["client"].dropna().unique().tolist()))

    if client_sel:
        df_client  = commandes[commandes["client"] == client_sel].copy()
        lic_client = clients[clients["nom"] == client_sel]

        st.markdown(f"""
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin-bottom:32px">
          <div class="kpi-card"><div class="kpi-lbl">Total CNT</div><div class="kpi-num" style="color:#0071E3">{int(df_client["nb_cnt"].sum())}</div></div>
          <div class="kpi-card"><div class="kpi-lbl">Total kgs</div><div class="kpi-num" style="color:#5856D6;font-size:1.4rem">{df_client["total_kgs"].sum():,.0f}</div></div>
          <div class="kpi-card"><div class="kpi-lbl">⏳ En cours</div><div class="kpi-num" style="color:#FF9F0A">{len(df_client[df_client["statut"].str.contains("À GÉNÉRER",na=False)])}</div></div>
          <div class="kpi-card"><div class="kpi-lbl">✅ Confirmées</div><div class="kpi-num" style="color:#34C759">{len(df_client[df_client["statut"].str.contains("GÉNÉRÉ",na=False)])}</div></div>
        </div>""", unsafe_allow_html=True)

        st.markdown(f'<div class="sec-hdr">{client_sel} — {len(df_client)} expédition(s)</div>',
                    unsafe_allow_html=True)

        for _, row in df_client.sort_values("semaine", ascending=False).iterrows():
            sc = "#34C759" if "GÉNÉRÉ" in str(row["statut"]) else "#FF9F0A"
            sb = "#F1FAF4" if "GÉNÉRÉ" in str(row["statut"]) else "#FFFBF0"
            st.markdown(f"""
            <div class="card" style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px">
              <div>
                <div style="font-size:14px;font-weight:700;color:#1D1D1F">{row['booking']}</div>
                <div style="font-size:12px;color:#6E6E73;margin-top:2px">{row['semaine']} &nbsp;·&nbsp; {row['licence']}</div>
              </div>
              <div style="text-align:center"><div style="font-size:10px;color:#8E8E93">Navire</div><div style="font-weight:600;font-size:13px;color:#1D1D1F">{row['navire']}</div></div>
              <div style="text-align:center"><div style="font-size:10px;color:#8E8E93">POL</div><div style="font-weight:700;color:#1D1D1F">{row['pol']}</div></div>
              <div style="text-align:center"><div style="font-size:10px;color:#8E8E93">CNT</div><div style="font-weight:800;color:#0071E3;font-size:20px">{row['nb_cnt']}</div></div>
              <div style="text-align:center"><div style="font-size:10px;color:#8E8E93">Départ</div><div style="font-weight:600;color:#1D1D1F">{row['depart']}</div></div>
              <div style="text-align:center"><div style="font-size:10px;color:#8E8E93">ETA</div><div style="font-weight:600;color:#1D1D1F">{row['eta']}</div></div>
              <div style="background:{sb};color:{sc};padding:7px 18px;border-radius:20px;font-size:12px;font-weight:700">{row['statut']}</div>
            </div>""", unsafe_allow_html=True)

        if not lic_client.empty:
            st.markdown('<div class="sec-hdr">Licences associées</div>', unsafe_allow_html=True)
            for _, lr in lic_client.iterrows():
                pct = max(0, min(100, lr["solde_reel"] / lr["poids_total"] * 100)) if lr["poids_total"] > 0 else 0
                st.markdown(f"""
                <div class="card">
                  <div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px;margin-bottom:14px">
                    <div style="font-weight:800;color:#1D1D1F;font-size:15px">🔑 {lr['licence']}</div>
                    <div style="font-size:13px">Réel : <b style="color:#0071E3">{lr['solde_reel']:,.0f} kgs</b> &nbsp;|&nbsp; Prév. : <b style="color:#FF9F0A">{lr['solde_prev']:,.0f} kgs</b></div>
                  </div>
                  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:14px">
                    <div style="background:#EAF4FF;border-radius:10px;padding:12px;text-align:center">
                      <div style="font-size:9px;color:#0071E3;font-weight:700">🇨🇷 CR Réel</div>
                      <div style="font-size:20px;font-weight:900;color:#0071E3">{lr['cnt_reel_cr']:.1f}</div>
                      <div style="font-size:9px;color:#6E6E73">CNT</div>
                    </div>
                    <div style="background:#FFF8EC;border-radius:10px;padding:12px;text-align:center">
                      <div style="font-size:9px;color:#FF9F0A;font-weight:700">🇨🇷 CR Prév.</div>
                      <div style="font-size:20px;font-weight:900;color:#FF9F0A">{lr['cnt_prev_cr']:.1f}</div>
                      <div style="font-size:9px;color:#6E6E73">CNT</div>
                    </div>
                    <div style="background:#EAF4FF;border-radius:10px;padding:12px;text-align:center">
                      <div style="font-size:9px;color:#0071E3;font-weight:700">🇨🇴 COL Réel</div>
                      <div style="font-size:20px;font-weight:900;color:#0071E3">{lr['cnt_reel_col']:.1f}</div>
                      <div style="font-size:9px;color:#6E6E73">CNT</div>
                    </div>
                    <div style="background:#FFF8EC;border-radius:10px;padding:12px;text-align:center">
                      <div style="font-size:9px;color:#FF9F0A;font-weight:700">🇨🇴 COL Prév.</div>
                      <div style="font-size:20px;font-weight:900;color:#FF9F0A">{lr['cnt_prev_col']:.1f}</div>
                      <div style="font-size:9px;color:#6E6E73">CNT</div>
                    </div>
                  </div>
                  <div style="background:#E5E5EA;border-radius:8px;height:6px">
                    <div style="background:#0071E3;width:{pct}%;height:100%;border-radius:8px"></div>
                  </div>
                </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# NOUVELLE COMMANDE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "new_cmd":
    st.markdown("""
    <div class="page-hdr">
      <p class="page-title">Nouvelle commande</p>
      <p class="page-sub">Les calculs de solde se mettent à jour en temps réel avant validation</p>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="main-content" style="padding-top:24px">', unsafe_allow_html=True)

    with st.form("form_commande", clear_on_submit=True):
        f1, f2 = st.columns(2)
        with f1:
            sem            = st.text_input("Semaine *", placeholder="ex: S-26")
            client_sel     = st.selectbox("Client *", sorted(clients["nom"].unique().tolist()))
            booking        = st.text_input("Référence Booking *", placeholder="ex: LHV4005547")
            licences_dispo = clients[clients["nom"] == client_sel]["licence"].tolist()
            licence_sel    = st.selectbox("N° Licence *", licences_dispo)
        with f2:
            navire  = st.text_input("Navire *", placeholder="ex: CMA CGM EXCELLENCE")
            voyage  = st.text_input("N° Voyage *", placeholder="ex: 0DVOPN1MA")
            pol_sel = st.selectbox("POL *", list(CRTNS.keys()))
            nb_cnt  = st.number_input("Nombre CNT *", min_value=1, max_value=100, value=1)

        f3, f4, f5 = st.columns(3)
        with f3: depart  = st.date_input("Date départ *", value=date.today())
        with f4: eta     = st.date_input("ETA *",          value=date.today())
        with f5: produit = st.selectbox("Produit *", ["BANANE","ANANAS","MANGUE","AUTRE"])

        crtns_cnt     = CRTNS[pol_sel]
        total_crtns   = nb_cnt * crtns_cnt
        total_kgs     = round(total_crtns * POIDS_UNIT, 2)
        lic_row       = clients[(clients["nom"] == client_sel) & (clients["licence"] == licence_sel)]
        solde_avant   = float(lic_row["solde_reel"].values[0]) if len(lic_row) > 0 else 0
        solde_apres   = round(solde_avant - total_kgs, 2)
        cnt_apres_cr  = round(solde_apres / KGS_PER_CNT["MOIN(COSTA RICA)"], 2)
        cnt_apres_col = round(solde_apres / KGS_PER_CNT["TURBO(COLOMBIA)"], 2)

        st.markdown("---")
        p1, p2, p3, p4, p5, p6 = st.columns(6)
        p1.metric("Cartons/CNT",     f"{crtns_cnt:,}")
        p2.metric("Total cartons",   f"{total_crtns:,}")
        p3.metric("Total kgs",       f"{total_kgs:,.0f}")
        p4.metric("Solde après",     f"{solde_apres:,.0f} kgs",
                  delta=f"{-total_kgs:,.0f}", delta_color="inverse")
        p5.metric("CNT restants 🇨🇷", f"{cnt_apres_cr:.1f}")
        p6.metric("CNT restants 🇨🇴", f"{cnt_apres_col:.1f}")

        if   solde_apres < 0:       st.markdown('<div class="alert-red">⚠️ Solde insuffisant — commande bloquée</div>', unsafe_allow_html=True)
        elif solde_apres < 19591.2: st.markdown('<div class="alert-warn">🔴 Solde critique après cette commande</div>', unsafe_allow_html=True)
        else:                        st.markdown('<div class="alert-ok">✅ Solde suffisant après cette commande</div>', unsafe_allow_html=True)

        submitted = st.form_submit_button("✅ Enregistrer la commande",
                        use_container_width=True, type="primary",
                        disabled=(solde_apres < 0))

        if submitted:
            st.session_state.new_commandes.append({
                "num": "", "semaine": sem, "client": client_sel,
                "booking": booking, "licence": licence_sel,
                "navire": navire, "voyage": voyage, "pol": pol_sel,
                "depart": depart.strftime("%d/%m/%Y"),
                "eta":    eta.strftime("%d/%m/%Y"),
                "nb_cnt": nb_cnt, "produit": produit, "statut": "⏳ À GÉNÉRER"
            })
            st.cache_data.clear()
            st.success(f"✅ Commande {booking} enregistrée !")
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
