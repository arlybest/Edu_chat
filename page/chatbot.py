import streamlit as st
from transformers import pipeline
import random

# Fonction d'initialisation pour le modèle 
generator = pipeline('text-generation', model='gpt2')

# Fonction pour générer une réponse avec GPT-2 (ou tout autre modèle)
def get_bot_response(user_input):
    response = generator(user_input, max_length=100, num_return_sequences=1)
    return response[0]['generated_text']

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

    # Affichage du message de bienvenue
    st.markdown("**Bienvenue sur le Chatbot Edu Chat!** \nPosez vos questions et je vais vous répondre avec plaisir.")

    # Initialisation de la session pour garder l'historique de la conversation
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Saisie de texte pour l'utilisateur
    user_input = st.text_input("Votre question", "", key="input_text")

    # Bouton pour envoyer le message
    if st.button("Envoyer", key="send_button"):
        # Ajouter le message de l'utilisateur dans l'historique
        if user_input:
            st.session_state.messages.append({"role": "user", "message": user_input})

            # Générer une réponse du chatbot
            bot_response = get_bot_response(user_input)

            # Ajouter la réponse du chatbot dans l'historique
            st.session_state.messages.append({"role": "bot", "message": bot_response})

            # Réinitialiser le champ de texte après envoi
            st.text_input("Votre question", "", key="reset_input")

    # Affichage de l'historique des messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="message-container"><div class="user-message">**Vous** : {message["message"]}</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="message-container"><div class="bot-message">**Chatbot** : {message["message"]}</div></div>', unsafe_allow_html=True)

    # Option d'entrée avec un placeholder pour guider l'utilisateur
    st.text_input("Appuyez sur 'Enter' pour envoyer", "", key="message_input", placeholder="Tapez ici...", label_visibility="collapsed")

    # Message d'assistance pour l'utilisateur
    st.markdown(
        """
        <p style="font-size: 14px; color: #808080; text-align: center;">
            Si vous avez des questions concernant le syllabus ou autre sujet, je suis là pour vous aider.
        </p>
        """, unsafe_allow_html=True
    )
