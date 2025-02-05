import os
import logging
import streamlit as st
from langchain.vectorstores import Pinecone as PineconeLangChain
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from pinecone import Pinecone

# Configuration des logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Clés API
PINECONE_API_KEY = "pcsk_53U2S4_H35UkcZBx97Wr6JgdNpjhb6yKHEhr8XHDUFTwUtyQbjHk5AYxmSEPLBf9VHBNzC"
GOOGLE_API_KEY = "AIzaSyAzPkQdUlVtp3iqre6lxMACoPUQNFKlYJg"

# Initialisation de Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
INDEX_NAME = "pdf-documents-index-v2"

# Vérification de l'index (évite la latence de création)
if INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(name=INDEX_NAME, dimension=1536, metric="cosine")

# Chargement du modèle d'embeddings
embedding_model = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-large")
vectorstore = PineconeLangChain.from_existing_index(index_name=INDEX_NAME, embedding=embedding_model)

# Configuration du modèle LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.7,
    max_tokens=None,
    max_retries=3
)

# Prompt optimisé
prompt_template = PromptTemplate(
    input_variables=["context", "question", "history"],
    template="""
    Tu es un assistant intelligent. Réponds de manière claire et concise.
    
    Contexte :
    {context}
    
    Historique :
    {history}
    
    Question :
    {question}
    
    Réponse :
    """
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=False
)

# Gestion de l'historique
conversation_history = []

def answer_question(question: str) -> str:
    try:
        history = "\n".join(conversation_history)
        result = qa_chain({"query": question, "history": history})
        response = result.get("result", "Je n'ai pas trouvé d'information pertinente.")
        
        if len(conversation_history) > 10:
            conversation_history.pop(0)
        conversation_history.append(f"Q: {question}")
        conversation_history.append(f"R: {response}")
        
        return response.strip()
    except Exception as e:
        logging.error(f"Erreur : {e}")
        return "Une erreur s'est produite. Veuillez réessayer."

# Interface utilisateur améliorée
st.set_page_config(page_title="💬 Edu_Chat", layout="wide")
st.markdown("""
    <h1 style='text-align: center;'>💬 Edu_Chat - Assistant Éducatif</h1>
    <p style='text-align: center; font-size:18px;'>Posez vos questions sur les syllabus 📚</p>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    role = "👤 Utilisateur" if msg["role"] == "user" else "🤖 Edu_Chat"
    with st.chat_message(msg["role"]):
        st.markdown(f"**{role}**: {msg['content']}", unsafe_allow_html=True)

user_input = st.chat_input("Posez votre question ici...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(f"👤 **Vous**: {user_input}", unsafe_allow_html=True)
    
    with st.spinner("✍️ Réflexion en cours..."):
        response = answer_question(user_input)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(f"🤖 **Edu_Chat**: {response}", unsafe_allow_html=True)

# CSS amélioré
st.markdown("""
    <style>
        .stChatMessage { border-radius: 10px; padding: 12px; margin-bottom: 12px; }
        .user-message { background-color: #DCF8C6; border-radius: 12px; padding: 10px; }
        .assistant-message { background-color: #f5f5f5; border-radius: 12px; padding: 10px; }
        .stButton button { background-color: #4CAF50; color: white; font-weight: bold; }
        .stSpinner div { color: #ff9800; }
    </style>
""", unsafe_allow_html=True)
