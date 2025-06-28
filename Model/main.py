# main.py
import streamlit as st
from resume_parser.ingest_resume import ingest_resume
from QA_Bot.query_resume import load_qa_chain
import os
from dotenv import load_dotenv
load_dotenv()


st.title("🧠 AI Career Coach")
st.write("Upload your resume to get personalized career guidance!")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if uploaded_file:
    file_path = f"data/{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success("Resume uploaded successfully!")
    
    if st.button("🔍 Process Resume"):
        ingest_resume(file_path)
        st.success("Resume processed and stored in vector DB!")

# Load the Gemini RAG-based chain
qa_chain = load_qa_chain()

st.markdown("---")
st.subheader("💬 Ask your AI Career Coach (Gemini-powered)")

question = st.text_input("Ask your question about the resume")

if question:
    with st.spinner("Thinking..."):
        response = qa_chain(question)
        st.success(response)

