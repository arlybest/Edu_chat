import os
import logging
import streamlit as st
from pinecone import Pinecone
from langchain.vectorstores import Pinecone as PineconeLangChain
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

st.set_page_config(page_title="Edu_Chat", layout="wide")

# 🔹 Configuration des logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 🔹 Clés API
PINECONE_API_KEY = "pcsk_53U2S4_H35UkcZBx97Wr6JgdNpjhb6yKHEhr8XHDUFTwUtyQbjHk5AYxmSEPLBf9VHBNzC"
GOOGLE_API_KEY = "AIzaSyAzPkQdUlVtp3iqre6lxMACoPUQNFKlYJg"

# 🔹 Initialisation de Pinecone
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
pc = Pinecone(api_key=PINECONE_API_KEY)

# 🔹 Création de l'index Pinecone
INDEX_NAME = "pdf-documents-index-v2"
if INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(name=INDEX_NAME, dimension=1536, metric="cosine")

# 🔹 Initialisation du modèle d'embeddings
embedding_model = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-large")

# 🔹 Chargement de Pinecone via LangChain
vectorstore = PineconeLangChain.from_existing_index(index_name=INDEX_NAME, embedding=embedding_model)

# 🔹 Initialisation du modèle LLM (Gemini)
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.5,
    max_tokens=None,
    max_retries=2
)

# 🔹 Prompt pour guider les réponses
prompt_template = PromptTemplate(
    input_variables=["context", "question", "history"],
    template="""
    Utilise uniquement les informations suivantes tirées des documents pour répondre à la question de l'utilisateur. Ne fais pas d'hypothèses ou ne réponds pas en dehors du contexte des documents.

    Contexte :
    {context}

    Historique de la conversation :
    {history}

    Question :
    {question}

    Réponse :
    """
)

# 🔹 Configuration du système de récupération des informations
retriever = vectorstore.as_retriever(search_kwargs={"k": 10})
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True
)

# 🔹 Gestion du contexte de conversation
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

def answer_question(question: str) -> str:
    """
    Recherche des documents pertinents et génère une réponse avec Gemini.
    """
    try:
        logging.info("🔍 Recherche et génération de réponse...")

        # Historique sous forme de texte
        history = "\n".join(st.session_state.conversation_history)

        # Ajouter l'espace réservé pour le spinner devant l'icône du bot
        placeholder = st.empty()  # Placeholder réservé pour le spinner

        with placeholder:
            with st.spinner('Je réfléchis...'):
                # Génération de la réponse
                result = qa_chain({"query": question, "history": history})
                response = result["result"]
                sources = result.get("source_documents", [])

        # Mise à jour de l'historique de conversation
        st.session_state.conversation_history.append(f"Question: {question}")
        st.session_state.conversation_history.append(f"Réponse: {response}")

        # Log des sources
        if sources:
            logging.info(f"📜 Sources utilisées : {[doc.page_content[:300] for doc in sources]}")
        else:
            logging.info("⚠️ Aucun document source trouvé.")

        # Remplacer le spinner par la réponse générée
        placeholder.empty()  # Vide le placeholder pour remplacer le spinner
        return response.strip() if response.strip() else "Désolé, aucune réponse pertinente n'a été trouvée."

    except Exception as e:
        logging.error(f"❌ Erreur : {e}")
        return "Une erreur s'est produite. Veuillez réessayer."

# 📌 Customisation du design (sans toucher au front-end original)
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
        .chat-message {
            display: flex;
            align-items: center;
            padding: 5px;
        }
        .bot-avatar {
            width: 30px;
            height: 30px;
            border-radius: 50%;
            background-color: #1b3b6f;
            margin-right: 10px;
            display: inline-block; /* Juste pour s'assurer qu'il est inline */
        }
        .bot-avatar img {
            width: 100%;
            height: 100%;
            border-radius: 50%;
            object-fit: cover;
        }
        </style>
        """, unsafe_allow_html=True
    )

add_custom_css()

st.sidebar.markdown("<div class='stSidebar'>", unsafe_allow_html=True)
st.sidebar.image("pages/sticker.png", use_container_width=True)
st.sidebar.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='header-title'>💬 Edu Chat - Chatbot</div>", unsafe_allow_html=True)

# 📌 Démarrer la conversation sans message d'initiation du bot
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage des messages existants
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        # Ajouter l'avatar du bot pour chaque message
        if message["role"] == "assistant":
            st.markdown(f'<div class="chat-message"><div class="bot-avatar"></div><span>{message["content"]}</span></div>', unsafe_allow_html=True)
        else:
            st.markdown(message["content"])

# 📌 Interaction avec l'utilisateur via `st.chat_message`
def on_new_message(message):
    if message:
        # Ajouter la question de l'utilisateur à l'historique
        st.session_state.messages.append({"role": "user", "content": message})
        
        # Générer la réponse avec le modèle
        response = answer_question(message)

        # Ajouter la réponse à l'historique
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Réafficher la conversation
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                # Ajouter l'avatar du bot pour chaque message
                if message["role"] == "assistant":
                    st.markdown(f'<div class="chat-message"><div class="bot-avatar"></div><span>{message["content"]}</span></div>', unsafe_allow_html=True)
                else:
                    st.markdown(message["content"])

# 📌 Placeholder dans la boîte de chat
message = st.chat_input("Écrire à Educhat")  # Placeholder changé ici

if message:
    on_new_message(message)
