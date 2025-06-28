# qa_chain/query_resume.py

from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
import google.generativeai as genai
import os

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load Gemini model (globally once)
model = genai.GenerativeModel("gemini-2.0-flash-lite")


def ask_gemini(question: str, context: str) -> str:
    """
    Uses Gemini Pro to answer the question based on resume context.
    """
    prompt = f"""
You are an AI Career Coach.

Based on the following resume context:

------------------------
{context}
------------------------

Answer the question: "{question}"
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Gemini API error: {str(e)}"


def load_qa_chain():
    """
    Loads the FAISS index and uses Gemini to generate answers based on semantic search context.
    """
    # Load local sentence embeddings (same as ingestion)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # Load previously stored vector index
    vectorstore = FAISS.load_local("data/resume_index", embeddings, allow_dangerous_deserialization=True)

    def run_query(user_question: str) -> str:
        # Retrieve top 3 similar chunks
        docs = vectorstore.similarity_search(user_question, k=3)
        context = "\n\n".join(doc.page_content for doc in docs)

        # Use Gemini to answer using the context
        return ask_gemini(user_question, context)

    return run_query
