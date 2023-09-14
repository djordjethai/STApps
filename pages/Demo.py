import streamlit as st
from mojafunkcja import st_style, positive_login


st.set_page_config(
    page_title="Positive App's",
    page_icon="👋",
    layout="wide"
)
st_style()


def main():
    def intro():
        st.subheader("Welcome to Positive Demo App's")
        st.caption("Sa leve strane mozete da birate aplikacije.")
        st.divider()
        # col1, col2 = st.columns(2)

        st.caption("OpenAI prikazuje upotrebu OpenAI funcije")
        st.caption(
            "LangChain Expression Language prikazuje upotrebu te funkcionalnosti")

        with st.sidebar:
            st.image(
                "https://test.georgemposi.com/wp-content/uploads/2023/05/positive-logo-red.jpg", width=150)
            st.success("Select a Demo from a Drop Box.")

    def OpenAi_Functions():
        import OpenaifuncST
        st.subheader("OpenAI Funkcije")
        OpenaifuncST.main()

    def LC_Expression_Language():
        st.subheader("LangChain Expression Language")
        import LangchainexpST
        LangchainexpST.main()

    page_names_to_funcs = {
        "Demo Home": intro,
        "OpenAI Functions": OpenAi_Functions,
        "LangChain Expression Language": LC_Expression_Language,
    }

    demo_name = st.sidebar.selectbox("Choose App", page_names_to_funcs.keys())
    page_names_to_funcs[demo_name]()


name, authentication_status, username = positive_login(main, "10.08.23")


