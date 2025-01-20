import streamlit as st
from streamlit_option_menu import option_menu
import os
from dotenv import load_dotenv
load_dotenv()

# Importer les pages de l'application
import acceuil, description, chatbot

# Configuration de la page principale
st.set_page_config(
    page_title="Edu Chat - Assistant Éducatif",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Intégration de Google Analytics
st.markdown(
    f"""
        <script async src="https://www.googletagmanager.com/gtag/js?id={os.getenv('analytics_tag')}"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){{dataLayer.push(arguments);}}
            gtag('js', new Date());
            gtag('config', '{os.getenv('analytics_tag')}');
        </script>
    """,
    unsafe_allow_html=True
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

    def run():
        with st.sidebar:
            app = option_menu(
                menu_title='📚 Edu Chat - Menu',
                options=['🏠 Accueil', '📖 description', '💬 Chatbot', 'ℹ️ À propos', '📞 Contact'],
                icons=['house-fill', 'book-fill', 'chat-fill', 'info-circle-fill', 'telephone-fill'],
                menu_icon='cast',
                default_index=0,
                styles={
                    "container": {"padding": "5px", "background-color": "#1E1E1E"},
                    "icon": {"color": "#FFD700", "font-size": "22px"}, 
                    "nav-link": {"color": "#FFFFFF", "font-size": "18px", "text-align": "left", "--hover-color": "#0056b3"},
                    "nav-link-selected": {"background-color": "#0056b3", "color": "white"},
                }
            )

        # Navigation entre les pages
        if app == "🏠 Accueil":
            acceuil.app()
        elif app == "📖 description":
            description.app()
        elif app == "💬 Chatbot":
            chatbot.app()
        

    run()
