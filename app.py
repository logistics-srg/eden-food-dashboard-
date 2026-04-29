import streamlit as st
import pandas as pd
from datetime import datetime, date
import plotly.express as px
import base64
import os

st.set_page_config(page_title="EDEN FOOD", page_icon="🍌", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
header[data-testid="stHeader"],#MainMenu,.stAppDeployButton,footer{display:none!important}
.stApp{background:#F5F5F7;font-family:-apple-system,BlinkMacSystemFont,'SF Pro Display','Helvetica Neue',Arial,sans-serif}
.block-container{padding:2rem 2.5rem;max-width:1400px}
section[data-testid="stSidebar"]{background:#1D1D1F!important;border-right:none!important}
section[data-testid="stSidebar"] p,section[data-testid="stSidebar"] span,section[data-testid="stSidebar"] label{color:#F5F5F7!important}
section[data-testid="stSidebar"] .stButton>button{background:transparent!important;border:none!important;color:#EBEBF5!important;text-align:left!important;width:100%!important;padding:10px 16px!important;border-radius:10px!important;font-size:14px!important;font-weight:500!important;transition:background 0.15s!important;margin-bottom:2px!important}
section[data-testid="stSidebar"] .stButton>button:hover{background:rgba(255,255,255,0.10)!important}
.kpi-card{background:#fff;border-radius:18px;padding:22px 20px;box-shadow:0 1px 4px rgba(0,0,0,0.06),0 4px 16px rgba(0,0,0,0.04)}
.kpi-num{font-size:2.2rem;font-weight:700;letter-spacing:-1px;color:#1D1D1F;margin:8px 0 4px;line-height:1}
.kpi-lbl{font-size:11px;color:#6E6E73;text-transform:uppercase;letter-spacing:0.8px;font-weight:600}
.kpi-sub{font-size:12px;color:#8E8E93;margin-top:4px}
.card{background:#fff;border-radius:18px;padding:22px 24px;box-shadow:0 1px 4px rgba(0,0,0,0.06),0 4px 16px rgba(0,0,0,0.04);margin-bottom:14px}
.page-title{font-size:28px;font-weight:700;color:#1D1D1F;letter-spacing:-0.5px;margin:0 0 4px}
.page-sub{font-size:14px;color:#6E6E73;margin:0 0 28px}
.sec-hdr{font-size:11px;font-weight:700;color:#8E8E93;text-transform:uppercase;letter-spacing:1.2px;margin:24px 0 14px;padding-bottom:8px;border-bottom:1px solid #E5E5EA}
.week-badge{background:#0071E3;color:#fff;padding:4px 14px;border-radius:20px;font-size:12px;font-weight:700;display:inline-block}
.alert-red{background:#FFF2F2;border-left:3px solid #FF3B30;padding:12px 16px;border-radius:10px;color:#C62828;font-size:13px;margin:8px 0;font-weight:600}
.alert-ok{background:#F1FAF4;border-left:3px solid #34C759;padding:12px 16px;border-radius:10px;color:#1B5E20;font-size:13px;margin:8px 0;font-weight:600}
.alert-warn{background:#FFFBF0;border-left:3px solid #FF9F0A;padding:12px 16px;border-radius:10px;color:#7A4F00;font-size:13px;margin:8px 0;font-weight:600}
div[data-testid="stForm"]{background:#fff!important;border-radius:18px!important;padding:28px!important;box-shadow:0 1px 4px rgba(0,0,0,0.06)!important;border:none!important}
hr{border:none!important;border-top:1px solid #E5E5EA!important;margin:16px 0!important}
</style>
""", unsafe_allow_html=True)

# ── USERS ─────────────────────────────────────────────────────────────────────
USERS = {
    "yann": {"password": "EdenFood2026!", "role": "admin"},
    "eden": {"password": "Eden@Logistik", "role": "user"},
    "srg":  {"password": "SRG@Trading1",  "role": "user"},
}

# ── SESSION STATE ─────────────────────────────────────────────────────────────
for k, v in {"authenticated": False, "username": "", "role": "", "page": "dashboard", "new_commandes": []}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── LOGIN ─────────────────────────────────────────────────────────────────────
def login_page():
    try:
        b64 = base64.b64encode(open("logo_eden_food.jpg", "rb").read()).decode()
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
    c1, c2, c3 = st.columns([1, 2, 1])
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
    clean = str(lic_num).replace(" ", "_").replace("/", "_")
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

def get_solde_reel(nom, lic, poids):
    mask = (commandes["client"] == nom) & (commandes["licence"] == lic) & \
           (~commandes["statut"].str.contains("À GÉNÉRER", na=False))
    return round(poids - commandes.loc[mask, "total_kgs"].sum(), 2)

def get_solde_prev(nom, lic, poids):
    mask = (commandes["client"] == nom) & (commandes["licence"] == lic)
    return round(poids - commandes.loc[mask, "total_kgs"].sum(), 2)

clients["solde_reel"] = clients.apply(lambda r: get_solde_reel(r["nom"], r["licence"], r["poids_total"]), axis=1)
clients["solde_prev"] = clients.apply(lambda r: get_solde_prev(r["nom"], r["licence"], r["poids_total"]), axis=1)

current_week_num = datetime.now().isocalendar()[1]
current_week_str = f"S-{current_week_num}"
commandes_semaine = commandes[commandes["semaine"] == current_week_str]

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    try:
        b64 = base64.b64encode(open("logo_eden_food.jpg", "rb").read()).decode()
        st.markdown(f'<div style="padding:24px 16px 16px"><img src="data:image/jpeg;base64,{b64}" style="height:38px"></div>', unsafe_allow_html=True)
    except:
        st.markdown('<div style="padding:24px 16px 16px;color:#fff;font-size:18px;font-weight:800">🍌 EDEN FOOD</div>', unsafe_allow_html=True)

    st.markdown('<div style="height:1px;background:rgba(255,255,255,0.1);margin:0 16px 12px"></div>', unsafe_allow_html=True)

    NAV = [
        ("dashboard", "🏠  Dashboard"),
        ("semaine",   f"📅  Semaine {current_week_str}"),
        ("licences",  "📋  Licences DPVCT"),
        ("commandes", "🚢  Commandes"),
        ("planning",  "👤  Planning client"),
        ("new_cmd",   "➕  Nouvelle commande"),
    ]
    for pid, label in NAV:
        if st.button(label, key=f"nav_{pid}", use_container_width=True):
            st.session_state.page = pid
            st.rerun()

    st.markdown('<div style="height:1px;background:rgba(255,255,255,0.1);margin:12px 16px 8px"></div>', unsafe_allow_html=True)
    st.markdown(f'<div style="padding:6px 16px;color:rgba(255,255,255,0.45);font-size:11px">👤 {st.session_state.username} · {st.session_state.role}</div>', unsafe_allow_html=True)
    if st.button("🚪  Déconnexion", use_container_width=True, key="logout"):
        st.session_state.update(authenticated=False, username="")
        st.rerun()

page = st.session_state.page

# ══════════════════════════════════════════════════════════════════════════════
# PAGE : DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
if page == "dashboard":
    st.markdown('<p class="page-title">Tableau de bord</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="page-sub">{datetime.now().strftime("%d %B %Y")} &nbsp;·&nbsp; Semaine en cours : <span class="week-badge">{current_week_str}</span></p>', unsafe_allow_html=True)

    todo   = commandes[commandes["statut"].str.contains("À GÉNÉRER", na=False)]
    done   = commandes[commandes["statut"].str.contains("GÉNÉRÉ", na=False)]
    alerte = clients[clients["solde_reel"] < 19591.2]
    depass = clients[clients["solde_reel"] < 0]

    k1, k2, k3, k4, k5, k6 = st.columns(6)
    for col, val, lbl, sub, color in [
        (k1, len(commandes),            "Expéditions",   "total enregistrées", "#0071E3"),
        (k2, len(todo),                 "⏳ À générer",  "en attente",          "#FF9F0A"),
        (k3, len(done),                 "✅ Confirmées", "générées",            "#34C759"),
        (k4, int(todo["nb_cnt"].sum()), "CNT planifiés", "conteneurs",          "#5856D6"),
        (k5, len(alerte),               "🔴 Alertes",   "licences critiques",  "#FF3B30"),
        (k6, len(commandes_semaine),    current_week_str,"cette semaine",       "#1D1D1F"),
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
        recent = commandes.tail(8)[["semaine","client","booking","pol","nb_cnt","depart","statut"]].copy()
        st.dataframe(recent, use_container_width=True, hide_index=True, height=300,
            column_config={
                "semaine":  st.column_config.TextColumn("Sem."),
                "client":   st.column_config.TextColumn("Client"),
                "booking":  st.column_config.TextColumn("Booking"),
                "pol":      st.column_config.TextColumn("POL"),
                "nb_cnt":   st.column_config.NumberColumn("CNT", format="%d"),
                "depart":   st.column_config.TextColumn("Départ"),
                "statut":   st.column_config.TextColumn("Statut"),
            })

    with c2:
        st.markdown('<div class="sec-hdr">Répartition POL</div>', unsafe_allow_html=True)
        if not commandes.empty:
            df_pol = commandes.groupby("pol")["nb_cnt"].sum().reset_index()
            fig = px.pie(df_pol, values="nb_cnt", names="pol", hole=0.65,
                color_discrete_sequence=["#0071E3","#FF9F0A"])
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=20,b=20,l=0,r=0),
                legend=dict(orientation="h", y=-0.15))
            fig.update_traces(textinfo="percent+label")
            st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="sec-hdr">Volume hebdomadaire (CNT)</div>', unsafe_allow_html=True)
    if not commandes.empty:
        df_sem = commandes.groupby("semaine")["nb_cnt"].sum().reset_index()
        fig2 = px.bar(df_sem, x="semaine", y="nb_cnt",
            color_discrete_sequence=["#0071E3"],
            labels={"semaine":"Semaine","nb_cnt":"Conteneurs"})
        fig2.update_layout(plot_bgcolor="#fff", paper_bgcolor="#fff",
            margin=dict(t=10,b=20,l=20,r=20), xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor="#F0F0F0"))
        fig2.update_traces(marker_cornerradius=6)
        st.plotly_chart(fig2, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE : SEMAINE EN COURS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "semaine":
    st.markdown(f'<p class="page-title">Semaine en cours — {current_week_str}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="page-sub">Toutes les commandes de la semaine {current_week_num} / {datetime.now().year}</p>', unsafe_allow_html=True)

    if commandes_semaine.empty:
        st.info(f"Aucune commande enregistrée pour {current_week_str}. Vérifie le format de la colonne Semaine dans ton Excel (ex: S-18).")
    else:
        todo_s = commandes_semaine[commandes_semaine["statut"].str.contains("À GÉNÉRER", na=False)]
        done_s = commandes_semaine[commandes_semaine["statut"].str.contains("GÉNÉRÉ", na=False)]

        a, b, c, d = st.columns(4)
        a.markdown(f'<div class="kpi-card"><div class="kpi-lbl">Total commandes</div><div class="kpi-num" style="color:#0071E3">{len(commandes_semaine)}</div></div>', unsafe_allow_html=True)
        b.markdown(f'<div class="kpi-card"><div class="kpi-lbl">⏳ À générer</div><div class="kpi-num" style="color:#FF9F0A">{len(todo_s)}</div></div>', unsafe_allow_html=True)
        c.markdown(f'<div class="kpi-card"><div class="kpi-lbl">✅ Confirmées</div><div class="kpi-num" style="color:#34C759">{len(done_s)}</div></div>', unsafe_allow_html=True)
        d.markdown(f'<div class="kpi-card"><div class="kpi-lbl">CNT total</div><div class="kpi-num" style="color:#5856D6">{int(commandes_semaine["nb_cnt"].sum())}</div></div>', unsafe_allow_html=True)

        st.markdown("")
        st.markdown('<div class="sec-hdr">Détail des commandes</div>', unsafe_allow_html=True)

        for _, row in commandes_semaine.iterrows():
            statut_color = "#34C759" if "GÉNÉRÉ" in str(row["statut"]) else "#FF9F0A"
            statut_bg    = "#F1FAF4" if "GÉNÉRÉ" in str(row["statut"]) else "#FFFBF0"
            st.markdown(f"""
            <div class="card" style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px">
              <div>
                <div style="font-size:15px;font-weight:700;color:#1D1D1F">{row['client']}</div>
                <div style="font-size:12px;color:#6E6E73;margin-top:2px">Booking : <b>{row['booking']}</b> &nbsp;·&nbsp; Licence : {row['licence']}</div>
              </div>
              <div style="text-align:center">
                <div style="font-size:11px;color:#8E8E93">POL</div>
                <div style="font-weight:700;color:#1D1D1F">{row['pol']}</div>
              </div>
              <div style="text-align:center">
                <div style="font-size:11px;color:#8E8E93">CNT</div>
                <div style="font-weight:700;color:#1D1D1F">{row['nb_cnt']}</div>
              </div>
              <div style="text-align:center">
                <div style="font-size:11px;color:#8E8E93">Départ</div>
                <div style="font-weight:700;color:#1D1D1F">{row['depart']}</div>
              </div>
              <div style="text-align:center">
                <div style="font-size:11px;color:#8E8E93">ETA</div>
                <div style="font-weight:700;color:#1D1D1F">{row['eta']}</div>
              </div>
              <div style="background:{statut_bg};color:{statut_color};padding:6px 16px;border-radius:20px;font-size:12px;font-weight:700">
                {row['statut']}
              </div>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE : LICENCES DPVCT
# ══════════════════════════════════════════════════════════════════════════════
elif page == "licences":
    st.markdown('<p class="page-title">Licences DPVCT</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Soldes réels et prévisionnels par licence · Cliquez sur le PDF pour ouvrir la licence</p>', unsafe_allow_html=True)

    for _, row in clients.iterrows():
        pct_reel = max(0, min(100, row["solde_reel"] / row["poids_total"] * 100)) if row["poids_total"] > 0 else 0
        pct_prev = max(0, min(100, row["solde_prev"] / row["poids_total"] * 100)) if row["poids_total"] > 0 else 0

        if row["solde_reel"] < 0:
            status_html = '<span style="background:#FF3B30;color:#fff;padding:4px 12px;border-radius:12px;font-size:11px;font-weight:700">❌ DÉPASSEMENT</span>'
        elif row["solde_reel"] < 19591.2:
            status_html = '<span style="background:#FF9F0A;color:#fff;padding:4px 12px;border-radius:12px;font-size:11px;font-weight:700">🔴 CRITIQUE</span>'
        elif row["solde_reel"] < 58773.6:
            status_html = '<span style="background:#FF9F0A22;color:#7A4F00;padding:4px 12px;border-radius:12px;font-size:11px;font-weight:700">⚠️ ATTENTION</span>'
        else:
            status_html = '<span style="background:#34C75922;color:#1B5E20;padding:4px 12px;border-radius:12px;font-size:11px;font-weight:700">✅ OK</span>'

        pdf_path = licence_to_pdf(row["licence"])
        pdf_exists = os.path.exists(pdf_path)

        with st.container():
            st.markdown(f"""
            <div class="card">
              <div style="display:flex;align-items:flex-start;justify-content:space-between;flex-wrap:wrap;gap:12px;margin-bottom:14px">
                <div>
                  <div style="font-size:16px;font-weight:700;color:#1D1D1F">{row['nom']}</div>
                  <div style="font-size:12px;color:#6E6E73;margin-top:3px">🔑 {row['licence']} &nbsp;·&nbsp; {row['pays']}</div>
                </div>
                <div style="display:flex;align-items:center;gap:10px">
                  {status_html}
                </div>
              </div>
              <div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:16px;margin-bottom:16px">
                <div><div style="font-size:11px;color:#8E8E93;margin-bottom:2px">POIDS TOTAL</div>
                  <div style="font-size:16px;font-weight:700;color:#1D1D1F">{row['poids_total']:,.0f} kgs</div></div>
                <div><div style="font-size:11px;color:#8E8E93;margin-bottom:2px">SOLDE RÉEL</div>
                  <div style="font-size:16px;font-weight:700;color:#0071E3">{row['solde_reel']:,.0f} kgs</div></div>
                <div><div style="font-size:11px;color:#8E8E93;margin-bottom:2px">SOLDE PRÉVISIONNEL</div>
                  <div style="font-size:16px;font-weight:700;color:#FF9F0A">{row['solde_prev']:,.0f} kgs</div></div>
                <div><div style="font-size:11px;color:#8E8E93;margin-bottom:2px">UTILISÉ</div>
                  <div style="font-size:16px;font-weight:700;color:#1D1D1F">{100-pct_reel:.0f}%</div></div>
              </div>
              <div style="margin-bottom:6px">
                <div style="font-size:11px;color:#8E8E93;margin-bottom:4px">Solde réel</div>
                <div style="background:#E5E5EA;border-radius:6px;height:8px;overflow:hidden">
                  <div style="background:#0071E3;width:{pct_reel}%;height:100%;border-radius:6px"></div>
                </div>
              </div>
              <div>
                <div style="font-size:11px;color:#8E8E93;margin-bottom:4px">Solde prévisionnel (commandes en cours incluses)</div>
                <div style="background:#E5E5EA;border-radius:6px;height:8px;overflow:hidden">
                  <div style="background:#FF9F0A;width:{pct_prev}%;height:100%;border-radius:6px"></div>
                </div>
              </div>
            </div>""", unsafe_allow_html=True)

            if pdf_exists:
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        label=f"📄 Télécharger licence {row['licence']}",
                        data=f.read(),
                        file_name=f"{row['licence'].replace('/','-')}.pdf",
                        mime="application/pdf",
                        key=f"pdf_{row['licence']}"
                    )
            else:
                st.caption(f"📎 PDF non disponible — uploade `{pdf_path}` sur GitHub")

# ══════════════════════════════════════════════════════════════════════════════
# PAGE : COMMANDES
# ══════════════════════════════════════════════════════════════════════════════
elif page == "commandes":
    st.markdown('<p class="page-title">Commandes</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Toutes les expéditions enregistrées</p>', unsafe_allow_html=True)

    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        f_statut = st.multiselect("Statut", commandes["statut"].dropna().unique().tolist(),
            default=commandes["statut"].dropna().unique().tolist())
    with fc2:
        f_pol = st.multiselect("POL", commandes["pol"].dropna().unique().tolist(),
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

    st.caption(f"**{len(df_filt)} commandes** · {df_filt['nb_cnt'].sum()} CNT · {df_filt['total_kgs'].sum():,.0f} kgs")

    if st.session_state.new_commandes:
        csv = commandes[["num","semaine","client","booking","licence","navire","voyage",
            "pol","depart","eta","nb_cnt","produit","statut"]].to_csv(index=False).encode("utf-8")
        st.download_button("📥 Exporter CSV", csv,
            file_name=f"commandes_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv", use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE : PLANNING CLIENT
# ══════════════════════════════════════════════════════════════════════════════
elif page == "planning":
    st.markdown('<p class="page-title">Planning client</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Historique et commandes en cours par client</p>', unsafe_allow_html=True)

    client_sel = st.selectbox("Sélectionner un client", sorted(commandes["client"].dropna().unique().tolist()))

    if client_sel:
        df_client = commandes[commandes["client"] == client_sel].copy()
        lic_client = clients[clients["nom"] == client_sel]

        st.markdown(f'<div class="sec-hdr">{client_sel} — {len(df_client)} expédition(s)</div>', unsafe_allow_html=True)

        a, b, c, d = st.columns(4)
        a.markdown(f'<div class="kpi-card"><div class="kpi-lbl">Total CNT</div><div class="kpi-num" style="color:#0071E3">{int(df_client["nb_cnt"].sum())}</div></div>', unsafe_allow_html=True)
        b.markdown(f'<div class="kpi-card"><div class="kpi-lbl">Total kgs</div><div class="kpi-num" style="color:#5856D6">{df_client["total_kgs"].sum():,.0f}</div></div>', unsafe_allow_html=True)
        c.markdown(f'<div class="kpi-card"><div class="kpi-lbl">⏳ En cours</div><div class="kpi-num" style="color:#FF9F0A">{len(df_client[df_client["statut"].str.contains("À GÉNÉRER",na=False)])}</div></div>', unsafe_allow_html=True)
        d.markdown(f'<div class="kpi-card"><div class="kpi-lbl">✅ Confirmées</div><div class="kpi-num" style="color:#34C759">{len(df_client[df_client["statut"].str.contains("GÉNÉRÉ",na=False)])}</div></div>', unsafe_allow_html=True)

        st.markdown("")

        for _, row in df_client.iterrows():
            statut_color = "#34C759" if "GÉNÉRÉ" in str(row["statut"]) else "#FF9F0A"
            statut_bg    = "#F1FAF4" if "GÉNÉRÉ" in str(row["statut"]) else "#FFFBF0"
            st.markdown(f"""
            <div class="card" style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px">
              <div>
                <div style="font-size:14px;font-weight:700;color:#1D1D1F">{row['booking']}</div>
                <div style="font-size:12px;color:#6E6E73;margin-top:2px">{row['semaine']} &nbsp;·&nbsp; {row['licence']}</div>
              </div>
              <div style="text-align:center">
                <div style="font-size:11px;color:#8E8E93">Navire</div>
                <div style="font-weight:600;font-size:13px;color:#1D1D1F">{row['navire']}</div>
              </div>
              <div style="text-align:center">
                <div style="font-size:11px;color:#8E8E93">POL</div>
                <div style="font-weight:700;color:#1D1D1F">{row['pol']}</div>
              </div>
              <div style="text-align:center">
                <div style="font-size:11px;color:#8E8E93">CNT</div>
                <div style="font-weight:700;color:#0071E3">{row['nb_cnt']}</div>
              </div>
              <div style="text-align:center">
                <div style="font-size:11px;color:#8E8E93">Départ</div>
                <div style="font-weight:600;color:#1D1D1F">{row['depart']}</div>
              </div>
              <div style="text-align:center">
                <div style="font-size:11px;color:#8E8E93">ETA</div>
                <div style="font-weight:600;color:#1D1D1F">{row['eta']}</div>
              </div>
              <div style="background:{statut_bg};color:{statut_color};padding:6px 16px;border-radius:20px;font-size:12px;font-weight:700">
                {row['statut']}
              </div>
            </div>""", unsafe_allow_html=True)

        if not lic_client.empty:
            st.markdown('<div class="sec-hdr">Licences associées</div>', unsafe_allow_html=True)
            for _, lr in lic_client.iterrows():
                pct = max(0, min(100, lr["solde_reel"] / lr["poids_total"] * 100)) if lr["poids_total"] > 0 else 0
                st.markdown(f"""
                <div class="card">
                  <div style="display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px;margin-bottom:12px">
                    <div style="font-weight:700;color:#1D1D1F">🔑 {lr['licence']}</div>
                    <div style="font-size:13px;color:#6E6E73">Solde réel : <b style="color:#0071E3">{lr['solde_reel']:,.0f} kgs</b> &nbsp;|&nbsp; Prévisionnel : <b style="color:#FF9F0A">{lr['solde_prev']:,.0f} kgs</b></div>
                  </div>
                  <div style="background:#E5E5EA;border-radius:6px;height:8px;overflow:hidden">
                    <div style="background:#0071E3;width:{pct}%;height:100%;border-radius:6px"></div>
                  </div>
                </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE : NOUVELLE COMMANDE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "new_cmd":
    st.markdown('<p class="page-title">Nouvelle commande</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Les champs calculés se mettent à jour automatiquement avant validation</p>', unsafe_allow_html=True)

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
        with f4: eta     = st.date_input("ETA *", value=date.today())
        with f5: produit = st.selectbox("Produit *", ["BANANE","ANANAS","MANGUE","AUTRE"])

        crtns_cnt   = CRTNS[pol_sel]
        total_crtns = nb_cnt * crtns_cnt
        total_kgs   = round(total_crtns * POIDS_UNIT, 2)
        lic_row     = clients[(clients["nom"] == client_sel) & (clients["licence"] == licence_sel)]
        solde_avant = float(lic_row["solde_reel"].values[0]) if len(lic_row) > 0 else 0
        solde_apres = round(solde_avant - total_kgs, 2)

        st.markdown("---")
        p1, p2, p3, p4 = st.columns(4)
        p1.metric("Cartons/CNT",   f"{crtns_cnt:,}")
        p2.metric("Total cartons", f"{total_crtns:,}")
        p3.metric("Total kgs",     f"{total_kgs:,.0f}")
        p4.metric("Solde après",   f"{solde_apres:,.0f} kgs",
            delta=f"{-total_kgs:,.0f} kgs", delta_color="inverse")

        if solde_apres < 0:
            st.markdown('<div class="alert-red">⚠️ Solde insuffisant — commande bloquée</div>', unsafe_allow_html=True)
        elif solde_apres < 19591.2:
            st.markdown('<div class="alert-warn">🔴 Solde critique après cette commande</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="alert-ok">✅ Solde suffisant après cette commande</div>', unsafe_allow_html=True)

        submitted = st.form_submit_button("✅ Enregistrer la commande", use_container_width=True,
            type="primary", disabled=(solde_apres < 0))

        if submitted:
            st.session_state.new_commandes.append({
                "num":"", "semaine":sem, "client":client_sel,
                "booking":booking, "licence":licence_sel,
                "navire":navire, "voyage":voyage, "pol":pol_sel,
                "depart":depart.strftime("%d/%m/%Y"),
                "eta":eta.strftime("%d/%m/%Y"),
                "nb_cnt":nb_cnt, "produit":produit, "statut":"⏳ À GÉNÉRER"
            })
            st.cache_data.clear()
            st.success(f"✅ Commande {booking} enregistrée ! Va dans Commandes pour exporter le CSV.")
            st.rerun()
