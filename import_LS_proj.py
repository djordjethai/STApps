import os
from re import search
from langsmith import Client
from datetime import datetime, timedelta
import streamlit as st
from mojafunkcja import st_style

os.environ["LANGCHAIN_ENDPOINT"] = "https://api.langchain.plus"
os.environ.get("LANGCHAIN_API_KEY")

st_style()

def main():
    client = Client()

    st.subheader("Odaberite projekat za koji bi da izvucete info")
    col1, col2, col3 = st.columns(3)

    ls_projects = {
        "Zapisnik": "Zapisnik",
        "Stil": "Stil",
        "Chatbot": "Multi Tool Chatbot",
        }
    selected_project = col1.selectbox('Odaberite projekat:', list(ls_projects.keys()))
    how_many_days = col2.slider('Koliko dana unazad uzeti u obzir:', min_value=1, max_value=30, step=1)
    score_name = col3.text_input(label="Naziv score-a", help="default je 'ocena'")

    score_name = "ocena" if score_name == "" else score_name
    project_name = ls_projects[selected_project]

    if st.button("Start 🚀"):
        status = st.empty()
        status.text("Samo sek... 🌌")

        runs = list(client.list_runs(project_name=project_name, start_time=datetime.now() - timedelta(days=how_many_days)))

        search_func = lambda some_text: search(r"'model_name': '([^']+)', 'temperature': ([^,]+)", some_text)

        feedback_data = []
        access_next_mrdc = False
        access_next_coai_s = False
        access_next_coai_c = False

        runs.sort(key=lambda run: run.start_time, reverse=True)

        for run in runs:
            x = False
            feedback_stats = run.feedback_stats
            run_name = run.name
            run_start_time = run.start_time.strftime("%y/%m/%d - %H:%M")
            run_inputs = run.inputs
            run_outputs = run.outputs

            if (run_name in ["LLMChain", "AgentExecutor"] and 
                feedback_stats != None and 
                score_name in feedback_stats and 
                not access_next_mrdc and
                not access_next_coai_s and
                not access_next_coai_c):

                x = True
                feedback = list(client.list_feedback(run_ids=[run.id]))[-1]

                feedback_dict = {
                    "time": run_start_time,
                    f"{score_name}": feedback_stats[score_name]["avg"],
                    "komentar": feedback.comment,
                    }
                
                if run_name == "AgentExecutor":
                    prefix = "Always answer in the Serbian language.\n\n"
                    input_output_dict = {
                        "model": "model",
                        "temp": "temp",
                        "prompt": run_inputs["input"][len(prefix):],
                        "odgovor": run_outputs["output"],
                        }
                    
                if project_name == ls_projects["Zapisnik"]:
                    access_next_mrdc = True
                elif project_name == ls_projects["Stil"]:
                    access_next_coai_s = True
                elif project_name == ls_projects["Chatbot"]:
                    access_next_coai_c = True

            elif run_name == "MapReduceDocumentsChain" and access_next_mrdc and run_outputs != None:
                match = search_func(str(client._load_child_runs(client.read_run(run.id))))
                
                input_output_dict = {
                    "model": match.group(1),
                    "temp": match.group(2),
                    "pocetni prompt": run_inputs["opis"],
                    "finalni prompt": run_inputs["opis_kraj"],
                    "sazetak": run_outputs["output_text"],
                    }
                feedback_dict.update(input_output_dict)
                access_next_mrdc = False

            elif run_name == "ChatOpenAI" and access_next_coai_s and run_outputs != None:
                run_extra_invoc_params = run.extra["invocation_params"]
                input_output_dict = {
                    "model": run_extra_invoc_params["model_name"],
                    "temp": run_extra_invoc_params["temperature"],
                    "prompt": run_inputs['messages'][1]['kwargs']['content'],
                    "odgovor": run_outputs["generations"][0]["text"],
                    }
                feedback_dict.update(input_output_dict)
                access_next_coai_s = False

            elif run_name == "ChatOpenAI" and access_next_coai_c and run_outputs != None:
                match = search_func(str(run))
                input_output_dict["model"] = match.group(1)
                input_output_dict["temp"] = match.group(2)
                feedback_dict.update(input_output_dict)
                access_next_coai_c = False

            if x:
                feedback_data.append(feedback_dict)

        status.text("Target in sight... 🪐")
        if project_name == ls_projects["Zapisnik"]:
            input_1 = "pocetni prompt"
            input_2 = "finalni prompt"
            output = "sazetak"
        else:
            input_1 = "prompt"
            output = "odgovor"

        cwd = os.getcwd()
        with open(os.path.join(cwd, f"{project_name} - svi komentari.txt", 'w')) as all_inputs_file:
            for d in feedback_data:
                with open(os.path.join(cwd, f"{project_name} {d['time']}.txt", 'w')) as individual_file:
                    individual_file.write(f"model: {d['model']}")
                    individual_file.write(f"\ttemp: {d['temp']}\n\n")
                    individual_file.write(f"INPUT:\n {d[input_1]}\n\n")

                    if project_name == ls_projects["Zapisnik"]:
                        individual_file.write(f"INPUT:\n {d[input_2]}\n\n")
                    individual_file.write(f"\nOUTPUT:\n {d[output]}")
                
                all_inputs_file.write(f"ocena: {d[score_name]}\nkomentar: {d['komentar']}\n\n\n")

        status.text("Target reached! 🏝️ - pogledaj cd")
        
if __name__ == "__main__":
    main()
