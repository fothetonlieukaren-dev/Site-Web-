import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px
import os

st.set_page_config(page_title="Café-Blitz", page_icon="☕", layout="wide")

# --- EN-TÊTE ACCUEIL ---
st.markdown("""
<div style='text-align: center; padding: 2rem 0 1rem 0; background: linear-gradient(135deg, #fff5eb, #ffe8d6); border-radius: 20px; margin-bottom: 2rem;'>
    <h1 style='color: #e67e22; font-size: 3rem;'>☕ Café-Blitz 🍛</h1>
    <p style='font-size: 1.3rem; color: #555;'>Venez savourer nos délicieux plats et boissons fraîches !</p>
    <p style='font-size: 1rem; color: #888;'>Plats chauds • Cafés • Jus naturels • Spécialités maison</p>
</div>
""", unsafe_allow_html=True)

# --- Fichier de sauvegarde ---
DATA_FILE = "ventes_cafe_blitz.csv"

# Charger ou créer les données
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["date", "categorie", "produit", "quantite", "prix"])

# --- TOUS LES PRODUITS DU CAFÉ ---
produits = {
    "🥘 Plats chauds": [
        "Nouilles sautées", "Riz sauté", "Riz gras", "Poulet DG", "Poisson braisé"
    ],
    "🍟 Fritures & Snacks": [
        "Frit plantain", "Frit pomme", "Frit beignet", "Pain-oeuf", "Mayonnaise", "Samoussa"
    ],
    "☕ Cafés": [
        "Café noir", "Café au lait", "Cappuccino", "Latte", "Expresso"
    ],
    "🧃 Jus & Boissons": [
        "Jus d'orange", "Jus de bissap", "Jus de gingembre", "Jus de mangue", "Jus d'ananas",
        "Citron pressé", "Dabino", "Eau minérale", "Soda"
    ],
    "🍰 Desserts": [
        "Tarte aux fruits", "Gâteau au chocolat", "Beignet au miel", "Glace vanille"
    ]
}

# Aplatir la liste des produits
liste_produits = []
for cat, items in produits.items():
    for item in items:
        liste_produits.append(item)

st.subheader("📝 Enregistrer une vente")

col_form1, col_form2 = st.columns([1, 1])

with col_form1:
    with st.form("ajout_vente"):
        categorie = st.selectbox("Catégorie", list(produits.keys()))
        # Afficher les produits selon la catégorie choisie
        produits_cat = produits[categorie]
        produit = st.selectbox("Produit", produits_cat)
        quantite = st.number_input("Quantité vendue", min_value=1, step=1, value=1)
        prix = st.number_input("Prix unitaire (F CFA)", min_value=100, step=50, value=500)
        
        submitted = st.form_submit_button("✅ Enregistrer la vente", use_container_width=True)
        
        if submitted:
            nouvelle_ligne = pd.DataFrame([{
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "categorie": categorie,
                "produit": produit,
                "quantite": quantite,
                "prix": prix
            }])
            df = pd.concat([df, nouvelle_ligne], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success(f"✅ {quantite} x {produit} enregistré !")
            st.rerun()

with col_form2:
    st.markdown("""
    <div style='background: #fef7e0; padding: 1rem; border-radius: 15px; margin-top: 2rem;'>
        <p style='font-size: 0.9rem; color: #e67e22;'>💡 <strong>Astuce</strong></p>
        <p style='font-size: 0.85rem; color: #555;'>Enregistre chaque vente au fur et à mesure.<br>L'application analysera automatiquement ce qui marche le mieux !</p>
    </div>
    """, unsafe_allow_html=True)

# --- AFFICHAGE ET ANALYSE ---
if len(df) > 0:
    df["total"] = df["quantite"] * df["prix"]
    
    # Filtre pour aujourd'hui
    aujourdhui = datetime.now().strftime("%Y-%m-%d")
    df["date_jour"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
    ventes_aujourdhui = df[df["date_jour"] == aujourdhui]
    
    # --- KPI principaux ---
    st.subheader("📊 Vue d'ensemble")
    col1, col2, col3, col4 = st.columns(4)
    
    ca_total = df["total"].sum()
    produits_vendus = df["quantite"].sum()
    col1.metric("💰 CA total", f"{ca_total:,.0f} F")
    col2.metric("🍽️ Produits vendus", f"{produits_vendus}")
    col3.metric("📦 Ventes enregistrées", len(df))
    
    if len(ventes_aujourdhui) > 0:
        col4.metric("📅 CA aujourd'hui", f"{ventes_aujourdhui['total'].sum():,.0f} F")
    else:
        col4.metric("📅 CA aujourd'hui", "0 F")
    
    # --- ANALYSE : CE QUI MARCHE LE MIEUX ---
    st.markdown("---")
    st.markdown("## 🔍 Analyse des ventes")
    st.markdown("*Voici ce qui se vend le mieux dans ton café*")
    
    # Onglets d'analyse
    tab1, tab2, tab3, tab4 = st.tabs(["🏆 Top produits", "📊 Par catégorie", "📈 Évolution", "💡 Conseils"])
    
    with tab1:
        col_top1, col_top2 = st.columns(2)
        
        with col_top1:
            st.markdown("### 🔥 Produits les plus vendus (quantité)")
            top_quantite = df.groupby("produit")["quantite"].sum().sort_values(ascending=False).head(10)
            
            fig1 = px.bar(
                x=top_quantite.values, y=top_quantite.index, orientation='h',
                text_auto=True, color=top_quantite.values,
                color_continuous_scale="oranges"
            )
            fig1.update_layout(height=400, title="Top 10 des produits les plus commandés")
            st.plotly_chart(fig1, use_container_width=True)
            
            meilleur_qte = top_quantite.index[0]
            st.success(f"🏆 **Produi le plus vendu : {meilleur_qte}** → {top_quantite.iloc[0]} unités")
        
        with col_top2:
            st.markdown("### 💰 Produits qui rapportent le plus (CA)")
            top_ca = df.groupby("produit")["total"].sum().sort_values(ascending=False).head(10)
            
            fig2 = px.bar(
                x=top_ca.values, y=top_ca.index, orientation='h',
                text_auto=True, color=top_ca.values,
                color_continuous_scale="reds"
            )
            fig2.update_layout(height=400, title="Top 10 du chiffre d'affaires")
            st.plotly_chart(fig2, use_container_width=True)
            
            meilleur_ca = top_ca.index[0]
            st.info(f"💰 **Produit le plus rentable : {meilleur_ca}** → {top_ca.iloc[0]:,.0f} F")
    
    with tab2:
        st.markdown("### Par catégorie de produits")
        
        col_cat1, col_cat2 = st.columns(2)
        
        with col_cat1:
            # Quantité par catégorie
            qte_categorie = df.groupby("categorie")["quantite"].sum().sort_values(ascending=False)
            fig3 = px.pie(
                values=qte_categorie.values, names=qte_categorie.index,
                title="Répartition des ventes par catégorie (quantité)",
                color_discrete_sequence=px.colors.sequential.Oranges_r
            )
            st.plotly_chart(fig3, use_container_width=True)
        
        with col_cat2:
            # CA par catégorie
            ca_categorie = df.groupby("categorie")["total"].sum().sort_values(ascending=False)
            fig4 = px.pie(
                values=ca_categorie.values, names=ca_categorie.index,
                title="Répartition du chiffre d'affaires par catégorie",
                color_discrete_sequence=px.colors.sequential.Reds_r
            )
            st.plotly_chart(fig4, use_container_width=True)
        
        # Meilleure catégorie
        meilleure_cat_qte = qte_categorie.index[0]
        meilleure_cat_ca = ca_categorie.index[0]
        
        st.markdown(f"""
        <div style='background: #e8f5e9; padding: 1rem; border-radius: 15px; margin-top: 1rem;'>
            <p>✅ <strong>Catégorie la plus vendue :</strong> {meilleure_cat_qte}</p>
            <p>💰 <strong>Catégorie qui rapporte le plus :</strong> {meilleure_cat_ca}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### Évolution des ventes dans le temps")
        
        # Ventes par jour
        df["date_simple"] = pd.to_datetime(df["date"]).dt.date
        ventes_par_jour = df.groupby("date_simple")["total"].sum().reset_index()
        
        if len(ventes_par_jour) > 1:
            fig5 = px.line(
                ventes_par_jour, x="date_simple", y="total",
                title="Chiffre d'affaires par jour",
                markers=True, color_discrete_sequence=["#e67e22"]
            )
            fig5.update_layout(height=400)
            st.plotly_chart(fig5, use_container_width=True)
            
            # Meilleur jour
            meilleur_jour = ventes_par_jour.loc[ventes_par_jour["total"].idxmax()]
            st.info(f"📅 **Meilleur jour :** {meilleur_jour['date_simple']} → {meilleur_jour['total']:,.0f} F")
        else:
            st.info("Encore quelques jours de vente pour voir l'évolution 📈")
        
        # Ventes par heure
        df["heure"] = pd.to_datetime(df["date"]).dt.hour
        ventes_par_heure = df.groupby("heure")["quantite"].sum().reset_index()
        
        if len(ventes_par_heure) > 1:
            fig6 = px.bar(
                ventes_par_heure, x="heure", y="quantite",
                title="Ventes par heure de la journée",
                color_discrete_sequence=["#f39c12"]
            )
            fig6.update_layout(height=350)
            st.plotly_chart(fig6, use_container_width=True)
            
            heure_peak = ventes_par_heure.loc[ventes_par_heure["quantite"].idxmax(), "heure"]
            st.success(f"⏰ **Heure de pointe :** {heure_peak}h → prépare plus de stock à ce moment !")
    
    with tab4:
        st.markdown("## 💡 Actions pour maximiser tes ventes")
        
        # Analyse intelligente des données
        top_ventes = df.groupby("produit")["quantite"].sum().sort_values(ascending=False)
        flop_ventes = df.groupby("produit")["quantite"].sum().sort_values(ascending=True)
        
        top3 = top_ventes.head(3).index.tolist()
        flop3 = flop_ventes.head(3).index.tolist() if len(flop_ventes) >= 3 else flop_ventes.index.tolist()
        
        col_ast1, col_ast2 = st.columns(2)
        
        with col_ast1:
            st.markdown("### ✅ À faire")
            st.markdown(f"""
            - **Mets en avant** : {', '.join(top3[:3])}
            - Propose ces produits en **menu du jour**
            - Fais une belle **affiche** pour ces best-sellers
            - Augmente légèrement le stock pour répondre à la demande
            """)
        
        with col_ast2:
            st.markdown("### ⚠️ À surveiller")
            st.markdown(f"""
            - **{flop3[0] if flop3 else 'certains produits'}** se vendent peu
            - Essaie une **promotion** ou un **prix découverte**
            - Demande aux clients pourquoi ils n'achètent pas ça
            - Peut-être à retirer de la carte
            """)
        
        # Conseils par catégorie
        ca_cat = df.groupby("categorie")["total"].sum()
        meilleure_cat = ca_cat.idxmax() if not ca_cat.empty else "aucune"
        
        st.markdown("---")
        st.markdown("### 🎯 Offres recommandées")
        
        if "🥘 Plats chauds" in meilleure_cat:
            st.markdown("**Formule Midi Express :** 1 plat chaud + 1 boisson → prix avantageux")
        if "☕ Cafés" in meilleure_cat:
            st.markdown("**Café + Viennoiserie** à prix doux")
        if "🧃 Jus & Boissons" in meilleure_cat:
            st.markdown("**Happy Hour Jus** entre 15h-17h")
        
        st.markdown("""
        ### 📢 Actions rapides
        1. **Affiche le top 3** du moment sur une ardoise
        2. **Fidélité** : 10 achats = 1 offert
        3. **Goûter découverte** pour les produits qui se vendent moins
        """)
    
    # --- HISTORIQUE DES VENTES ---
    with st.expander("📜 Voir tout l'historique des ventes"):
        st.dataframe(df[["date", "categorie", "produit", "quantite", "prix", "total"]], 
                     use_container_width=True, hide_index=True)
        st.caption(f"💰 Total général depuis le début : {df['total'].sum():,.0f} F")

else:
    st.info("📭 Aucune vente enregistrée pour le moment")
    st.markdown("""
    ### 🎯 Comment utiliser Café-Blitz :
    
    1. Choisis la **catégorie** (Plats, Fritures, Cafés, Jus, Desserts)
    2. Sélectionne le **produit** vendu
    3. Entre la **quantité**
    4. Fixe le **prix** (c'est toi qui décides)
    5. Clique sur **Enregistrer**
    
    ⭐ Plus tu enregistres de ventes, plus l'application t'aide à savoir **ce qui marche** et **ce qui ne marche pas** !
    """)

# --- RÉINITIALISATION ---
st.divider()
col_reset, col_info = st.columns([1, 3])
with col_reset:
    if st.button("🗑️ Réinitialiser toutes les ventes", type="secondary"):
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
        st.success("Toutes les données ont été effacées")
        st.rerun()
