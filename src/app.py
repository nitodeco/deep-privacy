import streamlit as st

from agent import generate_privacy_report

st.set_page_config(
    page_title="Deep Privacy",
    page_icon="🔒",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.title("Deep Privacy")
st.text("Create privacy reports for online services.")


service = st.text_input("Service name", placeholder="Spotify, Notion, etc.")

if st.button("Generate report"):
    with st.spinner("Generating report..."):
        report = generate_privacy_report(service)
        st.write(report)
