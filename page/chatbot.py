import streamlit as st
from transformers import pipeline
import random

# Initialisation du modèle (Utilisation d'un modèle par défaut si aucun modèle spécifique n'est encore défini)
try:
    generator = pipeline("text-generation", model="distilgpt2")
except Exception as e:
    generator = None
    st.error(f"Erreur lors du chargement du modèle : {e}")

# Liste de réponses aléatoires en attendant un vrai modèle
default_responses = [
    "Je suis encore en apprentissage !",
    "Je vais bientôt pouvoir mieux répondre.",
    "Merci pour votre question !",
    "Je suis là pour vous aider."
]

# Fonction pour générer une réponse
def get_bot_response(user_input):
    if generator:
        response = generator(user_input, max_length=100, num_return_sequences=1)
        return response[0]['generated_text']
    else:
        return random.choice(default_responses)

# Fonction de l'application chatbot
def app():
    # Titre de la page
    st.title("Edu_Chat")
    st.markdown(
        """
        <style>
            .stTextInput>div>div>input {
                font-size: 18px;
                height: 40px;
            }
            .stButton>button {
                background-color: #02ab21;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 16px;
            }
            .message-container {
                max-width: 600px;
                margin: auto;
                padding: 10px;
                border-radius: 8px;
                background-color: #f0f0f5;
            }
            .user-message {
                background-color: #A0D8FF;
                padding: 10px;
                border-radius: 10px;
                margin-bottom: 5px;
            }
            .bot-message {
                background-color: #D8E1F3;
                padding: 10px;
                border-radius: 10px;
                margin-bottom: 5px;
            }
        </style>
        """, unsafe_allow_html=True
    )

    # Message de bienvenue
    st.markdown("**Bienvenue sur Edu Chat !** Posez vos questions et je vous répondrai avec plaisir.")

    # Initialisation de l'historique des messages
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Champ de saisie utilisateur
    user_input = st.text_input("Votre question", "", key="input_text")

    # Bouton d'envoi
    if st.button("Envoyer", key="send_button"):
        if user_input:
            # Ajout du message utilisateur
            st.session_state.messages.append({"role": "user", "message": user_input})

            # Réponse du chatbot
            bot_response = get_bot_response(user_input)

            # Ajout de la réponse du chatbot
            st.session_state.messages.append({"role": "bot", "message": bot_response})

    # Affichage des messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="message-container"><div class="user-message">**Vous** : {message["message"]}</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="message-container"><div class="bot-message">**Chatbot** : {message["message"]}</div></div>', unsafe_allow_html=True)

    # Champ de texte avec placeholder
    st.text_input("Appuyez sur 'Enter' pour envoyer", "", key="message_input", placeholder="Tapez ici...", label_visibility="collapsed")

    # Message d'assistance
    st.markdown(
        """
        <p style="font-size: 14px; color: #808080; text-align: center;">
            Si vous avez des questions concernant le syllabus ou un autre sujet, je suis là pour vous aider.
        </p>
        """, unsafe_allow_html=True
    )

# Lancer l'application
if __name__ == "__main__":
    app()
