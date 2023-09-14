import streamlit as st
import time

i = 0
progress_text = "Operation in progress. Please wait."
progress_bar = st.progress(0.0, text=progress_text)
ph = st.empty()
while i < 247:
    i = i+1
    time.sleep(0.1)
    progress_bar.progress(i/247, text=progress_text)

    k = int(i/247*100)
    ph.write(f'{i} of 247 is {k} of 100')


