import os
from re import search
from pandas import DataFrame, concat
from langsmith import Client
from datetime import datetime, timedelta
import streamlit as st
from mojafunkcja import st_style

os.environ["LANGCHAIN_ENDPOINT"] = "https://api.langchain.plus"
os.environ.get("LANGCHAIN_API_KEY")

st_style()

def main():
    client = Client()
    
    st.subheader("**:rainbow[App za izvlačenje info sa LangSmith sajta]**")

    langsmith_projects = {
        "Zapisnik": "Zapisnik",
        "Stil": "Stil",
        "Chatbot": "Multi Tool Chatbot",
        }
    
    outer_col_1, _, outer_col_3 = st.columns([3, 1, 2])
    inner_col_11, inner_col_12 = outer_col_1.columns([5, 4])
    options = list(langsmith_projects.keys())

    selected_project = inner_col_11.selectbox(
        label="Select a project", label_visibility="hidden", placeholder="Odaberite app", options=options, index=None)
    
    score_name = inner_col_12.text_input(
        label="Score name", label_visibility="hidden", placeholder="Naziv skora")
    
    how_many_days = outer_col_3.slider(
        label="Koliko dana unazad uzeti u obzir", label_visibility="visible", min_value=1, max_value=30, step=1)
    
    help_box_text = "Ovde se mogu uneti instrukcije oko rada aplikacije, " \
        "ili neki drugi tekst koji bi imao smisla..."
    
    outer_col_3.text_area(label="Blok za help", label_visibility="collapsed", disabled=True, height=200,
                          placeholder=help_box_text)
    
    with outer_col_1:
        if selected_project:
            score_name = "ocena" if score_name == "" else score_name
            project_name = langsmith_projects[selected_project]

            if st.button("Start 🚀"):
                status = st.empty()
                status.text("Samo sek... 🌌")

                runs = list(client.list_runs(project_name=project_name, start_time=datetime.now() - timedelta(days=how_many_days)))

                search_func = lambda some_text: search(r"'model_name': '([^']+)', 'temperature': ([^,]+)", some_text)

                feedback_data = []
                input_output_data = []
                access_next_mrdc_z = False
                access_next_coai_s = False
                access_next_coai_c = False

                runs.sort(key=lambda run: run.start_time, reverse=True)
                double_check = True

                for run in runs:
                    feedback_stats = run.feedback_stats
                    run_name = run.name
                    run_start_time = run.start_time.strftime("%y/%m/%d - %H:%M")
                    run_inputs = run.inputs
                    run_outputs = run.outputs

                    if (run_name in ["LLMChain", "AgentExecutor"] and 
                        feedback_stats != None and 
                        score_name in feedback_stats and 
                        not access_next_mrdc_z and
                        not access_next_coai_s and
                        not access_next_coai_c):

                        feedbacks = list(client.list_feedback(run_ids=[run.id]))

                        desired_feedback = [feedback for feedback in feedbacks if feedback.key == score_name][0]
                        
                        if desired_feedback:
                            feedback_dict = {
                                "time fb": run_start_time,
                                f"{score_name}": feedback_stats[score_name]["avg"],
                                "komentar": desired_feedback.comment,
                                }
                            feedback_data.append(feedback_dict)
                            
                            if run_name == "AgentExecutor":
                                prefix = "Always answer in the Serbian language.\n\n"
                                input_output_dict = {
                                    "model": "model",
                                    "temp": "temp",
                                    "pitanje": run_inputs["input"][len(prefix):],
                                    "odgovor": run_outputs["output"],
                                    }
                                
                            if project_name == langsmith_projects["Zapisnik"]:
                                access_next_mrdc_z = True
                            elif project_name == langsmith_projects["Stil"]:
                                access_next_coai_s = True
                            elif project_name == langsmith_projects["Chatbot"]:
                                access_next_coai_c = True
                        else:
                            double_check = False

                    elif run_name == "MapReduceDocumentsChain" and access_next_mrdc_z and run_outputs != None:
                        match = search_func(str(client._load_child_runs(client.read_run(run.id))))
                        
                        input_output_dict = {
                            "model": match.group(1),
                            "temp": match.group(2),
                            "time io": run_start_time,
                            "pocetni prompt": run_inputs["opis"],
                            "finalni prompt": run_inputs["opis_kraj"],
                            "sazetak": run_outputs["output_text"],
                            }
                        input_output_data.append(input_output_dict)
                        access_next_mrdc_z = False

                    elif run_name == "ChatOpenAI" and access_next_coai_s and run_outputs != None:
                        run_extra_invoc_params = run.extra["invocation_params"]
                        input_output_dict = {
                            "model": run_extra_invoc_params["model_name"],
                            "temp": run_extra_invoc_params["temperature"],
                            "time io": run_start_time,
                            "prompt": run_inputs['messages'][1]['kwargs']['content'],
                            "odgovor": run_outputs["generations"][0]["text"],
                            }
                        input_output_data.append(input_output_dict)
                        access_next_coai_s = False

                    elif run_name == "ChatOpenAI" and access_next_coai_c and run_outputs != None:
                        match = search_func(str(run))
                        input_output_dict["model"] = match.group(1)
                        input_output_dict["temp"] = match.group(2)
                        input_output_data.append(input_output_dict)
                        access_next_coai_c = False

                if not feedback_data:
                    st.write("Skor koji ste odabrali nije pronađen na LangSmith-u.")
                    if not double_check:
                        st.write(":rainbow[DOUBLE CHECK FAILED] - msg: 'feedback sa skorom nije pronadjen unutar for-a!'")
                else:
                    status.text("Target in sight... 🪐")
                    df = concat([DataFrame(feedback_data), DataFrame(input_output_data)], axis=1)

                    df = df[~df["komentar"].str.contains("TEST", na=False)]
                    df["komentar"] = df["komentar"].fillna("Nije dat feedback")

                    csv = df.to_csv(index=False).encode(encoding='utf-8-sig')
                    status.text("Target reached! 🏝️")
                    if st.download_button(
                        label="Download as CSV",
                        data=csv,
                        file_name=f'{project_name} - info.csv',
                        mime='text/csv',):
                        pass
        
if __name__ == "__main__":
    main()
