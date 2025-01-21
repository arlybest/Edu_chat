import streamlit as st
from PIL import Image

# Charger l'image de l'en-tête 
header_image_path = "page/description.jpg"  # Vérifie ce chemin
header_image = Image.open(header_image_path)

# Afficher l'en-tête avec une image
st.image(header_image, use_container_width=True)

# Titre principal
st.title("📌 Description du Travail")

# Introduction
st.markdown(
    """
    **Edu Chat** est une application conçue pour aider les élèves et étudiants à consulter le syllabus 
    des cours du secondaire au Cameroun. Accessible aussi bien aux systèmes francophones qu’anglophones, 
    elle permet d'obtenir des informations détaillées sur les matières enseignées.
    
    Grâce à une interface intuitive, Edu Chat simplifie l’apprentissage et la recherche d’informations.
    """
)

# Fonctionnalités principales
st.subheader("🔹 Fonctionnalités de l'application")
st.markdown(
    """
    - 📚 **Consultation du syllabus** : Accédez aux détails de chaque matière.
    - 💬 **Chatbot éducatif** : Posez des questions sur les cours et obtenez des réponses.
    - 🎨 **Interface intuitive** : Navigation simple et fluide.
    - 🌍 **Multilingue** : Support des systèmes francophone et anglophone.
    - 📈 **Mises à jour régulières** : Améliorations et ajout de nouvelles matières.
    """
)

# Technologies utilisées
st.subheader("🛠️ Technologies utilisées")
st.markdown(
    """
    - 🐍 **Python** (Langage principal)
    - 🎨 **Streamlit** (Framework pour l'interface utilisateur)
    - 🤖 **NLP & Machine Learning** (Gestion du chatbot)
    - 💾 **Base de données** (Stockage des syllabus)
    """
)

# Public cible
st.subheader("🎯 Public Cible")
st.markdown(
    """
    - 📖 **Élèves du secondaire** au Cameroun (Francophones & Anglophones)
    - 🏫 **Enseignants & Éducateurs** souhaitant structurer leurs cours
    - 👨‍👩‍👧 **Parents** qui veulent suivre le programme scolaire de leurs enfants
    """
)

# Comment utiliser l'application
st.subheader("🚀 Comment utiliser Edu_Chat ?")
st.markdown(
    """
    1. **Naviguez dans le menu** pour choisir une rubrique (Description, Contact, Chat...).
    2. **Sélectionnez votre matière** et consultez son syllabus.
    3. **Posez des questions au chatbot** pour obtenir des précisions sur un sujet.
    4. **Profitez d'une expérience fluide et interactive !** 🎉
    """
)

# Ajouter une image d'illustration si besoin
image_path = "page/description.jpg"  
image = Image.open(image_path)
st.image(image, caption="Interface de Edu Chat", use_container_width=True)

# Contact
st.subheader("📞 Contact & Support")
st.markdown(
    """
    - 📧 **Email** : arlysimo@gmail.com  
    - 🌍 **Site Web** : [www.edu-chat.com](https://www.edu-chat.com)  
    - 📱 **Téléphone** : +237 656 109 435
    """
)
