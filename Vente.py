import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Café-Blitz", page_icon="☕")

st.markdown("# ☕ Café-Blitz")
st.caption("Venez savourer nos plats et boissons")

# Fichier
fichier = "ventes.csv"

# Charger ou créer les données
if os.path.exists(fichier):
    df = pd.read_csv(fichier)
else:
    df = pd.DataFrame(columns=["produit", "qte"])

# Formulaire
st.subheader("📝 Enregistrer une vente")

produit = st.selectbox("Produit", ["Nouilles sautées", "Riz sauté", "Frit plantain", "Frit pomme", "Pain-oeuf", "Café", "Jus"])
qte = st.number_input("Quantité", min_value=1, step=1, value=1)

if st.button("✅ Enregistrer"):
    nouvelle_ligne = pd.DataFrame({"produit": [produit], "qte": [qte]})
    df = pd.concat([df, nouvelle_ligne], ignore_index=True)
    df.to_csv(fichier, index=False)
    st.success(f"{qte} x {produit} ajouté !")
    st.rerun()

# Analyse
if len(df) > 0:
    st.subheader("📊 Les produits les plus vendus")
    top = df.groupby("produit")["qte"].sum().sort_values(ascending=False)
    
    for i, (p, q) in enumerate(top.head(3).items(), 1):
        st.write(f"**{i}. {p}** → {q} vendus")
    
    meilleur = top.index[0]
    st.success(f"💡 Conseil : {meilleur} est ton meilleur produit !")
    
    total = df["qte"].sum()
    st.metric("Total produits vendus", total)
else:
    st.info("Ajoute ta première vente ci-dessus 👆")
