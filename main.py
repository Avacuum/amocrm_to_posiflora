from fastapi import FastAPI, Request
from pydantic import BaseModel
from utils import get_id_from_url, get_lead
import requests
import json
import os
from dotenv import load_dotenv
app = FastAPI()


@app.post("/lead")
async def get_body(request: Request):
    a = await request.body()
    get_lead(get_id_from_url(a))
    f = open("logs.txt", "a")
    f.write(str(a)+"\n")
    f.close()
    return 200

