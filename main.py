import streamlit as st


from router import router
from faq import faq_chain
from sql import sql_chain,sql_generate,final_answer

def ask(query):
    route=router(query).name
    if route=="faq":
        return faq_chain(query)
    elif route=="sql":
        response=sql_generate(query)
        #return response
        print(response)
        x=final_answer(query,response)
        print(x)
        return x
    else:
        return "Query not recognized."
st.title("E-commerce Chatbot")

query=st.chat_input("Write your query")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

st.session_state["messages"]=[]
if query:
    with st.chat_message("user"):
        st.markdown(query)

    st.session_state["messages"].append({"role":"user","content":query})
    response=ask(query)

    with st.chat_message("assistant"):
        st.markdown(response)

    st.session_state["messages"].append({"role": "assistant", "content":response})