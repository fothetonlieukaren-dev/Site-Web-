import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Café-Blitz", page_icon="☕")

# === ACCUEIL ===
st.markdown("# ☕ Café-Blitz 🍛")
st.markdown("*Venez savourer nos délicieux plats et boissons !*")

# === FICHIER ===
fichier = "ventes.csv"

# Charger les données
if os.path.exists(fichier):
    df = pd.read_csv(fichier)
else:
    df = pd.DataFrame(columns=["date", "produit", "qte", "prix"])

# === FORMULAIRE SIMPLE ===
st.subheader("📝 Enregistrer une vente")

with st.form("vente"):
    col1, col2 = st.columns(2)
    with col1:
        produit = st.selectbox("Produit", [
            "Nouilles sautées", "Riz sauté", "Frit plantain", 
            "Frit pomme", "Pain-oeuf", "Café noir", "Café au lait",
            "Jus d'orange", "Jus de bissap", "Soda"
        ])
        qte = st.number_input("Quantité", 1, 20, 1)
    with col2:
        prix = st.number_input("Prix (F CFA)", 100, 2000, 500)
    
    if st.form_submit_button("✅ Enregistrer"):
        nouvelle = pd.DataFrame([{
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "produit": produit,
            "qte": qte,
            "prix": prix
        }])
        df = pd.concat([df, nouvelle], ignore_index=True)
        df.to_csv(fichier, index=False)
        st.success(f"✅ {qte} {produit} ajouté")
        st.rerun()

# === ANALYSE SIMPLE ===
if len(df) > 0:
    df["total"] = df["qte"] * df["prix"]
    
    st.subheader("📊 Ce qui marche le mieux")
    
    # Top produits
    top = df.groupby("produit")["qte"].sum().sort_values(ascending=False).head(3)
    
    col1, col2, col3 = st.columns(3)
    for i, (produit, qte) in enumerate(top.items()):
        with [col1, col2, col3][i]:
            st.metric(f"🏆 N°{i+1}", produit, f"{qte} vendus")
    
    # Petit conseil
    meilleur = top.index[0] if len(top) > 0 else "rien"
    st.info(f"💡 **Conseil :** {meilleur} est ton meilleur produit → mets-le en avant !")
    
    # Total CA
    st.metric("💰 Chiffre d'affaires total", f"{df['total'].sum():,.0f} F")
    
    # Dernières ventes
    with st.expander("📜 Dernières ventes"):
        st.dataframe(df[["date", "produit", "qte", "prix"]].tail(10))
else:
    st.info("📭 Aucune vente. Enregistre ta première vente !")
