import os
import time
import logging
from datetime import datetime
import streamlit as st
from pinecone import Pinecone
from langchain_community.vectorstores import Pinecone as PineconeLangChain
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough

# --- Page et configuration du logging ---
st.set_page_config(page_title="Edu_Chat", layout="wide")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Clés API et configuration de l'environnement ---
PINECONE_API_KEY = "pcsk_53U2S4_H35UkcZBx97Wr6JgdNpjhb6yKHEhr8XHDUFTwUtyQbjHk5AYxmSEPLBf9VHBNzC"
GOOGLE_API_KEY = "AIzaSyAzPkQdUlVtp3iqre6lxMACoPUQNFKlYJg"
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

# --- Fonctions de mise en cache pour l'initialisation ---
@st.cache_resource
def init_pinecone():
    pc = Pinecone(api_key=PINECONE_API_KEY)
    INDEX_NAME = "pdf-documents-index-v2"
    if INDEX_NAME not in pc.list_indexes().names():
        pc.create_index(name=INDEX_NAME, dimension=1536, metric="cosine")
    return pc, INDEX_NAME

@st.cache_resource
def init_vectorstore(index_name: str):
    embedding_model = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-large")
    vectorstore = PineconeLangChain.from_existing_index(index_name=index_name, embedding=embedding_model)
    return vectorstore

@st.cache_resource
def init_llm():
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        google_api_key=GOOGLE_API_KEY,
        temperature=0.0,  # réponses déterministes
        max_tokens=None,
        max_retries=1
    )
    return llm

@st.cache_resource
def init_prompt():
    return PromptTemplate(
        input_variables=["context", "question", "history"],
        template="""
Utilisez uniquement les informations extraites des documents (issus de manuels scolaires, cours, et autres supports pédagogiques) et l'historique de conversation pour répondre à la question de l'utilisateur bref tout ce qui se trouve dans le document qui pourrait t'aider. Ne faites aucune hypothèse et n'inventez pas de réponse. Si aucune information pertinente n'est trouvée dans le contexte, répondez : "Désolé, aucune information pertinente n'a été trouvée."

Historique :
{history}

Documents pertinents :
{context}

Question :
{question}

Répondez en français avec un style professionnel :
"""
    )

# --- Initialisation des composants ---
pc, INDEX_NAME = init_pinecone()
vectorstore = init_vectorstore(INDEX_NAME)
llm = init_llm()
prompt_template = init_prompt()

# --- Configuration du retriever ---
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# --- Chaîne QA utilisant RunnablePassthrough ---
# La clé "context" est fournie par une fonction lambda qui interroge le retriever avec la question et joint le contenu des documents récupérés.
qa_chain = (
    {
        "context": lambda inputs: "\n".join([doc.page_content for doc in retriever.get_relevant_documents(inputs["question"])]),
        "question": RunnablePassthrough(),
        "history": RunnablePassthrough()
    }
    | prompt_template
    | llm
)

# --- Gestion de l'état de la conversation ---
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Ajout de CSS personnalisé ---
def add_custom_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #f0f6fc;
            color: #1b3b6f;
            font-size: 18px;
        }
        .header-title {
            text-align: center;
            font-size: 40px;
            font-weight: bold;
            color: #ffffff;
            padding: 20px;
            background: linear-gradient(135deg, #87CEEB, #00BFFF);
            border-radius: 12px;
            margin-bottom: 20px;
        }
        .stSidebar {
            background-color: #87CEEB !important;
            padding: 20px;
            border-radius: 10px;
        }
        .footer {
            text-align: center;
            color: white;
            font-size: 16px;
            padding: 15px;
            margin-top: 30px;
            background: linear-gradient(135deg, #87CEEB, #00BFFF);
            border-radius: 10px;
        }
        .chat-message {
            display: flex;
            align-items: flex-start;
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 8px;
            max-width: 80%;
            word-wrap: break-word;
            opacity: 0;
            transform: translateY(10px);
            animation: fadeInUp 0.5s forwards;
        }
        @keyframes fadeInUp {
            to { opacity: 1; transform: translateY(0); }
        }
        .assistant-message {
            background-color: #e8f5ff;
            border: 1px solid #a2d2ff;
            margin-right: auto;
        }
        .user-message {
            margin-left: auto;
            text-align: left;
        }
        .avatar {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            margin-right: 10px;
            flex-shrink: 0;
        }
        .avatar img {
            width: 100%;
            height: 100%;
            border-radius: 50%;
            object-fit: cover;
        }
        .message-content { flex: 1; font-size: 18px; }
        .timestamp {
            font-size: 1rem;
            color: #888;
            margin-top: 5px;
        }
        .loader {
          display: inline-block;
          position: relative;
          width: 80px;
          height: 20px;
        }
        .loader div {
          position: absolute;
          top: 0;
          width: 16px;
          height: 16px;
          border-radius: 50%;
          background: #00BFFF;
          animation-timing-function: cubic-bezier(0, 1, 1, 0);
        }
        .loader div:nth-child(1) { left: 8px; animation: loader1 0.6s infinite; }
        .loader div:nth-child(2) { left: 8px; animation: loader2 0.6s infinite; }
        .loader div:nth-child(3) { left: 32px; animation: loader2 0.6s infinite; }
        .loader div:nth-child(4) { left: 56px; animation: loader1 0.6s infinite; }
        @keyframes loader1 { 0% { transform: scale(0); } 100% { transform: scale(1); } }
        @keyframes loader2 { 0% { transform: translate(0, 0); } 100% { transform: translate(24px, 0); } }
        </style>
        """, unsafe_allow_html=True
    )

add_custom_css()

# --- Sidebar et header ---
st.sidebar.markdown("<div class='stSidebar'>", unsafe_allow_html=True)
st.sidebar.image("pages/sticker.png", use_container_width=True)
st.sidebar.markdown("</div>", unsafe_allow_html=True)
st.markdown("<div class='header-title'>💬 Edu Chat - Chatbot</div>", unsafe_allow_html=True)

# --- Affichage de la conversation ---
def render_messages():
    bot_icon = "https://img.icons8.com/?size=100&id=1RueIplXPGd2&format=png&color=000000"
    user_icon = "https://img.icons8.com/?size=100&id=kDoeg22e5jUY&format=png&color=000000"
    for message in st.session_state.messages:
        timestamp = message.get("timestamp", "")
        time_html = f"<div class='timestamp'>{timestamp}</div>" if timestamp else ""
        if message["role"] == "assistant":
            st.markdown(
                f'''
                <div class="chat-message assistant-message">
                    <div class="avatar"><img src="{bot_icon}" alt="Bot Avatar" /></div>
                    <div class="message-content">{message["content"]}{time_html}</div>
                </div>
                ''', unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'''
                <div class="chat-message user-message">
                    <div class="avatar"><img src="{user_icon}" alt="User Avatar" /></div>
                    <div class="message-content">{message["content"]}{time_html}</div>
                </div>
                ''', unsafe_allow_html=True
            )

# --- Fonction de réponse avec animation et loader ---
def answer_question(question: str) -> str:
    try:
        logging.info("🔍 Recherche et génération de la réponse...")
        history_text = "\n".join(st.session_state.conversation_history)
        loader_html = """
         <div class="loader">
           <div></div><div></div><div></div><div></div>
         </div>
         """
        placeholder = st.empty()
        placeholder.markdown(loader_html, unsafe_allow_html=True)
        
        # Injection de la question et de l'historique dans la chaîne QA
        result = qa_chain.invoke({
            "question": question,
            "history": history_text
        })
        placeholder.empty()
        response = result.content if hasattr(result, "content") else str(result)
        sources = getattr(result, "source_documents", [])
        if sources:
            logging.info(f"📜 Documents utilisés : {[doc.page_content[:300] for doc in sources]}")
        else:
            logging.info("⚠️ Aucun document pertinent trouvé.")
        st.session_state.conversation_history.extend([f"Question: {question}", f"Réponse: {response}"])
        return response.strip() if response.strip() else "Désolé, aucune information pertinente n'a été trouvée."
    except Exception as e:
        logging.error(f"❌ Error: {e}")
        return "Une erreur s'est produite. Veuillez réessayer."

def typewriter_effect(text, delay=0.005):
    placeholder = st.empty()
    displayed_text = ""
    for char in text:
        displayed_text += char
        placeholder.markdown(
            f"<div class='chat-message assistant-message'><div class='message-content'>{displayed_text}</div></div>",
            unsafe_allow_html=True
        )
        time.sleep(delay)
    return displayed_text

def on_new_message(message: str):
    now = datetime.now().strftime("%H:%M:%S")
    st.session_state.messages.append({"role": "user", "content": message, "timestamp": now})
    render_messages()
    response = answer_question(message)
    animated_response = typewriter_effect(response)
    now_bot = datetime.now().strftime("%H:%M:%S")
    st.session_state.messages.append({"role": "assistant", "content": animated_response, "timestamp": now_bot})
    st.rerun()

# --- Affichage de la conversation et gestion de l'input utilisateur ---
render_messages()
user_input = st.chat_input("Écrire à EduChat")
if user_input:
    on_new_message(user_input)
