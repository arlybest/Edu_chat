import streamlit as st

# Définir le CSS personnalisé
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
            background: linear-gradient(135deg, #007bff, #0056b3);
            border-radius: 12px;
        }
        .feature-box {
            background: #e3f2fd;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            font-size: 18px;
            color: #003366;
            font-weight: bold;
            margin: 10px 0;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
        }
        .footer {
            text-align: center;
            color: white;
            font-size: 14px;
            padding: 15px;
            margin-top: 30px;
            background: linear-gradient(135deg, #007bff, #0056b3);
            border-radius: 10px;
        }
        .emoji {
            text-align: center;
            font-size: 60px;
            margin: 20px 0;
        }
        </style>
        """, unsafe_allow_html=True
    )

# Ajouter le CSS personnalisé
add_custom_css()

# Titre principal
st.markdown("<div class='header-title'>Edu Chat - Assistant Éducatif</div>", unsafe_allow_html=True)

# Emoji éducatif
st.markdown("<div class='emoji'>📚</div>", unsafe_allow_html=True)

# Présentation rapide
st.markdown("### 🤖 Apprendre devient plus simple avec **Edu_Chat** !")

# Fonctionnalités principales sous forme de boîtes
st.markdown("<div class='feature-box'>📖 Accédez aux syllabus</div>", unsafe_allow_html=True)
st.markdown("<div class='feature-box'>💬 Chatbot éducatif</div>", unsafe_allow_html=True)
st.markdown("<div class='feature-box'>🌍 Bilingue (FR/EN)</div>", unsafe_allow_html=True)

# Contact rapide
st.markdown("### 📞 Besoin d'aide ? Contactez-nous !")
st.markdown("✉️ **Email** : arlysimo@gmail.com,ronictakougang@gmail.com")
st.markdown("📞 **Téléphone** : +237 656 109 435,+237693115530")

# Pied de page
st.markdown("<div class='footer'>&copy; 2025 Edu_Chat. Tous droits réservés.</div>", unsafe_allow_html=True)
