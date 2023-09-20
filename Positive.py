import streamlit as st
from mojafunkcja import st_style, positive_login


st.set_page_config(
    page_title="Positive App's",
    page_icon="👋",
    layout="wide"
)
st_style()


def main():
    name = st.session_state.get('name')
    email = st.session_state.get('email')
    access_level = st.session_state.get('access_level')

    st.title("Welcome to Positive App's")
    st.info(
        f'Your username is {name} and email is {email} and access level is {access_level}.')
    st.caption(
        """**Sa leve strane možete da birate aplikacije. Skrolujte po potrebi da vidite sve aplikacije.
        Za većinu aplikacija mozete da birate jezički model i temperaturu.**""")
    st.divider()
    st.caption("""
               Aplikacije su snabdevene razlicitim alatima. 
               Na primer, za MP3 to TXT koristimo OpenAI Audio model - Whisper,
               za Koder koristimo Pinecone index naucen sa sajtova LangChain i Streamlit,
               za Pisi u stilu koristimo Pinecone naucen stilovima razlicitih osoba,
               Multi Tool Chatbot ima pristup internetu i koristi podatke iz Pinecone indeksa.
               App Zapisnik kreira zapisnike ili sumarizacije na osnovu transkripta audio fajla.
               """)
    st.sidebar.success("Select an App above.")


name, authentication_status, username = positive_login(main, "03.08.23")


