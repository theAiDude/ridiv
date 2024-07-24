from fastapi import FastAPI, UploadFile, File
from helping import read_pdf, db_creation, db_search, ai_reponse
from model import llm , tokenizer
app = FastAPI()


@app.post("/upload")
async def save_pdf(file: UploadFile = File(...)):
    pdf_path = "document.pdf"
    with open(pdf_path, "wb") as f:
        data = file.read()
        f.write(await data)

    # creating db
    text = read_pdf("document.pdf")
    db_creation("document.pdf", pdf_text=text, tokenizer=tokenizer)


# vector search & getting llm response
@app.post("/chat")
def user_query(question  : str):
    sim_docs = db_search(user_question=question,tokenizer = tokenizer)
    ai_output = ai_reponse(sim_docs, question,llm = llm)
    return ai_output["output_text"]





