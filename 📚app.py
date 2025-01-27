import streamlit as st

st.set_page_config(page_title="Edu_Chat", layout="wide")

st.sidebar.title("Navigation")
st.sidebar.page_link("pages/🏠acceuil.py", label="🏠 Accueil")
st.sidebar.page_link("pages/💬chatbot.py", label="💬 chatbot")

st.markdown("# <font color='#87CEEB'>Bienvenue sur Edu_Chat !</font>", unsafe_allow_html=True)
st.write("")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<font size='10'>📚</font>", unsafe_allow_html=True)

with col2:
    st.markdown("<font size='10'>🎓</font>", unsafe_allow_html=True)

with col3:
    st.markdown("<font size='10'>👨‍🎓</font>", unsafe_allow_html=True)

st.markdown("<font size='5'><b>Sélectionne une page dans la barre latérale pour commencer ton aventure éducative !</b></font>", unsafe_allow_html=True)