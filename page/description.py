import streamlit as st
from PIL import Image
import os

# Récupérer le chemin d'accès au répertoire courant
current_dir = os.path.dirname(__file__)

# Fonction d'initialisation pour ajouter un style CSS personnalisé
def add_custom_css():
    st.markdown(
        """
        <style>
        /* Style global */
        body {
            font-family: 'Arial', sans-serif;
            background-color: #ecf0f1;
            color: #2c3e50;
        }

        /* En-tête */
        .header-title {
            color: #ffffff;
            font-size: 56px;
            font-weight: 700;
            text-align: center;
            margin-top: 30px;
            background: linear-gradient(135deg, #3498db, #8e44ad);
            -webkit-background-clip: text;
            color: transparent;
        }

        /* Petit texte en bleu pour les éléments en gras */
        .content-text b {
            color: #3498db;
        }

        /* Sous-titre */
        .subheader-title {
            color: #2c3e50;
            font-size: 36px;
            font-weight: 600;
            text-align: center;
            margin-bottom: 20px;
            text-transform: uppercase;
        }

        /* Petites images devant les titres */
        .title-image {
            width: 30px;
            height: 30px;
            margin-right: 10px;
            vertical-align: middle;
        }

        /* Contenu des sections */
        .content-text {
            color: #34495e;
            font-size: 18px;
            line-height: 1.7;
            margin-bottom: 20px;
        }

        .content-text ul {
            list-style-type: none;
            padding: 0;
        }

        .content-text li {
            margin-bottom: 15px;
        }

        /* Boutons */
        .button {
            background-color: #2980b9;
            color: white;
            font-size: 18px;
            padding: 12px 25px;
            border-radius: 30px;
            border: none;
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .button:hover {
            background-color: #3498db;
            transform: scale(1.05);
        }

        /* Image de la section */
        .header-image {
            width: 100%;
            max-width: 600px; /* Taille réduite de l'image */
            border-radius: 15px;
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
            margin: 0 auto;
            display: block;
        }

        /* Pied de page */
        .footer {
            text-align: center;
            color: #95a5a6;
            font-size: 14px;
            margin-top: 30px;
            padding: 10px;
            background-color: #2c3e50;
            color: white;
        }
        </style>
        """, unsafe_allow_html=True
    )

# Ajouter du CSS personnalisé
add_custom_css()

# Titre principal
st.markdown("<h1 class='header-title'>Description du Travail</h1>", unsafe_allow_html=True)

# Charger l'image d'en-tête
header_image_path = os.path.join(current_dir, "education.jpg")
header_image = Image.open(header_image_path)

# Redimensionner l'image
header_image = header_image.resize((600, 300))  # Taille réduite de l'image

# Afficher l'image avec un style appliqué via CSS
st.image(header_image, caption="Edu Chat - Aide à l'éducation", use_container_width=True)

# Introduction
with st.expander("💡 Introduction"):
    st.markdown(
        """
        **Edu Chat** est une application conçue pour aider les élèves et les enseignants du secondaire dans les établissements du Cameroun à consulter les syllabus de cours.
        Accessible aussi bien aux systèmes francophones qu’anglophones, elle permet d'obtenir des informations détaillées sur les matières enseignées.
        Grâce à une interface intuitive, Edu Chat simplifie l’apprentissage et la recherche d’informations.
        """
    )

# Fonctionnalités principales
with st.expander("🔧 Fonctionnalités principales"):
    st.markdown(
        """
        - **Consultation du syllabus** : Accédez aux détails de chaque matière.
        - **Chatbot éducatif** : Posez des questions sur les cours et obtenez des réponses.
        - **Interface intuitive** : Navigation simple et fluide.
        - **Multilingue** : Support des systèmes francophone et anglophone.
        - **Mises à jour régulières** : Améliorations et ajout de nouvelles matières.
        """
    )

# Technologies utilisées
with st.expander("⚙️ Technologies utilisées"):
    st.markdown(
        """
        - **Python** (Langage principal)
        - **Streamlit** (Framework pour l'interface utilisateur)
        - **NLP & Machine Learning** (Gestion du chatbot)
        - **Base de données** (Stockage des PDFs de programmes de chaque matière)
        """
    )

# Public cible
with st.expander("🎯 Public Cible"):
    st.markdown(
        """
        - **Élèves du secondaire** au Cameroun (Francophones & Anglophones)
        - **Enseignants & Éducateurs** souhaitant structurer leurs cours
        - **Parents** qui veulent suivre le programme scolaire de leurs enfants
        """
    )

# Comment utiliser l'application
with st.expander("📱 Comment utiliser Edu_Chat ?"):
    st.markdown(
        """
        1. **Naviguez dans le menu** pour choisir une rubrique (Description, Contact, Chat...).
        2. **Sélectionnez votre matière** et consultez son syllabus.
        3. **Posez des questions au chatbot** pour obtenir des précisions sur un sujet.
        4. **Profitez d'une expérience fluide et interactive** !
        """
    )

# Contact
with st.expander("📞 Contact & Support"):
    st.markdown(
        """
        - **Email** : arlysimo@gmail.com  
        - **Site Web** : [www.edu-chat.com](https://www.edu-chat.com)  
        - **Téléphone** : +237 656 109 435
        """
    )

# Bouton pour visiter le site web
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.button("Visitez notre site web", key="visit_button", help="Accédez au site pour plus d'informations", use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# Pied de page
st.markdown("<div class='footer'>&copy; 2025 Edu Chat. Tous droits réservés.</div>", unsafe_allow_html=True)
