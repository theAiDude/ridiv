import streamlit as st
from helping import read_pdf, db_creation, db_search, ai_reponse
from model import tokenizer, llm
import time

# main title
st.title("Talk to PDF")

# sidebar
with st.sidebar:
    # file uploader
    file = st.file_uploader("Upload a pdf file.." , type = ["pdf"])  # file uploader

    # if pdf - file is present

    if file is not None:
        st.success("file uploaded")
        # read the pdf content
        text = read_pdf(file)
        # vector bd creation
        db_creation(text, tokenizer=tokenizer)

        if file is not None:
            value = 0

            progress_bar = st.progress(value)

            for progress in range(100):
                time.sleep(0.1)
                value = progress + 1

                if value < 100:
                    progress_text = "Operation in progress..."
                else:
                    progress_text = "Done."

                progress_bar.progress(value,text = f":orange-background[{progress_text}]")

# storing the chat history in the session state
if "history" not in st.session_state:
    st.session_state["history"] = []


# function to clear the previous conversation
def clear_history():
    del st.session_state["history"]



# history clear button
if file is not None:
    clear_btn = st.button("Clear History", on_click=clear_history)

# display previous conversation
for user in st.session_state["history"]:
    # user message
    if user["role"] == "user":
        with st.chat_message("You"):
            st.write(user["message"])
    # ai message
    else:
        with st.chat_message("AI"):
            st.write(user["message"])

# update the chat history with new conversation
if file is not None:
    user_input = st.chat_input("Write you message here...")

    # Execute only when user give some input
    if user_input is not None:
        # update user-message
        st.session_state["history"].append({"role": "user", "message": user_input})

        # vector db search - getting most relevant docs
        matched_docs = db_search(user_question=user_input, tokenizer=tokenizer)

        # getting ai output
        ai_output = ai_reponse(docs=matched_docs, question=user_input, llm=llm)
        # update ai-message
        st.session_state["history"].append({"role": "ai", "message": ai_output["output_text"]})
