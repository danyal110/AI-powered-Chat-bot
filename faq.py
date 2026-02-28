import pandas as pd
import numpy as np
import chromadb
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv
import os
load_dotenv()


client=chromadb.Client()
path=Path(__file__).parent /"faq_data.csv"
collection_name="faqs"
def ingest_faq_data(faq_path):

    if collection_name not in [c.name for c in client.list_collections()]:
        df=pd.read_csv(faq_path)
        collections=client.create_collection(
            name=collection_name
        )
        docs=df["question"].to_list()
        metadata=[{"answer":ans} for ans in df["answer"].to_list()]
        ids=[f"id_{i}" for i in range(len(docs))]

        collections.add(
            documents=docs,
            metadatas=metadata,
            ids=ids,
        )
        print("Faq data successfully ingested in Chromdb")
    else:
        print("Collection already exists")

def get_relevant_qa(query):
    collection=client.get_collection(collection_name)
    result=collection.query(
        query_texts=[query],
        n_results=2
    )
    return result

def faq_chain(query):
    ingest_faq_data(path)
    result=get_relevant_qa(query)
    context=""
    for r in result["metadatas"][0]:
        context+=(r.get("answer"))
    prompt=f'''Given the question and context below, generate answer based on context only.
    If you don't find the answer just say "I don't know".
    Do not make things up.
    
    Provide answer in right context.
    
    Question:
    {query}
    
    Context:
    {context}
    '''
    groq=Groq()
    chat = groq.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content":prompt,
            }
        ],
        model=os.environ["GROQ_MODEL"],
    )

    return chat.choices[0].message.content

if __name__=="__main__":
    ingest_faq_data(path)
    query="What is your return policy"

    #res=get_relevant_qa(query)
    print(faq_chain(query))
    #context =" ".join([r.get("answer") for r in res["metadatas"][0]])
    #print(context)

