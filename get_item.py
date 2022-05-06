import requests
import json
import os
from dotenv import load_dotenv

dotenv_path = '.env'
load_dotenv(dotenv_path)

amo_base_url = os.environ.get("AMO_BASE_URL")
item_id = 986945
catalog_id = 6305

endpoint = f'/api/v4/catalogs/{catalog_id}/elements/{item_id}'
access_token = os.environ.get("AMO_ACCESS_TOKEN")
method = 'GET'

headers = {
    'User-Agent': 'amoCRM-oAuth-client/1.0',
    'Authorization': 'Bearer {}'.format(access_token)
}
params = {
    'with': 'catalog_elements'
}

res = requests.get(url=amo_base_url+endpoint, headers=headers, params=params)
a = res.json()

item_name = a["name"]
item_price = a["custom_fields_values"][1]["values"][0]["value"]
item_posi_id = a["custom_fields_values"][0]["values"][0]["value"]
print(a, item_price, item_name, item_posi_id)

