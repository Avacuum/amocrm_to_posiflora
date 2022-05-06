import requests
import json
import os
from dotenv import load_dotenv

dotenv_path = '.env'
load_dotenv(dotenv_path)

posiflora_base_url = os.environ.get("POSIFLORA_BASE_URL")
posiflora_access_token = os.environ.get("POSIFLORA_ACCESS_TOKEN")
posiflora_refresh_token = os.environ.get("POSIFLORA_REFRESH_TOKEN")
posiflora_get_orders_url = posiflora_base_url + 'public/api/v1/orders'

headers = {
    'Authorization': 'Bearer {}'.format(posiflora_access_token)
}

params = {
    "search": "aaaa22000023"
}

res = requests.get(url=posiflora_get_orders_url, params=params, headers=headers)
print(res.text)
