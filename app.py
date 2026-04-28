import streamlit as st
import pandas as pd
from datetime import datetime, date
import plotly.express as px
import plotly.graph_objects as go

# ── CONFIG PAGE ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EDEN FOOD — Dashboard",
    page_icon="🍌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── CSS CUSTOM ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  .main { background:#F4F6F9; }
  .block-container { padding:1.5rem 2rem; }
  .kpi-card { background:#fff; border-radius:12px; padding:18px 20px;
    box-shadow:0 1px 6px rgba(0,0,0,.08); border-left:4px solid #0D1B2A; }
  .kpi-val { font-size:2rem; font-weight:800; margin:4px 0; }
  .kpi-lbl { font-size:11px; color:#6B7280; text-transform:uppercase;
    letter-spacing:.5px; font-weight:600; }
  .kpi-sub { font-size:11px; color:#9CA3AF; margin-top:4px; }
  .section-hdr { font-size:12px; font-weight:700; color:#6B7280;
    text-transform:uppercase; letter-spacing:1px; margin:24px 0 12px; }
  .alert-red { background:#FDECEA; border-left:4px solid #C0392B;
    padding:12px 16px; border-radius:8px; color:#C0392B;
    font-weight:700; font-size:13px; margin:8px 0; }
  .alert-ok  { background:#E8F8F0; border-left:4px solid #1E8449;
    padding:12px 16px; border-radius:8px; color:#1E8449;
    font-weight:700; font-size:13px; margin:8px 0; }
  div[data-testid="stForm"] { background:#fff; border-radius:12px;
    padding:24px; box-shadow:0 1px 6px rgba(0,0,0,.08); border:none; }
</style>
""", unsafe_allow_html=True)

# ── CONSTANTES ────────────────────────────────────────────────────────────────
POIDS_UNIT = 18.14
CRTNS = {"TURBO(COLOMBIA)": 1080, "MOIN(COSTA RICA)": 1200}

# ── SESSION STATE (nouvelles commandes temporaires) ───────────────────────────
if "new_commandes" not in st.session_state:
    st.session_state.new_commandes = []

# ── LECTURE DONNÉES EXCEL ─────────────────────────────────────────────────────
@st.cache_data(ttl=60)
def load_clients():
    df = pd.read_excel("data/eden_food.xlsx", sheet_name="BASE CLIENTS",
                       usecols=list(range(9)), header=3)
    df.columns = ["num","nom","adresse1","adresse2","ville","pays","licence","poids_total","solde_init"]
    df = df[df["nom"].notna() & (df["nom"] != "")].copy()
    return df

@st.cache_data(ttl=60)
def load_commandes():
    df = pd.read_excel("data/eden_food.xlsx", sheet_name="COMMANDES",
                       usecols=list(range(13)), header=3)
    df.columns = ["num","semaine","client","booking","licence","navire","voyage",
                  "pol","depart","eta","nb_cnt","produit","statut"]
    df = df[df["client"].notna() & (df["client"] != "")].copy()
    df["nb_cnt"] = pd.to_numeric(df["nb_cnt"], errors="coerce").fillna(0).astype(int)
    df["crtns_cnt"] = df["pol"].apply(lambda x: CRTNS.get(str(x).strip(), 1200))
    df["total_crtns"] = df["nb_cnt"] * df["crtns_cnt"]
    df["total_kgs"]   = (df["total_crtns"] * POIDS_UNIT).round(2)
    return df

# ── FUSION BASE + NOUVELLES COMMANDES SESSION ─────────────────────────────────
clients_base   = load_clients()
commandes_base = load_commandes()

if st.session_state.new_commandes:
    df_sess = pd.DataFrame(st.session_state.new_commandes)
    df_sess["nb_cnt"]       = pd.to_numeric(df_sess["nb_cnt"], errors="coerce").fillna(0).astype(int)
    df_sess["crtns_cnt"]    = df_sess["pol"].apply(lambda x: CRTNS.get(str(x).strip(), 1200))
    df_sess["total_crtns"]  = df_sess["nb_cnt"] * df_sess["crtns_cnt"]
    df_sess["total_kgs"]    = (df_sess["total_crtns"] * POIDS_UNIT).round(2)
    commandes = pd.concat([commandes_base, df_sess], ignore_index=True)
else:
    commandes = commandes_base.copy()

clients = clients_base.copy()

# ── CALCUL SOLDE ──────────────────────────────────────────────────────────────
def get_solde(client_nom, licence, poids_total):
    mask = (commandes["client"] == client_nom) & (commandes["licence"] == licence)
    charge = commandes.loc[mask, "total_kgs"].sum()
    return round(poids_total - charge, 2)

clients["poids_total"] = pd.to_numeric(clients["poids_total"], errors="coerce").fillna(0)
clients["solde_reel"]  = clients.apply(
    lambda r: get_solde(r["nom"], r["licence"], r["poids_total"]), axis=1)

# ── HEADER ────────────────────────────────────────────────────────────────────
col_logo, col_title, col_refresh = st.columns([1,8,2])
with col_logo:
    st.markdown("## 🍌")
with col_title:
    st.markdown("# EDEN FOOD — Logistics Dashboard")
    st.caption(f"Licences DPVCT & Suivi Commandes · Mis à jour : {datetime.now().strftime('%d/%m/%Y %H:%M')}")
with col_refresh:
    if st.button("🔄 Rafraîchir", use_container_width=True):
        st.cache_data.clear()
        st.session_state.new_commandes = []
        st.rerun()

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Tableau de bord",
    "🚢 Commandes",
    "➕ Nouvelle commande",
    "📋 Licences clients"
])

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab1:
    st.markdown('<div class="section-hdr">📊 KPIs globaux</div>', unsafe_allow_html=True)

    todo   = commandes[commandes["statut"].str.contains("À GÉNÉRER", na=False)]
    done   = commandes[commandes["statut"].str.contains("GÉNÉRÉ", na=False)]
    alerte = clients[clients["solde_reel"] < 19591.2]
    depass = clients[clients["solde_reel"] < 0]

    k1,k2,k3,k4,k5,k6 = st.columns(6)
    for col, val, lbl, sub, color in [
        (k1, len(clients),              "Licences",      f"{clients['nom'].nunique()} clients", "#1E8449"),
        (k2, len(todo),                 "⏳ À générer",  "commandes en attente",                "#6C3483"),
        (k3, len(done),                 "✅ Générées",   "confirmations envoyées",               "#1A4D8F"),
        (k4, int(todo["nb_cnt"].sum()), "CNT en cours",  "conteneurs planifiés",                "#E67E22"),
        (k5, len(alerte),               "🔴 Alertes",    "licences critiques",                   "#C0392B"),
        (k6, len(depass),               "❌ Dépassements","licences négatives",                  "#C0392B"),
    ]:
        col.markdown(f"""
        <div class="kpi-card" style="border-color:{color}">
          <div class="kpi-lbl">{lbl}</div>
          <div class="kpi-val" style="color:{color}">{val}</div>
          <div class="kpi-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-hdr">📦 Volumes par semaine</div>', unsafe_allow_html=True)
    c1, c2 = st.columns([2,1])
    with c1:
        if not commandes.empty:
            df_sem = commandes.groupby("semaine")["nb_cnt"].sum().reset_index()
            fig = px.bar(df_sem, x="semaine", y="nb_cnt",
                title="Conteneurs chargés par semaine",
                color="nb_cnt", color_continuous_scale=["#1A4D8F","#E67E22","#C0392B"],
                labels={"semaine":"Semaine","nb_cnt":"Nb CNT"})
            fig.update_layout(showlegend=False, coloraxis_showscale=False,
                plot_bgcolor="#fff", paper_bgcolor="#fff",
                title_font_size=13, margin=dict(t=40,b=20,l=20,r=20))
            fig.update_traces(marker_cornerradius=4)
            st.plotly_chart(fig, use_container_width=True)
    with c2:
        if not commandes.empty:
            df_pol = commandes.groupby("pol")["nb_cnt"].sum().reset_index()
            fig2 = px.pie(df_pol, values="nb_cnt", names="pol",
                title="Répartition POL",
                color_discrete_sequence=["#1A4D8F","#E67E22"],
                hole=0.6)
            fig2.update_layout(title_font_size=13,
                margin=dict(t=40,b=20,l=20,r=20),
                legend=dict(orientation="h",yanchor="bottom",y=-0.2))
            st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="section-hdr">⚖️ Poids chargés (kgs)</div>', unsafe_allow_html=True)
    if not commandes.empty:
        df_kgs = commandes.groupby("semaine")["total_kgs"].sum().reset_index()
        fig3 = px.area(df_kgs, x="semaine", y="total_kgs",
            title="Poids chargés par semaine (kgs)",
            labels={"semaine":"Semaine","total_kgs":"Kgs"},
            color_discrete_sequence=["#1A4D8F"])
        fig3.update_layout(plot_bgcolor="#fff", paper_bgcolor="#fff",
            title_font_size=13, margin=dict(t=40,b=20,l=20,r=20))
        fig3.update_traces(fill="tozeroy")
        st.plotly_chart(fig3, use_container_width=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab2:
    st.markdown('<div class="section-hdr">🚢 Toutes les commandes</div>', unsafe_allow_html=True)

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

    st.dataframe(df_filt, use_container_width=True, height=420,
        column_config={
            "semaine":   st.column_config.TextColumn("Sem."),
            "booking":   st.column_config.TextColumn("Ref Booking"),
            "client":    st.column_config.TextColumn("Client"),
            "navire":    st.column_config.TextColumn("Navire"),
            "pol":       st.column_config.TextColumn("POL"),
            "depart":    st.column_config.TextColumn("Départ"),
            "eta":       st.column_config.TextColumn("ETA"),
            "nb_cnt":    st.column_config.NumberColumn("CNT", format="%d"),
            "total_kgs": st.column_config.NumberColumn("Kgs", format="%.0f"),
            "licence":   st.column_config.TextColumn("Licence"),
            "statut":    st.column_config.TextColumn("Statut"),
        }, hide_index=True)

    st.caption(f"**{len(df_filt)} commandes** · Total : {df_filt['nb_cnt'].sum()} CNT · {df_filt['total_kgs'].sum():,.0f} kgs")

    # ── EXPORT EXCEL ──────────────────────────────────────────────────────────
    if st.session_state.new_commandes:
        st.info(f"💾 {len(st.session_state.new_commandes)} nouvelle(s) commande(s) ajoutée(s) cette session — télécharge le fichier mis à jour :")
        export_df = commandes[["num","semaine","client","booking","licence",
            "navire","voyage","pol","depart","eta","nb_cnt","produit","statut"]]
        csv = export_df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Télécharger commandes (CSV)", csv,
            file_name=f"commandes_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv", use_container_width=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab3:
    st.markdown('<div class="section-hdr">➕ Saisir une nouvelle commande</div>', unsafe_allow_html=True)
    st.info("💡 Les nouvelles commandes sont actives pendant la session. Télécharge le CSV depuis l'onglet Commandes pour sauvegarder.")

    with st.form("form_commande", clear_on_submit=True):
        f1, f2 = st.columns(2)
        with f1:
            sem        = st.text_input("Semaine *", placeholder="ex: S-26")
            client_sel = st.selectbox("Client *", clients["nom"].unique().tolist())
            booking    = st.text_input("Référence Booking *", placeholder="ex: LHV4005547")
            licences_dispo = clients[clients["nom"]==client_sel]["licence"].tolist()
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

        lic_row     = clients[(clients["nom"]==client_sel)&(clients["licence"]==licence_sel)]
        solde_avant = float(lic_row["solde_reel"].values[0]) if len(lic_row)>0 else 0
        solde_apres = round(solde_avant - total_kgs, 2)

        st.markdown("---")
        p1,p2,p3,p4 = st.columns(4)
        p1.metric("Cartons/CNT",  f"{crtns_cnt:,}")
        p2.metric("Total cartons",f"{total_crtns:,}")
        p3.metric("Total kgs",    f"{total_kgs:,.2f}")
        p4.metric("Solde après",  f"{solde_apres:,.2f} kgs",
            delta=f"{-total_kgs:,.0f} kgs", delta_color="inverse")

        if solde_apres < 0:
            st.markdown('<div class="alert-red">⚠️ ATTENTION — Solde insuffisant. Commande bloquée.</div>', unsafe_allow_html=True)
        elif solde_apres < 19591.2:
            st.markdown('<div class="alert-red">🔴 Solde critique après cette commande</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="alert-ok">✅ Solde suffisant après cette commande</div>', unsafe_allow_html=True)

        submitted = st.form_submit_button("✅ Enregistrer la commande", use_container_width=True,
            type="primary", disabled=(solde_apres < 0))

        if submitted:
            new_row = {
                "num":"", "semaine":sem, "client":client_sel,
                "booking":booking, "licence":licence_sel,
                "navire":navire, "voyage":voyage, "pol":pol_sel,
                "depart":depart.strftime("%d/%m/%Y"),
                "eta":eta.strftime("%d/%m/%Y"),
                "nb_cnt":nb_cnt, "produit":produit,
                "statut":"⏳ À GÉNÉRER"
            }
            st.session_state.new_commandes.append(new_row)
            st.cache_data.clear()
            st.success(f"✅ Commande {booking} enregistrée ! Va dans l'onglet Commandes pour télécharger le fichier mis à jour.")
            st.rerun()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab4:
    st.markdown('<div class="section-hdr">📋 Licences & soldes</div>', unsafe_allow_html=True)
    for _, row in clients.iterrows():
        pct = max(0, min(100, row["solde_reel"]/row["poids_total"]*100)) if row["poids_total"]>0 else 0
        c1,c2,c3 = st.columns([2,4,2])
        with c1:
            st.markdown(f"**{row['nom'][:30]}**")
            st.caption(row["licence"])
        with c2:
            st.progress(pct/100)
            st.caption(f"Solde : **{row['solde_reel']:,.0f} kgs** / {row['poids_total']:,.0f} kgs")
        with c3:
            if row["solde_reel"] < 0:
                st.error("❌ DÉPASSEMENT")
            elif row["solde_reel"] < 19591.2:
                st.error("🔴 CRITIQUE")
            elif row["solde_reel"] < 58773.6:
                st.warning("⚠️ ATTENTION")
            else:
                st.success("✅ OK")
        st.divider()
