import streamlit as st

st.set_page_config(page_title="Mon bloc-notes", page_icon="📓")

st.title("📓 Mon bloc-notes")

# Stocker les notes dans la session
if "notes" not in st.session_state:
    st.session_state.notes = []

nouvelle_note = st.text_input("📝 Écris ta note")

if st.button("Ajouter"):
    if nouvelle_note:
        st.session_state.notes.append(nouvelle_note)
        st.success("Note ajoutée !")

# Afficher les notes
if st.session_state.notes:
    st.write("### 📋 Tes notes :")
    for i, note in enumerate(st.session_state.notes):
        st.write(f"{i+1}. {note}")
