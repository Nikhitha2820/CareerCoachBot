# resume_parser/ingest_resume.py

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
import os

def ingest_resume(file_path: str) -> None:
    """
    Ingests a resume PDF, splits it into text chunks, embeds them using HuggingFace embeddings,
    and stores the embeddings in a local FAISS vector database for semantic search.

    Args:
        file_path (str): The file path to the resume PDF to be ingested.

    Returns:
        None
    """
    # Step 1: Load and extract text from resume PDF
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    # Step 2: Split the text into overlapping chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)

    # Step 3: Initialize HuggingFace embeddings (runs locally)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # Step 4: Create FAISS vector store from chunks
    vectorstore = FAISS.from_documents(chunks, embeddings)

    # Step 5: Save the vector DB locally
    vectorstore.save_local("data/resume_index")
    print("✅ Resume embedded and saved to FAISS index (using HuggingFace).")
