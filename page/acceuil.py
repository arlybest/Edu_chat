import streamlit as st
from streamlit_option_menu import option_menu
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Importer les pages de l'application
import acceuil, description, chatbot

# Configuration de la page principale
st.set_page_config(
    page_title="Edu_Chat - Assistant Éducatif",
    layout="wide",
    initial_sidebar_state="expanded"
)




# Définition de la classe MultiApp pour gérer les pages
class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        # Menu latéral avec Streamlit OptionMenu
        with st.sidebar:
            app = option_menu(
                menu_title='📚 Edu_Chat - Menu',
                options=['🏠 Accueil', '📖 Description', '💬 Chatbot'],
                icons=['house-fill', 'book-fill', 'chat-fill', ],
                menu_icon='cast',
                default_index=0,
                styles={
                    "container": {"padding": "10px", "background-color": "#2c3e50"},
                    "icon": {"color": "#1abc9c", "font-size": "20px"},
                    "nav-link": {"color": "#ecf0f1", "font-size": "18px", "text-align": "left", "--hover-color": "#2980b9"},
                    "nav-link-selected": {"background-color": "#2980b9", "color": "white", "border-radius": "5px"},
                }
            )

        # Navigation entre les pages
        if app == "🏠 Accueil":
            acceuil.app()
        elif app == "📖 Description":
            description.app()
        elif app == "💬 Chatbot":
            chatbot.app()
        

    def about(self):
        st.title("À propos de Edu Chat")
        st.markdown(
            """
            **Edu Chat** est un assistant éducatif intelligent destiné aux élèves et aux enseignants du secondaire au Cameroun. 
            Cette application facilite l'accès aux syllabus des matières, tout en offrant un chatbot capable de répondre aux questions des utilisateurs.
            """
        )

    def contact(self):
        st.title("Contact & Support")
        st.markdown(
            """
            - **Email** : arlysimo@gmail.com  
            - **Site Web** : [www.edu-chat.com](https://www.edu-chat.com)  
            - **Téléphone** : +237 656 109 435
            """
        )

# Lancer l'application
app = MultiApp()
app.add_app("🏠 Accueil", acceuil.app)
app.add_app("📖 Description", description.app)
app.add_app("💬 Chatbot", chatbot.app)
app.run()
