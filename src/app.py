import streamlit as st
import time

st.set_page_config(
    page_title="Deep-privacy",
    page_icon="🔒",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.title("Deep Privacy")
st.text("Create privacy reports for online tools.")

with st.expander("API Key Settings"):
    with st.form("api_key_form"):
        key = st.text_input("OpenAI API Key", placeholder="sk-...", type="password")
        if st.form_submit_button("Save"):
            st.session_state["openai_key"] = key


tool = st.text_input("Online tool name", placeholder="Jira, Notion, etc.")

if st.button("Generate report"):
    with st.spinner("Generating report..."):
        time.sleep(3)
        st.write("Report generated")
