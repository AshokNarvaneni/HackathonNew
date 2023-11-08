import openai
import boto3
#import pyodbc
import pymssql
import time
from setup import *
from config import *
import re

openai.api_key = OPEN_APIKEY
table_definitions = {} # This will store your table definitions


def create_table_definition(df, table_name):
    column_definitions = [f"{col} {df[col].dtype}" for col in df.columns]
    table_definition = f"-- Table Definition for {table_name}: CREATE TABLE {table_name} (\n"
    table_definition += ",\n".join(column_definitions)
    table_definition += "\n)"
    return table_definition

def initialize_table_definitions():
    global table_definitions
    for table_name, df in dataframes.items():
        table_definitions[table_name] = create_table_definition(df, table_name)
        
# Call this function once during your application's initialization
initialize_table_definitions()


# def combine_prompts(dataframes, query):
#     combined_prompt = ""
#     for table_name, df in dataframes.items():
#         table_definition = create_table_definition(df, table_name)
#         query_prompt = f"-- sql query to answer for: {query} on {table_name}:"
#         combined_prompt += f"{table_definition}\n{query_prompt}\n\n"

#     return combined_prompt


def combine_prompts(dataframes, tables, query):
    combined_prompt = ""
    for table_name in tables:
        df = dataframes.get(table_name)
        if df is not None:  # Check if the dataframe exists for the given table name
            # table_definition = create_table_definition(df, table_name)
            table_definition = table_definitions[table_name]
             # Append the table definition to the combined prompt
            combined_prompt += f"{table_definition}\n"
    # After all table definitions, append the query
    query_prompt = f"-- SQL query to answer for: {query} on the SQL Server tables above."
    combined_prompt += f"{query_prompt}\n\n"
    return combined_prompt

def handle_response(response):
    # query = response['choices'][0]['message']['content']
    query = response.choices[0].message.content
    if not query.startswith("SELECT") and not query.startswith("select"):
        query = "SELECT "+query
    # Check if the query ends with a LIMIT clause
    limit_pattern = re.compile(r'\sLIMIT\s+\d+\s*$', re.IGNORECASE)
    if limit_pattern.search(query):
        # Remove the LIMIT clause
        query = limit_pattern.sub("", query)
    return query


def retrive_param(event, key, default):
    try:
        return event[key]
    except:
        return default

# Function to execute query in SQL Server
def execute_sql(query):
    # Establishing the connection
    #conn = pyodbc.connect(SQL_SERVER_CONNECTION_STRING)
    # query1 = "SELECT * from users"
    conn = pymssql.connect(server=SERVER, user=UID, password=PWD, database=DATABASE)
    cursor = conn.cursor()
    # sql server odbc driver for macos
    # Executing the query
    cursor.execute(query)
    
    # Fetching results
    rows = cursor.fetchall()

    #convert list of tuples as list of dictionaries
    column_names = [col[0] for col in cursor.description]
    results = [dict(zip(column_names, row)) for row in rows]

    # Closing the connection
    conn.close()
    
    return results

# ... (your other functions)

# Modify your main part of the code where you call the execute function
# Replace execute_athena call with execute_sql function

# if __name__ == "__main__":
#     results = execute_sql("your_sql_query")
#     print(results)

def get_prompt_result(event):
    try:
        messages = retrive_param(event, "MESSAGES", [])
        query = retrive_param(event, "QUERY", "Thanks")
        messages.append({"role": "user", "content": query})
        response = openai.chat.completions.create(
            model=MODEL_NAME,
            messages=messages
        )
        # print("ChatGPT Response:", response)
        text_response = handle_response(response)
        messages.append({"role": "assistant", "content": text_response})
        
        print("ChatGPT Response:", text_response)

        # return (text_response, messages)
        return (execute_sql(text_response), messages)

    except Exception as error:
        print("ERROR is " , error)
        return ([{"type": "error", "text": "Sorry Couldn't find the results for the query, Please give me more specific and refined Query."}], messages)
    
