import streamlit as st
import random

# Définir des réponses automatiques basiques
responses = {
    "bonjour": "Bonjour ! Comment puis-je vous aider aujourd'hui ?",
    "syllabus": "Vous pouvez consulter les syllabus en sélectionnant votre classe et matière.",
    "merci": "Avec plaisir ! 😊",
    "au revoir": "Au revoir ! Bonne journée et bon apprentissage ! 📚",
    "default": "Je ne suis pas sûr de comprendre. Pouvez-vous reformuler ?"
}

def chatbot_response(user_input):
    user_input = user_input.lower()
    return responses.get(user_input, responses["default"])

# Interface utilisateur
st.title("💬 Edu_Chat")
st.write("Posez vos questions sur les  syllabus de cours !")

# Zone de saisie de l'utilisateur
user_input = st.text_input("Entrez votre question :", "")

if user_input:
    response = chatbot_response(user_input)
    st.write("🤖 Chatbot :", response)
