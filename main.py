

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
    table: str = "filter"
    
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):     
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/hello")
def hello_world():
    # newOne = handle_response();
    return {"Message" : "Hello World"}

@app.post("/action")
async def root(item: Item):
    print("Action method called")
    text = item.text
    messages = item.messages

    messages.append(
        {"role": "assistant", "content": "you are sql query generator AI model"})

    messages.append({"role": "user", "content": text})
    
    _new_dataframe = dataframes.get(item.table, None)

    # _new_dataframe.info()

    (result, _messages) = get_prompt_result(
        {"MESSAGES": messages, "QUERY": combine_prompts({item.table: _new_dataframe}, text)})
     
    print("Response result: ", result)
    messages = _messages
    # messages = _messages
    return {"data": result, "messages":messages}
