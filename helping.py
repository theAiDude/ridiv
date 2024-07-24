from langchain_community.vectorstores import FAISS

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
import PyPDF2

# loading the api key
load_dotenv()

key = os.getenv("GOOGLE_API")


# Function to extract content from the  pdf file
def read_pdf(file_name):
    reader = PyPDF2.PdfReader(file_name)
    # total pages
    num_pages = len(reader.pages)

    # pdf - content
    raw_text = ""

    for page_num in range(num_pages):
        page = reader.pages[page_num]
        text = page.extract_text()

        raw_text = raw_text + " " + text
    return raw_text


# function for creating documents : split text into multiple documents
def db_creation( pdf_text, tokenizer):
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    docs = splitter.create_documents([pdf_text])

    # vector db
    db = FAISS.from_documents(documents=docs, embedding=tokenizer)
    db.save_local("Vector_db")


# function to perform vector search
def db_search(user_question: str, tokenizer):
    # load the vector db
    db = FAISS.load_local("Vector_db", embeddings=tokenizer, allow_dangerous_deserialization=True)
    # similarity search
    similar_docs = db.similarity_search(user_question)
    return similar_docs


# function to get the LLm response
def ai_reponse(docs, question, llm):
    template = '''
        You are a great ai assistant, provide answers to the user question based on the context provided.
        Question:{user_question}
        Context:{context}
        '''
    # prompt
    prompt = PromptTemplate(input_variables=["question"], template=template)
    # chaining
    chain = load_qa_chain(llm=llm, prompt=prompt)
    ai = chain.invoke({"input_documents": docs, "user_question": question})

    return ai
