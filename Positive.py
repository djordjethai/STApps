import streamlit as st
from mojafunkcja import st_style, positive_login


st.set_page_config(
    page_title="Positive App's",
    page_icon="🦾",
    layout="wide"
)
st_style()


def main():
    name = st.session_state.get('name')
    email = st.session_state.get('email')
    access_level = st.session_state.get('access_level')

    st.title("Welcome to Positive App's")
    st.info(
        f'Your username is {name}, the email is {email} and access level is {access_level}.')
    st.caption("""
               Sa leve strane možete da birate aplikacije. Skrolujte po potrebi da vidite sve aplikacije.\n
               Za većinu aplikacija možete da birate jezički model i temperaturu.
               """)
    st.divider()
    st.caption("""
               Aplikacije su snabdevene različitim alatima.\n
               Na primer, za **MP3 to Text** koristimo *OpenAI* audio model - *Whisper*,\n
               za *Koder* koristimo Pinecone indeks naučen sa sajtova *LangChain* i *Streamlit*,\n
               za *Pisi u stilu* koristimo Pinecone naučen stilovima različitih osoba,\n
               *Multi Tool Chatbot* ima pristup internetu i koristi podatke iz Pinecone indeksa.\n
               *Zapisnik* generiše zapisnike ili sumarizacije na osnovu transkripta audio fajla.
               """)
    st.sidebar.success("Select an App above.")


name, authentication_status, username = positive_login(main, "03.08.23")


