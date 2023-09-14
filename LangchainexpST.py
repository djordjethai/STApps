import streamlit as st
import os
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.schema.output_parser import StrOutputParser
from langchain import PromptTemplate
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from operator import itemgetter
import sys
from mojafunkcja import st_style, init_cond_llm

st_style()


def main():
    st.subheader("Recursive Criticism Chain")
    model, temp = init_cond_llm()
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    chat_model = ChatOpenAI(
        model=model,
        temperature=temp
    )

    # RCA Chain
    if "final_result" not in st.session_state:
        st.session_state.final_result = None
    if "initial_question" not in st.session_state:
        st.session_state.initial_question = ""
    if "explanation" not in st.session_state:
        st.session_state.explanation = ""
    template_i = "You are a helpful assistant that imparts wisdom and guides people with accurate answers."
    system_message_prompt = SystemMessagePromptTemplate.from_template(
        template_i)

    # Initial Question Chain
    human_template_i = "{question}"
    human_message_prompt_i = HumanMessagePromptTemplate.from_template(
        human_template_i)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt_i])
    chain1 = chat_prompt | chat_model | StrOutputParser()
    template_imp = "You are a helpful assistant that reviews answers and critiques based on the original question given and write a new improved final answer."
    system_message_prompt_imp = SystemMessagePromptTemplate.from_template(
        template_imp)
    ph0 = st.empty()
    with ph0.container():
        with st.expander("Objasnjenje", expanded=False):
            st.write(
                """Ideja ove vezbe ja da pokaze kako model moze sam sebe da ispravlja ali i da prima ljudske inpute.
                Na primer, pitanje: Roger has 5 tennis balls. He buys 2 more cans of tennis balls. Each can has 3 tennis balls. 
                How many tennis balls does he have now? Cesto daje pogresan odgovor, ali ako mu se da objasnjenje zasto je odgovor pogresan, 
                ili dodatna uputstva kao sto je da svaka limenka im 3 loptice, on ce se korigovati. Mozete mu postavljati podpitanja i dodatne 
                instrukcije u nedogled, dok ne budete zadovoljni odgovorom. Kao i uvek, moete podesavati model i temperaturu...""")

    ph1 = st.empty()
    ph2 = st.empty()
    ph3 = st.empty()
    ph4 = st.empty()
    ph5 = st.empty()

    with ph1.container():
        initial_question = st.text_input("Enter your question: ")
    if initial_question:
        # intervenisem sa Human objasnjenjem pre trece faze
        initial_answer = chain1.invoke({"question": initial_question})
        with ph3.container():
            st.write("Initial answer: ")
            st.info(initial_answer)
        # Critique Chain
        template_c = "You are a helpful assistant that looks at answers and finds what is wrong with them based on the original question given."
        system_message_prompt_c = SystemMessagePromptTemplate.from_template(
            template_c)
        human_template_c = "### Question:\n\n{question}\n\n ###Answer Given:{initial_answer}\n\n Review your previous answer and find problems with your answer"
        human_message_prompt = HumanMessagePromptTemplate.from_template(
            human_template_c)
        rc_prompt = ChatPromptTemplate.from_messages(
            [system_message_prompt, human_message_prompt])

        chain2 = rc_prompt | chat_model | StrOutputParser()

        # "rucno" vezivanje
        constructive_criticism = chain2.invoke(
            {"question": initial_question, "initial_answer": initial_answer})
        with ph4.container():
            st.write("Critique: ")
            st.info(constructive_criticism)

        # Improvement Chain
    st.session_state.explanation = ""
    # napraviti kao clarification (dodao sam koliko lopti ima u svakoj limenci)
    if st.session_state.final_result:
        initial_answer = st.session_state.final_result
    with ph5.form(key='my_form', clear_on_submit=True):
        st.session_state.explanation = st.text_input(
            "Please explain misisng data, or give additional instructions: ")
        submit_button = st.form_submit_button(label='Submit')

        if submit_button:
            if st.session_state.explanation:
                expalanation = st.session_state.explanation
                # if explanation == "exit":
                #     sys.exit()

                human_template_imp = "### Question:\n\n{question}\n\n ###Answer Given:{initial_answer}\n\n \
                        ###Constructive Criticism:{constructive_criticism}\n\n Based on the problems you found, improve your answer given that {explanation}.\n\n### Final Answer:"
                human_message_prompt_imp = HumanMessagePromptTemplate.from_template(
                    human_template_imp)
                improvement_prompt = ChatPromptTemplate.from_messages(
                    [system_message_prompt_imp, human_message_prompt_imp])

                chain3 = improvement_prompt | chat_model | StrOutputParser()

                # sa itemgetter funkcijom se uzima vrednost iz recnika
                if st.session_state.explanation:
                    explanation = st.session_state.explanation
                st.session_state.final_result = chain3.invoke({"question": itemgetter("question"),
                                                               "initial_answer": chain1,
                                                               "explanation": explanation,
                                                               "constructive_criticism": constructive_criticism})
                with ph2.container():
                    st.write("Final Result: ")
                    st.success(st.session_state.final_result)


if __name__ == "__main__":
    main()


