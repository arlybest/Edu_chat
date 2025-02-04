import streamlit as st
import random

st.set_page_config(page_title="Edu_Chat - Chatbot", layout="wide")

# Définir des réponses automatiques basiques
responses = {
    "bonjour": "Bonjour ! Comment puis-je vous aider aujourd'hui ?",
    "syllabus": "Vous pouvez consulter les syllabus en sélectionnant votre classe et matière.",
    "merci": "Avec plaisir ! 😊",
    "au revoir": "Au revoir ! Bonne journée et bon apprentissage ! 📚",
    "default": "Je ne suis pas sûr de comprendre. Pouvez-vous reformuler ?"
}

# Définir des intents
intents = {
    "demande_info": ["Qu'est-ce que", "Pouvez-vous me dire", "Je voudrais savoir"],
    "pose_question": ["Quelle est", "Qu'est-ce que", "Pouvez-vous me dire"],
    "remerciement": ["Merci", "Je vous remercie"]
}

# Fonction pour traiter les entrées de l'utilisateur
def process_input(user_input):
    user_input = user_input.lower()
    for intent, keywords in intents.items():
        for keyword in keywords:
            if keyword in user_input:
                return intent
    return "default"

# Fonction pour générer des réponses
def generate_response(intent, user_input):
    if intent == "demande_info":
        return "Je vais vous fournir les informations que vous cherchez !"
    elif intent == "pose_question":
        return "Je vais essayer de répondre à votre question !"
    elif intent == "remerciement":
        return "De rien ! 😊"
    else:
        return responses["default"]

# Ajouter le même CSS que l'accueil
def add_custom_css():
    st.markdown(
        """
        <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f0f6fc;
            color: #1b3b6f;
        }
        .header-title {
            text-align: center;
            font-size: 50px;
            font-weight: bold;
            color: #ffffff;
            padding: 20px;
            background: linear-gradient(135deg, #87CEEB, #00BFFF);
            border-radius: 12px;
        }
        .stSidebar {
            background-color: #87CEEB !important;
            padding: 20px;
            border-radius: 10px;
        }
        .footer {
            text-align: center;
            color: white;
            font-size: 14px;
            padding: 15px;
            margin-top: 30px;
            background: linear-gradient(135deg, #87CEEB, #00BFFF);
            border-radius: 10px;
        }
        </style>
        """, unsafe_allow_html=True
    )

# Appliquer le CSS
add_custom_css()

# Barre latérale avec le sticker
st.sidebar.markdown("<div class='stSidebar'>", unsafe_allow_html=True)
st.sidebar.image("C:/Users/arlys/OneDrive/Desktop/m2 data_science/Edu_chat/pages/sticker.png", use_container_width=True)
st.sidebar.markdown("</div>", unsafe_allow_html=True)

# Titre de la page
st.markdown("<div class='header-title'>💬 Edu Chat - Chatbot</div>", unsafe_allow_html=True)

# Interface utilisateur
if "messages" not in st.session_state:
    st.session_state.messages = []

# Afficher les messages précédents
for message in st.session_state.messages:
    st.chat_message(message["role"]).markdown(message["content"])

# Zone de saisie de l'utilisateur
user_input = st.text_input("Entrez votre question :", "")

if user_input:
    # Traiter l'entrée de l'utilisateur
    intent = process_input(user_input)
    
    # Générer une réponse
    response = generate_response(intent, user_input)
    
    # Ajouter le message de l'utilisateur
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Ajouter la réponse du chatbot
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Afficher la réponse
    st.chat_message("assistant").markdown(response)