import streamlit as st
from mojafunkcja import st_style, positive_login


st.set_page_config(
    page_title="Positive App's",
    page_icon="👉",
    layout="wide"
)
st_style()


def main():
    def intro():
        st.subheader("Dobrodošli u :red[**Positive**] :green[**Demo**] aplikacije 💻")
        st.caption("Sa leve strane možete da birate aplikacije.")
        st.divider()
        st.caption("""
                   OpenAI prikazuje upotrebu OpenAI funkcije,\n
                   LangChain Expression Language prikazuje upotrebu te funkcionalnosti.
                   """)
        with st.sidebar:
            st.success("Odaberite Demo iz padajuće liste.")
            st.image(
                "https://test.georgemposi.com/wp-content/uploads/2023/05/positive-logo-red.jpg", width=150)

    def OpenAi_Functions():
        import OpenaifuncST
        st.subheader("OpenAI Funkcije")
        OpenaifuncST.main()

    def LC_Expression_Language():
        import LangchainexpST
        st.subheader("LangChain Expression Language")
        LangchainexpST.main()

    page_names_to_funcs = {
        "Demo Home": intro,
        "OpenAI Functions": OpenAi_Functions,
        "LangChain Expression Language": LC_Expression_Language,
    }

    demo_name = st.sidebar.selectbox("Choose App", page_names_to_funcs.keys())
    page_names_to_funcs[demo_name]()


name, authentication_status, username = positive_login(main, "10.08.23")


