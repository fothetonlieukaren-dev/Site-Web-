import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import os

st.set_page_config(page_title="Café-Blitz", page_icon="🍛", layout="centered")

# --- ACCUEIL CHALEUREUX ---
st.markdown("""
<div style='text-align: center; padding: 2rem 0 1rem 0;'>
    <h1 style='color: #e67e22; font-size: 3rem;'>☕ Café-Blitz 🍛</h1>
    <p style='font-size: 1.3rem; color: #555;'>Venez savourer nos délicieux plats faits maison !</p>
    <p style='font-size: 1rem; color: #888;'>Nouilles sautées • Riz sauté • Frit plantain • Frit pomme • Pain-oeuf • Mayonnaise</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# --- Fichier pour sauvegarder ---
DATA_FILE = "ventes_cafe_blitz.csv"

# Charger ou créer les données
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["date", "produit", "quantite", "prix"])

# --- Liste des produits ---
produits = [
    "Nouilles sautées",
    "Riz sauté", 
    "Frit plantain",
    "Frit pomme",
    "Pain-oeuf",
    "Mayonnaise"
]

st.subheader("📝 Enregistrer une vente")

with st.form("ajout_vente"):
    col1, col2 = st.columns(2)
    with col1:
        produit = st.selectbox("Produit vendu", produits)
        quantite = st.number_input("Quantité", min_value=1, step=1, value=1)
    with col2:
        prix = st.number_input("Prix unitaire (F CFA)", min_value=100, step=50, value=500)
    
    submitted = st.form_submit_button("✅ Enregistrer la vente", use_container_width=True)
    
    if submitted:
        nouvelle_ligne = pd.DataFrame([{
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "produit": produit,
            "quantite": quantite,
            "prix": prix
        }])
        df = pd.concat([df, nouvelle_ligne], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success(f"✅ {quantite} x {produit} enregistré ({(quantite * prix):,} F)")
        st.rerun()

# --- Afficher les ventes du jour ---
if len(df) > 0:
    df["total"] = df["quantite"] * df["prix"]
    
    # Filtre pour aujourd'hui
    aujourdhui = datetime.now().strftime("%Y-%m-%d")
    df["date_jour"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
    ventes_aujourdhui = df[df["date_jour"] == aujourdhui]
    
    st.subheader("📊 Ventes du jour")
    
    if len(ventes_aujourdhui) > 0:
        col1, col2, col3 = st.columns(3)
        col1.metric("💰 CA du jour", f"{ventes_aujourdhui['total'].sum():,.0f} F")
        col2.metric("🍽️ Plats vendus", f"{ventes_aujourdhui['quantite'].sum()}")
        col3.metric("📦 Ventes", len(ventes_aujourdhui))
        
        # Petit tableau des ventes du jour
        st.dataframe(ventes_aujourdhui[["produit", "quantite", "prix", "total"]], 
                     use_container_width=True, hide_index=True)
    else:
        st.info("Aucune vente enregistrée aujourd'hui")
    
    # --- ANALYSE : Ce qui marche le mieux ---
    st.subheader("🔍 Ce qui marche le mieux")
    
    col_analyse1, col_analyse2 = st.columns(2)
    
    with col_analyse1:
        # Top produits par quantité
        top_qte = df.groupby("produit")["quantite"].sum().sort_values(ascending=False)
        if len(top_qte) > 0:
            meilleur = top_qte.index[0]
            chiffre = top_qte.iloc[0]
            st.info(f"🏆 **Produit le plus vendu**\n\n{meilleur}\n\n{chiffre} unités")
            
            # Petit graphique simple
            st.caption("Classement des ventes :")
            for i, (prod, qte) in enumerate(top_qte.head(4).items()):
                st.progress(min(qte / top_qte.iloc[0], 1.0), text=f"{i+1}. {prod} : {qte} vendus")
    
    with col_analyse2:
        # Top produits par chiffre d'affaires
        top_ca = df.groupby("produit")["total"].sum().sort_values(ascending=False)
        if len(top_ca) > 0:
            meilleur_ca = top_ca.index[0]
            st.success(f"💰 **Produit qui rapporte le plus**\n\n{meilleur_ca}\n\n{top_ca.iloc[0]:,.0f} F")
    
    # --- Conseils pour maximiser les ventes ---
    st.subheader("💡 Astuces pour toi")
    
    if len(df) > 5:
        top_produit = df.groupby("produit")["quantite"].sum().idxmax()
        low_produit = df.groupby("produit")["quantite"].sum().idxmin()
        
        st.markdown(f"""
        - ✅ **{top_produit}** se vend super bien ! Mets-le en avant sur l'ardoise
        - ⚠️ **{low_produit}** se vend moins. Peut-être une petite promo ?
        - 📈 Tu as fait {df['total'].sum():,.0f} F de CA au total
        """)
        
        # Analyse des heures de vente
        df["heure"] = pd.to_datetime(df["date"]).dt.hour
        heures_actives = df.groupby("heure")["quantite"].sum()
        if len(heures_actives) > 0:
            heure_peak = heures_actives.idxmax()
            st.info(f"⏰ Ton heure la plus active : {heure_peak}h → Prépare plus de plats à cette heure !")
    else:
        st.info("Encore quelques ventes et je pourrai te donner des conseils personnalisés !")
    
    # --- Historique complet (déroulant) ---
    with st.expander("📜 Voir tout l'historique des ventes"):
        st.dataframe(df[["date", "produit", "quantite", "prix", "total"]], 
                     use_container_width=True)
        st.caption(f"Total général : {df['total'].sum():,.0f} F")

else:
    st.info("📭 Aucune vente enregistrée pour le moment")
    st.markdown("""
    ### Comment utiliser :
    1. Choisis un **produit** dans la liste
    2. Entre la **quantité** vendue
    3. Entre le **prix** (ta gérante fixe le prix)
    4. Clique sur **Enregistrer**
    
    L'application analyse automatiquement ce qui marche le mieux !
    """)

# --- Bouton réinitialiser ---
st.divider()
col_reset, col_vide = st.columns([1, 3])
with col_reset:
    if st.button("🗑️ Réinitialiser", type="secondary"):
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
        st.success("Données effacées")
        st.rerun()
