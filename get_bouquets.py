import requests
import json
import os
from dotenv import load_dotenv

dotenv_path = '.env'
load_dotenv(dotenv_path)

posiflora_base_url = os.environ.get("POSIFLORA_BASE_URL")
posiflora_access_token = os.environ.get("POSIFLORA_ACCESS_TOKEN")
posiflora_refresh_token = os.environ.get("POSIFLORA_REFRESH_TOKEN")
posiflora_get_orders_url = posiflora_base_url + 'api/v1/specifications/4e0f733f-3c59-467b-8a3e-81ce3a0de8fb'

headers = {
    'Authorization': 'Bearer {}'.format(posiflora_access_token)
}

params = {'include': 'specVariants.specItems.item'}

res = requests.get(url=posiflora_get_orders_url, params=params, headers=headers)
print(res.json()["data"]["attributes"]["maxPrice"])
