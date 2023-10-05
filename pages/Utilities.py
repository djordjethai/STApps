import streamlit as st
from mojafunkcja import st_style, positive_login, pinecone_stats


st.set_page_config(
    page_title="Positive Utilities",
    page_icon="👉",
    layout="wide"
)
st_style()


def main():
    def intro():
        st.subheader("Dobrodošli na uslužne aplikacije 🚙")
        st.caption("Sa leve strane možete da birate aplikacije.")
        st.divider()
        st.caption("""
                   Scraper čita web sajtove i smešta podatke u Pinecone Indeks\n
                   Positive ubacuje cele dokumente u Pinecone Indeks\n
                   Pinecone Dokumenti priprema dokument i indeksira ih u Pincone Indeks\n
                   Utilities održava Pinecone Indeks\n
                   Stats prikazuje statistiku Pinecone Indeksa\n
                   New Login otvara novog korsinika\n
                   Change Login menja ime korisnika\n
                   Import LangSmith projects izvlacu sve bitne info sa LangSmith-a na lokal
                   """)

        st.sidebar.success("Odaberite uslugu iz padajuće liste.")

    def pinecone_scraping():
        import Pinecone_Scraper
        Pinecone_Scraper.main()

    def pinecone_utilities():
        import Pinecone_Utility
        Pinecone_Utility.main()

    def pcone_stats():
        from mojafunkcja import pinecone_stats
        import pinecone
        index = pinecone.Index('embedings1')
        pinecone_stats(index)

    def pisi_positive():
        import selfquerypositive
        selfquerypositive.main()

    def new_login_name():
        import newlogin
        newlogin.main()

    def change_login_name():
        import changelogin
        changelogin.main()

    def pcone_docs():
        import Priprema
        Priprema.main()

    def positive_scraping():
        import Positive_Scraper
        Positive_Scraper.main()

    def import_langsmith_proj():
        import import_LS_proj
        import_LS_proj.main()

    page_names_to_funcs = {
        "Utilities Home": intro,
        "Pinecone Scraping": pinecone_scraping,
        "Positive Scraping": positive_scraping,
        "Pinecone Management": pinecone_utilities,
        "Pinecone Dokumenti": pcone_docs,
        "Pinecone Positive": pisi_positive,
        "Pinocone Stats": pcone_stats,
        "New User": new_login_name,
        "Change Password": change_login_name,
        "Import from LangSmith": import_langsmith_proj,
    }

    demo_name = st.sidebar.selectbox("Odaberite aplikaciju", page_names_to_funcs.keys())
    page_names_to_funcs[demo_name]()


name, authentication_status, username = positive_login(main, "16.08.23")


