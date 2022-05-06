from fastapi import FastAPI, Request
from pydantic import BaseModel
from utils import *
import requests
import json
import os
from dotenv import load_dotenv
app = FastAPI()


@app.post("/lead")
async def get_body(request: Request):
    get_refresh_posiflora()
    webhook = await request.body()
    amo_lead = get_lead(get_id_from_url(webhook))
    item_data = get_item_data(amo_lead)
    spec_items = get_specifications_items(item_data)
    posi_json = generate_posi_json(amo_lead, item_data, spec_items[0])
    order_request = send_posi_order(posi_json)
    send_payment(order_request, spec_items[1])
    print(order_request)
    print(type(order_request))
    return 200


