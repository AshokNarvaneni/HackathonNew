

from fastapi import FastAPI, Request
from cs_chat_gpt import *
import openai
from setup import *
from pydantic import BaseModel
from typing import List, Dict
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from config import *

app = FastAPI()
templates = Jinja2Templates(directory="templates")

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
    "*"
]
#QA URL: 'https://test-vsgapi.vsgdover.com/api/'

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
openai.api_key = OPEN_APIKEY
openai.chat.completions.create(
    model=MODEL_NAME,
    messages=[{"role": "assistant",
               "content": "Consider monitoring_events and monitoring_event_types tables can be joined using global_event_code, and consider case insensitive search"}]
)


class Item(BaseModel):
    text: str
    messages: list = []
    tables: list = []
    
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):     
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/hello")
def hello_world():
    # newOne = handle_response();
    return {"Message" : "Hello World"}

@app.post("/action")
async def root(item: Item):
    text = item.text
    messages = item.messages
    table_names = item.tables

    messages.append(
        {"role": "assistant", "content": "you are sql query generator AI model"})
    # messages.append(
    #     {"role": "assistant", "content": "you are an Json praser AI model and convert to human readable"})

    messages.append({"role": "user", "content": text})
    
    # _new_dataframe = dataframes.get(item.table, None)
    combined_prompt = combine_prompts(dataframes, table_names, text)


    # _new_dataframe.info()

    (result, _messages) = get_prompt_result(
        {"MESSAGES": messages, "QUERY": combined_prompt})

    print("Response result: ", result)
#     #jsonRes = execute_sql(result)
#     jsonRes = '''[{
#     "Email": "1289@yopmail.com",
#     "FirstName": "Abhiram",
#     "LastName": "Challapalli",
#     "PhoneNumber": 19876567890,
#     "CreatedDate": "2023-06-13 10:24:52.193",
#     "MiddleName": "",
#     "CompanyName": "ABC Company",
#     "BillingStreet": "4025 Windward Plaza",
#     "BillingCity": "Alpharetta",
#     "BillingState": "4025 Windward Plaza",
#     "BillingCountry": "United States",
#     "BillingCounty": "United States",
#     "ZipCode": 30005,
#     "UserRole": "Basic User",
#     "IsUserActive": 1,
#     "IsSolutionActive": 1
#   }]'''
#     queryNew = f"write a simple sentence in active voice from this json {jsonRes}"

#     (resultNew, _messages) = get_prompt_result(
#         {"MESSAGES": messages, "QUERY":queryNew})
     
#     print("Response result: ", resultNew)
    messages = _messages
    # messages = _messages
    return {"data": result, "messages":messages}
