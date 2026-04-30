import streamlit as st
import pandas as pd
from datetime import datetime, date
import plotly.express as px
import base64
import os
import json

st.set_page_config(page_title="EDEN FOOD", page_icon="🍌", layout="wide",
                   initial_sidebar_state="expanded")

# ── CSS CARGO PRODUCE STYLE ───────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

header[data-testid="stHeader"],#MainMenu,.stAppDeployButton,footer{display:none!important}

/* ── SIDEBAR FIXE BLANCHE ── */
section[data-testid="stSidebar"]{
    transform:none!important;
    min-width:220px!important;
    max-width:220px!important;
    background:#fff!important;
    border-right:1px solid #E8EAED!important;
    position:relative!important;
    visibility:visible!important;
    display:block!important;
    box-shadow:2px 0 8px rgba(0,0,0,0.04)!important;
}
section[data-testid="stSidebarCollapsedControl"]{display:none!important;width:0!important}
[data-testid="collapsedControl"]{display:none!important}
section[data-testid="stSidebar"] button[data-testid="baseButton-headerNoPadding"]{display:none!important}

section[data-testid="stSidebar"] *{font-family:'Inter',sans-serif!important}
section[data-testid="stSidebar"] .stButton>button{
    background:transparent!important;border:none!important;
    color:#5F6368!important;text-align:left!important;
    width:100%!important;padding:9px 16px!important;border-radius:8px!important;
    font-size:13px!important;font-weight:500!important;
    transition:all 0.15s!important;margin-bottom:2px!important;
}
section[data-testid="stSidebar"] .stButton>button:hover{
    background:#F0F4FF!important;color:#3B5BDB!important;
}

/* ── GLOBAL ── */
*{font-family:'Inter',sans-serif!important}
.stApp{background:#F8F9FB}
.block-container{padding:0!important;max-width:100%!important}

/* ── TOP BAR ── */
.topbar{
    background:#fff;border-bottom:1px solid #E8EAED;
    padding:16px 32px;display:flex;align-items:center;
    justify-content:space-between;position:sticky;top:0;z-index:100;
}
.topbar-title{font-size:20px;font-weight:700;color:#1A1A2E;letter-spacing:-0.3px}
.topbar-sub{font-size:12px;color:#9AA0AB;margin-top:2px;font-weight:400}

/* ── FILTER BAR ── */
.filter-bar{
    background:#fff;border-bottom:1px solid #E8EAED;
    padding:10px 32px;display:flex;gap:8px;align-items:center;flex-wrap:wrap;
}

/* ── MAIN ── */
.main-wrap{padding:24px 32px;max-width:1500px;margin:0 auto}

/* ── KPI ── */
.kpi-row{display:grid;grid-template-columns:repeat(6,1fr);gap:12px;margin-bottom:24px}
.kpi-box{
    background:#fff;border-radius:12px;padding:18px 16px;
    border:1px solid #E8EAED;
    transition:box-shadow 0.15s;
}
.kpi-box:hover{box-shadow:0 4px 16px rgba(0,0,0,0.08)}
.kpi-box .val{font-size:1.9rem;font-weight:800;color:#1A1A2E;letter-spacing:-1px;line-height:1;margin:6px 0 3px}
.kpi-box .lbl{font-size:10px;color:#9AA0AB;text-transform:uppercase;letter-spacing:0.8px;font-weight:700}
.kpi-box .sub{font-size:11px;color:#C4C9D4;font-weight:500}

/* ── TABLE SECTION ── */
.section-hdr{
    display:flex;align-items:center;justify-content:space-between;
    margin-bottom:14px;
}
.section-title{font-size:13px;font-weight:700;color:#1A1A2E;letter-spacing:-0.2px}
.section-sub{font-size:11px;color:#9AA0AB}

/* ── STATUS PILLS ── */
.pill-green{background:#E8F5E9;color:#2E7D32;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700;display:inline-block}
.pill-orange{background:#FFF3E0;color:#E65100;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700;display:inline-block}
.pill-red{background:#FFEBEE;color:#C62828;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700;display:inline-block}
.pill-blue{background:#E3F2FD;color:#1565C0;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700;display:inline-block}

/* ── COMMANDE ROW ── */
.cmd-row{
    background:#fff;border:1px solid #E8EAED;border-radius:10px;
    padding:16px 20px;margin-bottom:8px;
    display:flex;align-items:center;justify-content:space-between;
    flex-wrap:wrap;gap:12px;
    transition:box-shadow 0.15s,border-color 0.15s;
}
.cmd-row:hover{box-shadow:0 4px 14px rgba(0,0,0,0.07);border-color:#C7D2FE}

/* ── DOC SECTION ── */
.doc-zone{
    background:#F8F9FB;border:1.5px dashed #CBD5E1;
    border-radius:10px;padding:20px;margin-top:12px;
}
.doc-chip{
    display:inline-flex;align-items:center;gap:6px;
    background:#fff;border:1px solid #E8EAED;border-radius:8px;
    padding:6px 12px;font-size:12px;color:#374151;font-weight:500;
    margin:4px;
}

/* ── CARDS ── */
.card{background:#fff;border-radius:12px;padding:20px 24px;border:1px solid #E8EAED;margin-bottom:12px}

/* ── HERO ── */
.hero-wrap{position:relative;width:100%;height:280px;overflow:hidden}
.hero-wrap img{width:100%;height:100%;object-fit:cover;object-position:center 35%}
.hero-overlay{
    position:absolute;inset:0;
    background:linear-gradient(to right,rgba(10,20,60,0.78) 0%,rgba(10,20,60,0.25) 70%,transparent 100%);
    display:flex;align-items:center;padding:0 48px;
}
.hero-text h1{font-size:32px;font-weight:800;color:#fff;letter-spacing:-1px;line-height:1.15;margin:0 0 10px}
.hero-text p{font-size:14px;color:rgba(255,255,255,0.8);margin:0 0 20px;max-width:420px;line-height:1.6}
.hero-badge{display:inline-flex;align-items:center;gap:6px;background:rgba(255,255,255,0.15);backdrop-filter:blur(10px);border:1px solid rgba(255,255,255,0.25);color:#fff;padding:6px 16px;border-radius:24px;font-size:12px;font-weight:600}

/* ── ALERTS ── */
.alert-ok{background:#E8F5E9;border-left:3px solid #4CAF50;padding:10px 14px;border-radius:8px;color:#1B5E20;font-size:12px;margin:6px 0;font-weight:600}
.alert-warn{background:#FFF8E1;border-left:3px solid #FF9800;padding:10px 14px;border-radius:8px;color:#7A4F00;font-size:12px;margin:6px 0;font-weight:600}
.alert-red{background:#FFEBEE;border-left:3px solid #F44336;padding:10px 14px;border-radius:8px;color:#C62828;font-size:12px;margin:6px 0;font-weight:600}

/* ── FORM ── */
div[data-testid="stForm"]{background:#fff!important;border-radius:12px!important;padding:24px!important;border:1px solid #E8EAED!important;box-shadow:none!important}
div[data-testid="stDataFrame"]{border-radius:10px!important;overflow:hidden!important}
hr{border:none!important;border-top:1px solid #E8EAED!important;margin:14px 0!important}
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
             "page": "dashboard", "new_commandes": [],
             "expanded_cmd": None}.items():
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

CHART_FONT = dict(family="Inter, Arial", size=12, color="#1A1A2E")

def apply_chart_style(fig, bgcolor="#fff"):
    fig.update_layout(paper_bgcolor=bgcolor, plot_bgcolor=bgcolor, font=CHART_FONT,
        margin=dict(t=20,b=20,l=20,r=20), legend=dict(font=dict(color="#1A1A2E",size=12)))
    fig.update_xaxes(tickfont=dict(color="#1A1A2E"), title_font=dict(color="#1A1A2E"), showgrid=False)
    fig.update_yaxes(tickfont=dict(color="#1A1A2E"), title_font=dict(color="#1A1A2E"), gridcolor="#F0F2F5")
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
    p   = docs_path(booking)
    fp  = os.path.join(p, uploaded_file.name)
    with open(fp, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return fp

def delete_doc(booking, filename):
    fp = os.path.join(docs_path(booking), filename)
    if os.path.exists(fp):
        os.remove(fp)

# ── LOGIN ─────────────────────────────────────────────────────────────────────
def login_page():
    logo_src = img_to_b64("logo_eden_food.jpg") or img_to_b64("logo_eden_food.png")
    logo_html = (f'<img src="{logo_src}" style="height:52px;margin-bottom:22px;display:block;margin-left:auto;margin-right:auto">'
                 if logo_src else '<div style="font-size:44px;margin-bottom:20px;text-align:center">🍌</div>')
    fond_src = img_to_b64("fond.png") or img_to_b64("fond.jpg")
    bg_css   = f"url('{fond_src}') center center / cover no-repeat fixed" if fond_src \
               else "linear-gradient(135deg,#1a1a2e 0%,#16213e 50%,#0f3460 100%)"

    st.markdown(f"""
    <style>
    .stApp{{background:{bg_css}!important}}
    section[data-testid="stSidebar"]{{display:none!important}}
    section[data-testid="stSidebarCollapsedControl"]{{display:none!important}}
    .login-overlay{{position:fixed;inset:0;background:rgba(0,0,0,0.52);backdrop-filter:blur(3px);z-index:0;pointer-events:none}}
    </style>
    <div class="login-overlay"></div>
    <div style="position:relative;z-index:1;display:flex;align-items:center;justify-content:center;min-height:82vh;">
      <div style="background:rgba(255,255,255,0.98);border-radius:24px;padding:48px 42px;
          max-width:400px;width:90%;text-align:center;box-shadow:0 24px 64px rgba(0,0,0,0.4);">
        {logo_html}
        <p style="font-size:22px;font-weight:800;color:#1A1A2E;margin:0 0 4px;letter-spacing:-0.5px">Eden Food</p>
        <p style="font-size:13px;color:#9AA0AB;margin:0 0 28px">Logistics Platform · Accès sécurisé</p>
      </div>
    </div>""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1,2,1])
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
KGS_PER_CNT = {"MOIN(COSTA RICA)": 1200*18.14, "TURBO(COLOMBIA)": 1080*18.14}

def licence_to_filename(lic):
    return str(lic).replace(" ","_").replace("/","_") + ".pdf"
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
    mask = (commandes["client"]==nom)&(commandes["licence"]==lic)&(~commandes["statut"].str.contains("À GÉNÉRER",na=False))
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
        st.markdown(f'<div style="padding:24px 16px 12px"><img src="{logo_src}" style="height:32px"></div>',
                    unsafe_allow_html=True)
    else:
        st.markdown('<div style="padding:24px 16px 12px;font-size:15px;font-weight:800;color:#1A1A2E">🍌 EDEN FOOD</div>',
                    unsafe_allow_html=True)

    st.markdown('<div style="height:1px;background:#E8EAED;margin:0 16px 12px"></div>', unsafe_allow_html=True)
    st.markdown('<div style="padding:0 16px 6px;font-size:10px;color:#C4C9D4;text-transform:uppercase;letter-spacing:1.2px;font-weight:700">Menu principal</div>',
                unsafe_allow_html=True)

    NAV = [
        ("dashboard", "🏠", "Overview"),
        ("semaine",   "📅", f"Semaine {current_week_str}"),
        ("commandes", "🚢", "Commandes"),
        ("documents", "📁", "Documents"),
        ("licences",  "📋", "Licences DPVCT"),
        ("planning",  "👤", "Planning client"),
    ]
    for pid, icon, label in NAV:
        if st.button(f"{icon}  {label}", key=f"nav_{pid}", use_container_width=True):
            st.session_state.page = pid
            st.rerun()

    if st.session_state.role == "admin":
        st.markdown('<div style="height:1px;background:#E8EAED;margin:8px 16px"></div>', unsafe_allow_html=True)
        st.markdown('<div style="padding:0 16px 6px;font-size:10px;color:#C4C9D4;text-transform:uppercase;letter-spacing:1.2px;font-weight:700">Admin</div>',
                    unsafe_allow_html=True)
        if st.button("➕  Nouvelle commande", key="nav_new_cmd", use_container_width=True):
            st.session_state.page = "new_cmd"
            st.rerun()

    st.markdown('<div style="height:1px;background:#E8EAED;margin:12px 16px 8px"></div>', unsafe_allow_html=True)
    st.markdown(f'<div style="padding:4px 16px;color:#C4C9D4;font-size:11px">👤 {st.session_state.username.upper()} · {st.session_state.role}</div>',
                unsafe_allow_html=True)
    if st.button("🚪  Déconnexion", use_container_width=True, key="logout"):
        st.session_state.update(authenticated=False, username="")
        st.rerun()

page = st.session_state.page

# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD / OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
if page == "dashboard":

    hero_src = img_to_b64("hero.jpg") or img_to_b64("hero.png")
    logo_src = img_to_b64("logo_eden_food.jpg") or img_to_b64("logo_eden_food.png")
    logo_ov  = f'<img src="{logo_src}" style="height:38px;margin-bottom:14px;display:block">' if logo_src else ""

    if hero_src:
        st.markdown(f"""
        <div class="hero-wrap">
          <img src="{hero_src}" alt="Eden Food">
          <div class="hero-overlay">
            <div class="hero-text">
              {logo_ov}
              <h1>Fresh from the<br>plantation to the world</h1>
              <p>Suivi en temps réel — Colombie & Costa Rica</p>
              <div class="hero-badge">🍌 &nbsp;{current_week_str} &nbsp;·&nbsp; {len(commandes)} expéditions</div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="main-wrap">', unsafe_allow_html=True)

    todo   = commandes[commandes["statut"].str.contains("À GÉNÉRER", na=False)]
    done   = commandes[commandes["statut"].str.contains("GÉNÉRÉ",    na=False)]
    alerte = clients[clients["solde_reel"] < 19591.2]

    # Compter les docs uploadés
    total_docs = sum(len(list_docs(b)) for b in commandes["booking"].dropna().unique())

    st.markdown(f"""
    <div class="kpi-row">
      <div class="kpi-box"><div class="lbl">Expéditions</div><div class="val" style="color:#3B5BDB">{len(commandes)}</div><div class="sub">enregistrées</div></div>
      <div class="kpi-box"><div class="lbl">⏳ À générer</div><div class="val" style="color:#E65100">{len(todo)}</div><div class="sub">en attente</div></div>
      <div class="kpi-box"><div class="lbl">✅ Confirmées</div><div class="val" style="color:#2E7D32">{len(done)}</div><div class="sub">générées</div></div>
      <div class="kpi-box"><div class="lbl">📦 CNT</div><div class="val" style="color:#6D28D9">{int(todo["nb_cnt"].sum())}</div><div class="sub">planifiés</div></div>
      <div class="kpi-box"><div class="lbl">🔴 Alertes</div><div class="val" style="color:#C62828">{len(alerte)}</div><div class="sub">licences critiques</div></div>
      <div class="kpi-box"><div class="lbl">📁 Documents</div><div class="val" style="color:#0277BD">{total_docs}</div><div class="sub">uploadés</div></div>
    </div>""", unsafe_allow_html=True)

    c1, c2 = st.columns([3,2])
    with c1:
        st.markdown('<div class="section-hdr"><span class="section-title">Dernières expéditions</span></div>', unsafe_allow_html=True)
        st.dataframe(
            commandes.tail(10)[["semaine","client","booking","pol","nb_cnt","depart","statut"]],
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
        st.markdown('<div class="section-hdr"><span class="section-title">Répartition POL</span></div>', unsafe_allow_html=True)
        if not commandes.empty:
            df_pol = commandes.groupby("pol")["nb_cnt"].sum().reset_index()
            fig = px.pie(df_pol, values="nb_cnt", names="pol", hole=0.6,
                         color_discrete_sequence=["#3B5BDB","#F59E0B"])
            fig.update_traces(textinfo="percent+label", textfont=dict(color="#1A1A2E",size=12))
            fig = apply_chart_style(fig, "rgba(0,0,0,0)")
            fig.update_layout(legend=dict(orientation="h",y=-0.15,font=dict(color="#1A1A2E")))
            st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section-hdr" style="margin-top:24px"><span class="section-title">Volume hebdomadaire (CNT)</span></div>', unsafe_allow_html=True)
    if not commandes.empty:
        df_sem = commandes.groupby("semaine")["nb_cnt"].sum().reset_index()
        fig2   = px.bar(df_sem, x="semaine", y="nb_cnt",
                        color_discrete_sequence=["#3B5BDB"],
                        labels={"semaine":"Semaine","nb_cnt":"Conteneurs"})
        fig2.update_traces(marker_cornerradius=6)
        fig2 = apply_chart_style(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SEMAINE EN COURS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "semaine":
    st.markdown(f"""
    <div class="topbar">
      <div>
        <div class="topbar-title">Semaine en cours — {current_week_str}</div>
        <div class="topbar-sub">Commandes actives · Semaine {current_week_num} · {datetime.now().year}</div>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="main-wrap">', unsafe_allow_html=True)

    if commandes_semaine.empty:
        st.info(f"Aucune commande pour {current_week_str}.")
    else:
        todo_s = commandes_semaine[commandes_semaine["statut"].str.contains("À GÉNÉRER",na=False)]
        done_s = commandes_semaine[commandes_semaine["statut"].str.contains("GÉNÉRÉ",na=False)]

        st.markdown(f"""
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:24px">
          <div class="kpi-box"><div class="lbl">Total</div><div class="val" style="color:#3B5BDB">{len(commandes_semaine)}</div></div>
          <div class="kpi-box"><div class="lbl">⏳ À générer</div><div class="val" style="color:#E65100">{len(todo_s)}</div></div>
          <div class="kpi-box"><div class="lbl">✅ Confirmées</div><div class="val" style="color:#2E7D32">{len(done_s)}</div></div>
          <div class="kpi-box"><div class="lbl">CNT total</div><div class="val" style="color:#6D28D9">{int(commandes_semaine["nb_cnt"].sum())}</div></div>
        </div>""", unsafe_allow_html=True)

        for _, row in commandes_semaine.iterrows():
            sc = "#2E7D32" if "GÉNÉRÉ" in str(row["statut"]) else "#E65100"
            sb = "#E8F5E9" if "GÉNÉRÉ" in str(row["statut"]) else "#FFF3E0"
            n_docs = len(list_docs(row["booking"]))
            doc_badge = f'<span style="background:#E3F2FD;color:#1565C0;padding:2px 8px;border-radius:12px;font-size:10px;font-weight:700">📁 {n_docs} doc{"s" if n_docs>1 else ""}</span>' if n_docs > 0 else ""
            st.markdown(f"""
            <div class="cmd-row">
              <div>
                <div style="font-size:14px;font-weight:700;color:#1A1A2E">{row['client']}</div>
                <div style="font-size:11px;color:#9AA0AB;margin-top:3px">📦 {row['booking']} &nbsp;·&nbsp; 🔑 {row['licence']} &nbsp;{doc_badge}</div>
              </div>
              <div style="text-align:center"><div style="font-size:9px;color:#9AA0AB;margin-bottom:3px">POL</div><div style="font-weight:700;color:#1A1A2E;font-size:12px">{row['pol']}</div></div>
              <div style="text-align:center"><div style="font-size:9px;color:#9AA0AB;margin-bottom:3px">CNT</div><div style="font-weight:800;color:#3B5BDB;font-size:20px">{row['nb_cnt']}</div></div>
              <div style="text-align:center"><div style="font-size:9px;color:#9AA0AB;margin-bottom:3px">Départ</div><div style="font-weight:600;color:#1A1A2E;font-size:12px">{row['depart']}</div></div>
              <div style="text-align:center"><div style="font-size:9px;color:#9AA0AB;margin-bottom:3px">ETA</div><div style="font-weight:600;color:#1A1A2E;font-size:12px">{row['eta']}</div></div>
              <div style="background:{sb};color:{sc};padding:5px 14px;border-radius:16px;font-size:11px;font-weight:700">{row['statut']}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# COMMANDES — avec gestion documents inline
# ══════════════════════════════════════════════════════════════════════════════
elif page == "commandes":
    st.markdown("""
    <div class="topbar">
      <div>
        <div class="topbar-title">Commandes</div>
        <div class="topbar-sub">Toutes les expéditions · Cliquer sur une ligne pour gérer les documents</div>
      </div>
    </div>""", unsafe_allow_html=True)

    # Filtres style Cargo Produce
    st.markdown('<div style="background:#fff;border-bottom:1px solid #E8EAED;padding:12px 32px">', unsafe_allow_html=True)
    fc1, fc2, fc3, fc4 = st.columns([2,2,2,1])
    with fc1:
        f_client = st.multiselect("Client", commandes["client"].dropna().unique().tolist(),
                                  default=commandes["client"].dropna().unique().tolist(), label_visibility="collapsed",
                                  placeholder="🔍 Filtrer par client")
    with fc2:
        f_pol    = st.multiselect("POL",    commandes["pol"].dropna().unique().tolist(),
                                  default=commandes["pol"].dropna().unique().tolist(), label_visibility="collapsed",
                                  placeholder="🌍 Filtrer par POL")
    with fc3:
        f_statut = st.multiselect("Statut", commandes["statut"].dropna().unique().tolist(),
                                  default=commandes["statut"].dropna().unique().tolist(), label_visibility="collapsed",
                                  placeholder="📊 Filtrer par statut")
    with fc4:
        f_sem = st.text_input("Semaine", placeholder="ex: S-18", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="main-wrap">', unsafe_allow_html=True)

    df_filt = commandes[
        commandes["client"].isin(f_client) &
        commandes["pol"].isin(f_pol) &
        commandes["statut"].isin(f_statut)
    ]
    if f_sem:
        df_filt = df_filt[df_filt["semaine"].str.contains(f_sem, case=False, na=False)]

    st.caption(f"**{len(df_filt)} commandes** · {int(df_filt['nb_cnt'].sum())} CNT · {df_filt['total_kgs'].sum():,.0f} kgs")
    st.markdown("")

    for _, row in df_filt.iterrows():
        sc = "#2E7D32" if "GÉNÉRÉ" in str(row["statut"]) else "#E65100"
        sb = "#E8F5E9" if "GÉNÉRÉ" in str(row["statut"]) else "#FFF3E0"
        n_docs = len(list_docs(row["booking"]))
        doc_badge = f'<span style="background:#E3F2FD;color:#1565C0;padding:2px 8px;border-radius:12px;font-size:10px;font-weight:700">📁 {n_docs} doc{"s" if n_docs>1 else ""}</span>' if n_docs > 0 else '<span style="background:#F5F5F5;color:#9AA0AB;padding:2px 8px;border-radius:12px;font-size:10px">📁 Aucun doc</span>'

        st.markdown(f"""
        <div class="cmd-row">
          <div style="min-width:200px">
            <div style="font-size:13px;font-weight:700;color:#1A1A2E">{row['client']}</div>
            <div style="font-size:11px;color:#9AA0AB;margin-top:3px">{row['semaine']} &nbsp;·&nbsp; {row['booking']}</div>
          </div>
          <div style="text-align:center"><div style="font-size:9px;color:#9AA0AB;margin-bottom:2px">Navire</div><div style="font-weight:600;color:#374151;font-size:11px">{row['navire']}</div></div>
          <div style="text-align:center"><div style="font-size:9px;color:#9AA0AB;margin-bottom:2px">POL</div><div style="font-weight:700;color:#1A1A2E;font-size:12px">{row['pol']}</div></div>
          <div style="text-align:center"><div style="font-size:9px;color:#9AA0AB;margin-bottom:2px">CNT</div><div style="font-weight:800;color:#3B5BDB;font-size:18px">{row['nb_cnt']}</div></div>
          <div style="text-align:center"><div style="font-size:9px;color:#9AA0AB;margin-bottom:2px">Départ</div><div style="font-weight:600;color:#374151;font-size:11px">{row['depart']}</div></div>
          <div style="text-align:center"><div style="font-size:9px;color:#9AA0AB;margin-bottom:2px">ETA</div><div style="font-weight:600;color:#374151;font-size:11px">{row['eta']}</div></div>
          <div>{doc_badge}</div>
          <div style="background:{sb};color:{sc};padding:4px 12px;border-radius:14px;font-size:11px;font-weight:700">{row['statut']}</div>
        </div>""", unsafe_allow_html=True)

        # Bouton pour ouvrir/fermer les documents de cette commande
        btn_key = f"docs_btn_{row['booking']}"
        is_open = st.session_state.expanded_cmd == row['booking']

        col_btn, _ = st.columns([1,4])
        with col_btn:
            btn_label = "🔼 Fermer documents" if is_open else "📁 Gérer documents"
            if st.button(btn_label, key=btn_key, use_container_width=True):
                st.session_state.expanded_cmd = None if is_open else row['booking']
                st.rerun()

        # Zone documents expandée
        if is_open:
            st.markdown(f"""
            <div class="doc-zone">
              <div style="font-size:12px;font-weight:700;color:#1A1A2E;margin-bottom:12px">
                📁 Documents — {row['booking']} · {row['client']}
              </div>
            </div>""", unsafe_allow_html=True)

            existing_docs = list_docs(row['booking'])
            if existing_docs:
                st.markdown("**Documents disponibles :**")
                for doc_name in existing_docs:
                    doc_path = os.path.join(docs_path(row['booking']), doc_name)
                    d1, d2, d3 = st.columns([3,1,1])
                    with d1:
                        st.markdown(f'<div class="doc-chip">📄 {doc_name}</div>', unsafe_allow_html=True)
                    with d2:
                        with open(doc_path, "rb") as f:
                            st.download_button("⬇️ DL", f.read(),
                                file_name=doc_name,
                                key=f"dl_{row['booking']}_{doc_name}",
                                use_container_width=True)
                    with d3:
                        if st.session_state.role == "admin":
                            if st.button("🗑️", key=f"del_{row['booking']}_{doc_name}",
                                         use_container_width=True):
                                delete_doc(row['booking'], doc_name)
                                st.rerun()
            else:
                st.caption("Aucun document uploadé pour cette commande.")

            st.markdown("**Uploader un document :**")
            u1, u2 = st.columns([2,1])
            with u1:
                uploaded = st.file_uploader(
                    f"Fichier pour {row['booking']}",
                    type=["pdf","xlsx","xls","docx","jpg","png","jpeg"],
                    key=f"upload_{row['booking']}",
                    label_visibility="collapsed"
                )
            with u2:
                doc_type = st.selectbox("Type", DOC_TYPES,
                    key=f"dtype_{row['booking']}",
                    label_visibility="collapsed")

            if uploaded is not None:
                # Renommer le fichier avec le type
                ext = uploaded.name.split(".")[-1]
                new_name = f"{doc_type.replace(' ','_')}_{row['booking']}_{uploaded.name}"
                uploaded.name = new_name
                if st.button(f"✅ Confirmer l'upload", key=f"confirm_{row['booking']}",
                             use_container_width=False, type="primary"):
                    save_doc(row['booking'], uploaded)
                    st.success(f"✅ {uploaded.name} uploadé avec succès !")
                    st.rerun()

            st.markdown("")

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# DOCUMENTS — Centre de documents global
# ══════════════════════════════════════════════════════════════════════════════
elif page == "documents":
    st.markdown("""
    <div class="topbar">
      <div>
        <div class="topbar-title">Documents</div>
        <div class="topbar-sub">Tous les documents uploadés par commande</div>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="main-wrap">', unsafe_allow_html=True)

    # Stats globales
    all_bookings = commandes["booking"].dropna().unique()
    total_docs   = sum(len(list_docs(b)) for b in all_bookings)
    cmds_avec    = sum(1 for b in all_bookings if len(list_docs(b)) > 0)
    cmds_sans    = len(all_bookings) - cmds_avec

    st.markdown(f"""
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:24px">
      <div class="kpi-box"><div class="lbl">Total documents</div><div class="val" style="color:#0277BD">{total_docs}</div><div class="sub">tous types</div></div>
      <div class="kpi-box"><div class="lbl">✅ Commandes documentées</div><div class="val" style="color:#2E7D32">{cmds_avec}</div><div class="sub">avec au moins 1 doc</div></div>
      <div class="kpi-box"><div class="lbl">⚠️ Sans documents</div><div class="val" style="color:#E65100">{cmds_sans}</div><div class="sub">à compléter</div></div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-hdr"><span class="section-title">Rechercher une commande</span></div>', unsafe_allow_html=True)

    search = st.text_input("Rechercher par booking ou client", placeholder="🔍 ex: LHV4005539 ou GENERAL FRUITS",
                           label_visibility="collapsed")

    for _, row in commandes.iterrows():
        if search and search.lower() not in str(row["booking"]).lower() and search.lower() not in str(row["client"]).lower():
            continue

        docs = list_docs(row["booking"])
        n    = len(docs)

        border_color = "#4CAF50" if n >= 3 else ("#FF9800" if n >= 1 else "#EF5350")
        label_color  = "#2E7D32" if n >= 3 else ("#E65100" if n >= 1 else "#C62828")
        label_text   = f"✅ {n} doc{'s' if n>1 else ''}" if n > 0 else "⚠️ Aucun doc"

        st.markdown(f"""
        <div class="cmd-row" style="border-left:3px solid {border_color}">
          <div style="min-width:220px">
            <div style="font-size:13px;font-weight:700;color:#1A1A2E">{row['client']}</div>
            <div style="font-size:11px;color:#9AA0AB;margin-top:2px">{row['booking']} &nbsp;·&nbsp; {row['semaine']}</div>
          </div>
          <div><span style="color:{label_color};font-weight:700;font-size:12px">{label_text}</span></div>
          <div style="display:flex;flex-wrap:wrap;gap:4px">
            {"".join([f'<span class="doc-chip">📄 {d}</span>' for d in docs]) if docs else '<span style="color:#9AA0AB;font-size:11px;font-style:italic">Aucun fichier</span>'}
          </div>
        </div>""", unsafe_allow_html=True)

        # Upload rapide depuis cette page
        with st.expander(f"📤 Uploader pour {row['booking']}", expanded=False):
            u1, u2 = st.columns([2,1])
            with u1:
                upf = st.file_uploader("Fichier", type=["pdf","xlsx","xls","docx","jpg","png","jpeg"],
                                       key=f"doc_upload_global_{row['booking']}",
                                       label_visibility="collapsed")
            with u2:
                dtype = st.selectbox("Type", DOC_TYPES,
                                     key=f"doc_type_global_{row['booking']}",
                                     label_visibility="collapsed")
            if upf and st.button("✅ Uploader", key=f"up_confirm_global_{row['booking']}", type="primary"):
                upf.name = f"{dtype.replace(' ','_')}_{row['booking']}_{upf.name}"
                save_doc(row["booking"], upf)
                st.success(f"✅ Uploadé !")
                st.rerun()

            # Téléchargements existants
            if docs:
                st.markdown("**Télécharger :**")
                for doc_name in docs:
                    doc_path = os.path.join(docs_path(row["booking"]), doc_name)
                    col_n, col_dl = st.columns([3,1])
                    with col_n:
                        st.markdown(f"📄 `{doc_name}`")
                    with col_dl:
                        with open(doc_path, "rb") as f:
                            st.download_button("⬇️", f.read(),
                                file_name=doc_name,
                                key=f"dl_doc_global_{row['booking']}_{doc_name}",
                                use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# LICENCES DPVCT
# ══════════════════════════════════════════════════════════════════════════════
elif page == "licences":
    st.markdown("""
    <div class="topbar">
      <div>
        <div class="topbar-title">Licences DPVCT</div>
        <div class="topbar-sub">Soldes réels & prévisionnels · PDF téléchargeables</div>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="main-wrap">', unsafe_allow_html=True)

    for _, row in clients.iterrows():
        pct_reel = max(0, min(100, row["solde_reel"]/row["poids_total"]*100)) if row["poids_total"] > 0 else 0
        pct_prev = max(0, min(100, row["solde_prev"]/row["poids_total"]*100)) if row["poids_total"] > 0 else 0

        if   row["solde_reel"] < 0:       badge = '<span style="background:#FFEBEE;color:#C62828;padding:4px 12px;border-radius:16px;font-size:11px;font-weight:700">❌ DÉPASSEMENT</span>'
        elif row["solde_reel"] < 19591.2: badge = '<span style="background:#FFEBEE;color:#C62828;padding:4px 12px;border-radius:16px;font-size:11px;font-weight:700">🔴 CRITIQUE</span>'
        elif row["solde_reel"] < 58773.6: badge = '<span style="background:#FFF8E1;color:#E65100;padding:4px 12px;border-radius:16px;font-size:11px;font-weight:700">⚠️ ATTENTION</span>'
        else:                              badge = '<span style="background:#E8F5E9;color:#2E7D32;padding:4px 12px;border-radius:16px;font-size:11px;font-weight:700">✅ OK</span>'

        pdf_path   = licence_pdf_path(row["licence"])
        pdf_exists = os.path.exists(pdf_path)

        st.markdown(f"""
        <div class="card">
          <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px;margin-bottom:18px">
            <div>
              <div style="font-size:16px;font-weight:800;color:#1A1A2E">{row['nom']}</div>
              <div style="font-size:12px;color:#9AA0AB;margin-top:3px">🔑 {row['licence']} &nbsp;·&nbsp; {row['pays']}</div>
            </div>
            {badge}
          </div>
          <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-bottom:16px">
            <div style="background:#F8F9FB;border-radius:10px;padding:14px">
              <div style="font-size:9px;color:#9AA0AB;text-transform:uppercase;letter-spacing:0.8px;font-weight:700;margin-bottom:4px">Poids total</div>
              <div style="font-size:20px;font-weight:800;color:#1A1A2E">{row['poids_total']:,.0f} <span style="font-size:12px;color:#9AA0AB">kgs</span></div>
            </div>
            <div style="background:#EEF2FF;border-radius:10px;padding:14px">
              <div style="font-size:9px;color:#3B5BDB;text-transform:uppercase;letter-spacing:0.8px;font-weight:700;margin-bottom:4px">Solde réel</div>
              <div style="font-size:20px;font-weight:800;color:#3B5BDB">{row['solde_reel']:,.0f} <span style="font-size:12px">kgs</span></div>
            </div>
            <div style="background:#FFF8E1;border-radius:10px;padding:14px">
              <div style="font-size:9px;color:#E65100;text-transform:uppercase;letter-spacing:0.8px;font-weight:700;margin-bottom:4px">Solde prévisionnel</div>
              <div style="font-size:20px;font-weight:800;color:#E65100">{row['solde_prev']:,.0f} <span style="font-size:12px">kgs</span></div>
            </div>
          </div>
          <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:16px">
            <div style="background:#EEF2FF;border-radius:10px;padding:12px;text-align:center">
              <div style="font-size:9px;color:#3B5BDB;font-weight:700;text-transform:uppercase;margin-bottom:4px">🇨🇷 CR · Réel</div>
              <div style="font-size:22px;font-weight:900;color:#3B5BDB">{row['cnt_reel_cr']:.1f}</div>
              <div style="font-size:9px;color:#9AA0AB">CNT · MOIN</div>
            </div>
            <div style="background:#FFF8E1;border-radius:10px;padding:12px;text-align:center">
              <div style="font-size:9px;color:#E65100;font-weight:700;text-transform:uppercase;margin-bottom:4px">🇨🇷 CR · Prév.</div>
              <div style="font-size:22px;font-weight:900;color:#E65100">{row['cnt_prev_cr']:.1f}</div>
              <div style="font-size:9px;color:#9AA0AB">CNT · MOIN</div>
            </div>
            <div style="background:#EEF2FF;border-radius:10px;padding:12px;text-align:center">
              <div style="font-size:9px;color:#3B5BDB;font-weight:700;text-transform:uppercase;margin-bottom:4px">🇨🇴 COL · Réel</div>
              <div style="font-size:22px;font-weight:900;color:#3B5BDB">{row['cnt_reel_col']:.1f}</div>
              <div style="font-size:9px;color:#9AA0AB">CNT · TURBO</div>
            </div>
            <div style="background:#FFF8E1;border-radius:10px;padding:12px;text-align:center">
              <div style="font-size:9px;color:#E65100;font-weight:700;text-transform:uppercase;margin-bottom:4px">🇨🇴 COL · Prév.</div>
              <div style="font-size:22px;font-weight:900;color:#E65100">{row['cnt_prev_col']:.1f}</div>
              <div style="font-size:9px;color:#9AA0AB">CNT · TURBO</div>
            </div>
          </div>
          <div style="margin-bottom:8px">
            <div style="display:flex;justify-content:space-between;margin-bottom:4px">
              <span style="font-size:11px;color:#9AA0AB">Solde réel</span>
              <span style="font-size:11px;color:#3B5BDB;font-weight:700">{pct_reel:.0f}%</span>
            </div>
            <div style="background:#E8EAED;border-radius:6px;height:5px"><div style="background:#3B5BDB;width:{pct_reel}%;height:100%;border-radius:6px"></div></div>
          </div>
          <div>
            <div style="display:flex;justify-content:space-between;margin-bottom:4px">
              <span style="font-size:11px;color:#9AA0AB">Solde prévisionnel</span>
              <span style="font-size:11px;color:#E65100;font-weight:700">{pct_prev:.0f}%</span>
            </div>
            <div style="background:#E8EAED;border-radius:6px;height:5px"><div style="background:#E65100;width:{pct_prev}%;height:100%;border-radius:6px"></div></div>
          </div>
        </div>""", unsafe_allow_html=True)

        if pdf_exists:
            with open(pdf_path, "rb") as f:
                pdf_data = f.read()
            col_pdf, _ = st.columns([2,5])
            with col_pdf:
                st.download_button(f"📄 Télécharger {row['licence']}", pdf_data,
                    file_name=licence_to_filename(row["licence"]),
                    mime="application/pdf", key=f"pdf_{row['licence']}",
                    use_container_width=True)
        else:
            st.caption(f"⚠️ PDF non trouvé → uploade `{pdf_path}` sur GitHub")
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PLANNING CLIENT
# ══════════════════════════════════════════════════════════════════════════════
elif page == "planning":
    st.markdown("""
    <div class="topbar">
      <div>
        <div class="topbar-title">Planning client</div>
        <div class="topbar-sub">Historique et commandes par client</div>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="main-wrap">', unsafe_allow_html=True)

    client_sel = st.selectbox("Client", sorted(commandes["client"].dropna().unique().tolist()),
                               label_visibility="collapsed")
    if client_sel:
        df_c = commandes[commandes["client"]==client_sel].copy()
        lic_c = clients[clients["nom"]==client_sel]

        st.markdown(f"""
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:24px">
          <div class="kpi-box"><div class="lbl">Total CNT</div><div class="val" style="color:#3B5BDB">{int(df_c["nb_cnt"].sum())}</div></div>
          <div class="kpi-box"><div class="lbl">Total kgs</div><div class="val" style="color:#6D28D9;font-size:1.4rem">{df_c["total_kgs"].sum():,.0f}</div></div>
          <div class="kpi-box"><div class="lbl">⏳ En cours</div><div class="val" style="color:#E65100">{len(df_c[df_c["statut"].str.contains("À GÉNÉRER",na=False)])}</div></div>
          <div class="kpi-box"><div class="lbl">✅ Confirmées</div><div class="val" style="color:#2E7D32">{len(df_c[df_c["statut"].str.contains("GÉNÉRÉ",na=False)])}</div></div>
        </div>""", unsafe_allow_html=True)

        for _, row in df_c.sort_values("semaine",ascending=False).iterrows():
            sc = "#2E7D32" if "GÉNÉRÉ" in str(row["statut"]) else "#E65100"
            sb = "#E8F5E9" if "GÉNÉRÉ" in str(row["statut"]) else "#FFF3E0"
            n_docs = len(list_docs(row["booking"]))
            st.markdown(f"""
            <div class="cmd-row">
              <div><div style="font-size:13px;font-weight:700;color:#1A1A2E">{row['booking']}</div>
              <div style="font-size:11px;color:#9AA0AB">{row['semaine']} · {row['licence']}</div></div>
              <div style="text-align:center"><div style="font-size:9px;color:#9AA0AB">POL</div><div style="font-weight:700;color:#1A1A2E">{row['pol']}</div></div>
              <div style="text-align:center"><div style="font-size:9px;color:#9AA0AB">CNT</div><div style="font-weight:800;color:#3B5BDB;font-size:18px">{row['nb_cnt']}</div></div>
              <div style="text-align:center"><div style="font-size:9px;color:#9AA0AB">Départ</div><div style="font-weight:600;color:#374151;font-size:11px">{row['depart']}</div></div>
              <div style="text-align:center"><div style="font-size:9px;color:#9AA0AB">ETA</div><div style="font-weight:600;color:#374151;font-size:11px">{row['eta']}</div></div>
              <div><span style="background:#E3F2FD;color:#1565C0;padding:2px 8px;border-radius:12px;font-size:10px;font-weight:700">📁 {n_docs}</span></div>
              <div style="background:{sb};color:{sc};padding:5px 12px;border-radius:14px;font-size:11px;font-weight:700">{row['statut']}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# NOUVELLE COMMANDE (admin uniquement)
# ══════════════════════════════════════════════════════════════════════════════
elif page == "new_cmd":
    if st.session_state.role != "admin":
        st.error("⛔ Accès réservé aux administrateurs")
        st.stop()

    st.markdown("""
    <div class="topbar">
      <div>
        <div class="topbar-title">Nouvelle commande</div>
        <div class="topbar-sub">Calculs de solde en temps réel avant validation</div>
      </div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="main-wrap">', unsafe_allow_html=True)

    with st.form("form_commande", clear_on_submit=True):
        f1, f2 = st.columns(2)
        with f1:
            sem            = st.text_input("Semaine *", placeholder="ex: S-26")
            client_sel     = st.selectbox("Client *", sorted(clients["nom"].unique().tolist()))
            booking        = st.text_input("Référence Booking *", placeholder="ex: LHV4005547")
            licences_dispo = clients[clients["nom"]==client_sel]["licence"].tolist()
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
        lic_row       = clients[(clients["nom"]==client_sel)&(clients["licence"]==licence_sel)]
        solde_avant   = float(lic_row["solde_reel"].values[0]) if len(lic_row) > 0 else 0
        solde_apres   = round(solde_avant - total_kgs, 2)
        cnt_apres_cr  = round(solde_apres / KGS_PER_CNT["MOIN(COSTA RICA)"], 2)
        cnt_apres_col = round(solde_apres / KGS_PER_CNT["TURBO(COLOMBIA)"], 2)

        st.markdown("---")
        p1,p2,p3,p4,p5,p6 = st.columns(6)
        p1.metric("Cartons/CNT",     f"{crtns_cnt:,}")
        p2.metric("Total cartons",   f"{total_crtns:,}")
        p3.metric("Total kgs",       f"{total_kgs:,.0f}")
        p4.metric("Solde après",     f"{solde_apres:,.0f} kgs", delta=f"{-total_kgs:,.0f}", delta_color="inverse")
        p5.metric("CNT restants 🇨🇷", f"{cnt_apres_cr:.1f}")
        p6.metric("CNT restants 🇨🇴", f"{cnt_apres_col:.1f}")

        if   solde_apres < 0:       st.markdown('<div class="alert-red">⚠️ Solde insuffisant — commande bloquée</div>', unsafe_allow_html=True)
        elif solde_apres < 19591.2: st.markdown('<div class="alert-warn">🔴 Solde critique après cette commande</div>', unsafe_allow_html=True)
        else:                        st.markdown('<div class="alert-ok">✅ Solde suffisant</div>', unsafe_allow_html=True)

        submitted = st.form_submit_button("✅ Enregistrer la commande",
                        use_container_width=True, type="primary", disabled=(solde_apres < 0))

        if submitted:
            st.session_state.new_commandes.append({
                "num":"","semaine":sem,"client":client_sel,
                "booking":booking,"licence":licence_sel,
                "navire":navire,"voyage":voyage,"pol":pol_sel,
                "depart":depart.strftime("%d/%m/%Y"),
                "eta":eta.strftime("%d/%m/%Y"),
                "nb_cnt":nb_cnt,"produit":produit,"statut":"⏳ À GÉNÉRER"
            })
            st.cache_data.clear()
            st.success(f"✅ Commande {booking} enregistrée !")
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
