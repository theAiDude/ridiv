
from langchain_google_genai import GoogleGenerativeAI
from langchain_google_genai.embeddings import GoogleGenerativeAIEmbeddings
import os
from dotenv import load_dotenv


# accessing the key
load_dotenv()
h_key = os.getenv("HUGGINGFACE_API")
google_key = os.getenv("GOOGLE_API")

# llm and tokenizer
tokenizer = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=google_key )
llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=google_key)