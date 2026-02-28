import sqlite3
import pandas as pd
from groq import Groq
import os
import re
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()
GROQ_MODEL=os.getenv("GROQ_MODEL")
db_path=Path(__file__).parent.parent/"app/db.sqlite"

client_sql=Groq()


def sql_chain(query):
    prompt = f'''
    From the given query generate sql command to retrive all columns from product database.
    Query should be contextually right.
    Database name is product with following columns like brand, price etc
    Brand can be like the given brand and need not be exactly similar.
    Remove any extra messages from the query including extra spaces,any words before select and after;
    
    Also the database schema is given in schema tags.
    <schema>
    table:product
    
    fields:
    product_link:string to provide link to product
    title:string to provide name of product and also contain purpose
    brand:string to provide brand
    price:integer to provide price of product
    discount:float to provide discount of product
    avg_rating:float to provide average rating of product
    total_ratings:integer to provide total rating of product
    
    Make sure to use %like for title,brand.
    Generate conceptually correct sql command.
    Ensure that query begin with SELECT and end with;
    
    The query should have all the fields in SELECT clause(i.e. SELECT *).
    
    Only return sql query which is executable.
    
    Multiply discount by 100.
    


    Brand is for company and title is for name of the product are different
    The query should start with <SQL> and end with </SQL>.
    
    Query: {query}
    '''
    chat = client_sql.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=GROQ_MODEL,
        temperature=0.2,
        max_tokens=1024
    )
    #print(chat.choices[0].message.content)
    return chat.choices[0].message.content

def run_query(query):
    if query.strip().upper().startswith("SELECT"):
        with sqlite3.connect(db_path) as connection:
            df=pd.read_sql_query(query,connection)

            return df

def sql_generate(question):
    sql_query=sql_chain(question)
    print(sql_query)
    pattern="<SQL>(.*?)</SQL>"
    matches=re.findall(pattern,sql_query,re.DOTALL)

    if len(matches)==0:
        return "Sorry, no results"
    print(matches[0].strip())
    response= run_query(matches[0].strip())
    if response is None:
        return "Sorry, no results"

    return response




def final_answer(query,context):

    #context_dic = context.to_dict(orient="records")
    comprehension_prompt = f"""
    You are a product information extractor. Given a user query and a product dataframe, extract and return only the relevant products.

    **Output Format** (strictly follow this):
    1. <title>: Rs <price> (<discount>% off), Rating: <rating> | <product_link>
    2. <title>: Rs <price> (<discount>% off), Rating: <rating> | <product_link>

    **Rules:**
    -Use the exact value from the 'title' column (or whichever column contains the product name)
    - Only include products relevant to the query
    - If discount is unavailable, omit that part
    - If rating is unavailable, write Rating: N/A
    - Return at most 5 most relevant results
    - Do not add extra commentary
    -Only return output format

    **Examples:**
    1. Campus Women Running Shoes: Rs 1,104 (35% off), Rating: 4.4 | https://example.com/campus-shoes
    2. Nike Air Max: Rs 10,000 (20% off), Rating: 4.0 | https://example.com/nike-air-max
    
    Do not add extra commentary and give output like above example.
    
    Question: {query}
    Dataframe: {context}
    """

    chat = client_sql.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": comprehension_prompt,
            }
        ],
        model=GROQ_MODEL,
        temperature=0.2,
        max_tokens=1500
    )
    return chat.choices[0].message.content

if __name__ == "__main__":

    query="shoes with discount 40%"
    #query="select * from product where brand like '%nike%' and price"
    df=sql_generate(query)

    x=final_answer(query,df)
    print(x)

