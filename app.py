import streamlit as st
import pandas as pd
from datetime import datetime, date
import plotly.express as px
import base64
import os

# ── CONFIG ────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EDEN FOOD",
    page_icon="🍌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS — Apple / CMA CGM ─────────────────────────────────────────────────────
st.markdown("""
<style>
header[data-testid="stHeader"],#MainMenu,.stAppDeployButton,footer{display:none!important}
.stApp{background:#F5F5F7;font-family:-apple-system,BlinkMacSystemFont,'SF Pro Display','Helvetica Neue',Arial,sans-serif}
.block-container{padding:2rem 2.5rem;max-width:1400px}

/* SIDEBAR */
section[data-testid="stSidebar"]{background:#1D1D1F!important;border-right:none!important}
section[data-testid="stSidebar"] p,section[data-testid="stSidebar"] span,section[data-testid="stSidebar"] label{color:#F5F5F7!important}
section[data-testid="stSidebar"] .stButton>button{
  background:transparent!important;border:none!important;color:#EBEBF5!important;
  text-align:left!important;width:100%!important;padding:10px 16px!important;
  border-radius:10px!important;font-size:14px!important;font-weight:500!important;
  transition:background 0.15s!important;margin-bottom:2px!important}
section[data-testid="stSidebar"] .stButton>button:hover{background:rgba(255,255,255,0.10)!important}
section[data-testid="stSidebar"] .stButton>button:focus{background:rgba(255,255,255,0.14)!important;box-shadow:none!important}

/* KPI */
.kpi-card{background:#fff;border-radius:18px;padding:22px 20px;box-shadow:0 1px 4px rgba(0,0,0,0.06),0 4px 16px rgba(0,0,0,0.04)}
.kpi-num{font-size:2.2rem;font-weight:700;letter-spacing:-1px;color:#1D1D1F;margin:8px 0 4px;line-height:1}
.kpi-lbl{font-size:11px;color:#6E6E73;text-transform:uppercase;letter-spacing:0.8px;font-weight:600}
.kpi-sub{font-size:12px;color:#8E8E93;margin-top:4px}

/* CARD */
.card{background:#fff;border-radius:18px;padding:22px 24px;box-shadow:0 1px 4px rgba(0,0,0,0.06),0 4px 16px rgba(0,0,0,0.04);margin-bottom:14px}

/* TYPO */
.page-title{font-size:28px;font-weight:700;color:#1D1D1F;letter-spacing:-0.5px;margin:0 0 4px}
.page-sub{font-size:14px;color:#6E6E73;margin:0 0 28px}
.sec-hdr{font-size:11px;font-weight:700;color:#8E8E93;text-transform:uppercase;letter-spacing:1.2px;margin:24px 0 14px;padding-bottom:8px;border-bottom:1px solid #E5E5EA}

/* BADGES */
.badge-gen{background:#E8F5E9;color:#1B5E20;padding:3px 10px;border-radius:12px;font-size:11px;font-weight:700}
.badge-todo{background:#FFF3E0;color:#E65100;padding:3px 10px;border-radius:12px;font-size:11px;font-weight:700}
.badge-ok{background:#E3F2FD;color:#0D47A1;padding:3px 10px;border-radius:12px;font-size:11px;font-weight:700}

/* WEEK */
.week-badge{background:#0071E3;color:#fff;padding:4px 14px;border-radius:20px;font-size:12px;font-weight:700;display:inline-block}

/* ALERTS */
.alert-red{background:#FFF2F2;border-left:3px solid #FF3B30;padding:12px 16px;border-radius:10px;color:#C62828;font-size:13px;margin:8px 0;font-weight:600}
.alert-ok{background:#F1FAF4;border-left:3px solid #34C759;padding:12px 16px;border-radius:10px;color:#1B5E20;font-size:13px;margin:8px 0;font-weight:600}
.alert-warn{background:#FFFBF0;border-left:3px solid #FF9F0A;padding:12px 16px;border-radius:10px;color:#7A4F00;font-size:13px;margin:8px 0;font-weight:600}

/* FORM */
div[data-testid="stForm"]{background:#fff!important;border-radius:18px!important;padding:28px!important;box-shadow:0 1px 4px rgba(0,0,0,0.06)!important;border:none!important}
hr{border:none!important;border-top:1px solid #E5E5EA!important;margin:16px 0!important}
.stDataFrame{border-radius:14px;overflow:hidden}
</style>
""", unsafe_allow_html=True)

# ── USERS ─────────────────────────────────────────────────────────────────────
USERS = {
    "yann":  {"password": "EdenFood2026!", "role": "admin"},
    "eden":  {"password": "Eden@Logistik",  "role": "user"},
    "srg":   {"password": "SRG@Trading1",   "role": "user"},
}

# ── SESSION STATE ─────────────────────────────────────────────────────────────
defaults = {"authenticated":False,"username":"","role":"","page":"dashboard","new_commandes":[]}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── LOGIN ─────────────────────────────────────────────────────────────────────
def login_page():
    try:
        b64 = base64.b64encode(open("logo_eden_food.jpg","rb").read()).decode()
        logo_html = f'<img src="data:image/jpeg;base64,{b64}" style="height:60px;margin-bottom:24px">'
    except:
        logo_html = '<div style="font-size:42px;margin-bottom:20px">🍌</div>'

    st.markdown(f"""
    <div style="display:flex;align-items:center;justify-content:center;min-height:78vh">
      <div style="background:#fff;border-radius:24px;padding:52px 44px;
          box-shadow:0 8px 40px rgba(0,0,0,0.10);max-width:400px;width:100%;text-align:center">
        {logo_html}
        <p style="font-size:22px;font-weight:700;color:#1D1D1F;margin:0 0 6px">Logistics Platform</p>
        <p style="font-size:14px;color:#6E6E73;margin:0 0 32px">Accès sécurisé — identifiez-vous</p>
      </div>
    </div>""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        with st.form("login"):
            u = st.text_input("Identifiant", placeholder="ex: yann")
            p = st.text_input("Mot de passe", type="password")
            if st.form_submit_button("→ Connexion", use_container_width=True, type="primary"):
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
POIDS_UNIT = 18.14
CRTNS = {"TURBO(COLOMBIA)": 1080, "MOIN(COSTA RICA)": 1200}

def licence_to_pdf(lic_num):
    clean = str(lic_num).replace(" ","_").replace("/","_")
    return f"licences/{clean}.pdf"

# ── DATA ──────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=60)
def load_clients():
    df = pd.read_excel("eden_food.xlsx", sheet_name="📋 BASE CLIENTS",
                       usecols=list(range(11)), header=3)
    df.columns = ["num","nom","adresse1","adresse2","ville","pays","licence",
                  "poids_total","solde_init","contact","notes"]
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

# Solde réel = confirmées uniquement (✅ GÉNÉRÉ)
def get_solde_reel(nom, lic, poids):
    mask = (commandes["client"]==nom) & (commandes["licence"]==lic) & \
           (~commandes["statut"].str.contains("À GÉNÉRER", na=False))
    return round(poids - commandes.loc[mask,"total_kgs"].sum(), 2)

# Solde prévisionnel = toutes les commandes (réel + à générer)
def get_solde_prev(nom, lic, poids):
    mask = (commandes["client"]==nom) & (commandes["licence"]==lic)
    return round(poids - commandes.loc[mask,"total_kgs"].sum(), 2)

clients["solde_reel"] = clients.apply(lambda r: get_solde_reel(r["nom"],r["licence"],r["poids_total"]), axis=1)
clients["solde_prev"] = clients.apply(lambda r: get_solde_prev(r["nom"],r["licence"],r["poids_total"]), axis=1)

current_week_num = datetime.now().isocalendar()[1]
current_week_str = f"S-{current_week_num}"
commandes_semaine = commandes[commandes["semaine"] == current_week_str]

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    try:
        b64 = base64.b64encode(open("logo_eden_food.jpg","rb").read()).decode()
        st.markdown(f'<div style="padding:24px 16px 16px"><img src="data:image/jpeg;base64,{b64}" style="height:38px"></div>', unsafe_allow_html=True)
    except:
        st.markdown('<div style="padding:24px 16px 16px;color:#fff;font-size:18px;font-weight:800;letter-spacing:1px">🍌 EDEN FOOD</div>', unsafe_allow_html=True)

    st.markdown('<div style="height:1px;background:rgba(255,255,255,0.1);margin:0 16px 12px"></div>', unsafe_allow_html=True)

    NAV = [
        ("dashboard",  "🏠  Dashboard"),
        ("semaine",    f"📅  Semaine {current_week_str}"),
        ("licences",   "📋  Licences DPVCT"),
        ("commandes",  "🚢  Commandes"),
        ("planning",   "👤  Planning client"),
        ("new_cmd",    "➕  Nouvelle commande"),
    ]
    for page_id, label in NAV:
        if st.button(label, key=f"nav_{page_id}", use_container_width=True):
            st.session_state.page = page_id
            st.rerun()

    st.markdown('<div style="height:1px;background:rgba(255,255,255,0.1);margin:12px 16px 8px"></div>', unsafe_allow_html=True)
    st.markdown(f'<div style="padding:6px 16px;color:rgba(255,255,255,0.45);font-size:11px;text-transform:uppercase;letter-spacing:0.5px">👤 {st.session_state.username} · {st.session_state.role}</div>', unsafe_allow_html=True)
    if st.button("🚪  Déconnexion", use_container_width=True, key="logout"):
        st.session_state.update(authenticated=False, username="")
        st.rerun()

page = st.session_state.page

# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
if page == "dashboard":
    st.markdown('<p class="page-title">Tableau de bord</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="page-sub">{datetime.now().strftime("%A %d %B %Y")} &nbsp;·&nbsp; Semaine <span class="week-badge">{current_week_str}</span></p>', unsafe_allow_html=True)

    todo   = commandes[commandes["statut"].str.contains("À GÉNÉRER", na=False)]
    done   = commandes[~commandes["statut"].str.contains("À GÉNÉRER", na=False) & commandes["statut"].str.contains("GÉNÉRÉ", na=False)]
    alerte = clients[clients["solde_reel"] < 19591.2]
    depass = clients[clients["solde_reel"] < 0]

    k1,k2,k3,k4,k5,k6 = st.columns(6)
    for col, val, lbl, sub, color in [
        (k1, len(commandes),             "Expéditions",    "total enregistrées",  "#0071E3"),
        (k2, len(todo),                  "⏳ À générer",   "en attente",           "#FF9F0A"),
        (k3, len(done),                  "✅ Confirmées",  "générées",             "#34C759"),
        (k4, int(todo["nb_cnt"].sum()),  "CNT planifiés",  "conteneurs",           "#5856D6"),
        (k5, len(alerte),                "🔴 Alertes",     "licences critiques",   "#FF3B30"),
        (k6, len(commandes_semaine),     current_week_str, "commandes en cours",   "#1D1D1F"),
    ]:
        col.markdown(f"""
        <div class="kpi-card">
          <div class="kpi-lbl">{lbl}</div>
          <div class="kpi-num" style="color:{color}">{val}</div>
          <div class="kpi-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("")
    c1, c2 = st.columns([3, 2])

    with c1:
        st.markdown('<div class="sec-hdr">Dernières expéditions</div>', unsafe_allow_html=True)
        recent = commandes.tail(8)[["semaine","client","booking","pol","nb_cnt","depart","eta","statut"]]
        st.dataframe(recent, use_container_width=True, hide_index=True, height=310,
            column_config={
                "semaine": st.column_config.Text
