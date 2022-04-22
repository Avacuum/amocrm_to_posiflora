import requests
import json
import os
from dotenv import load_dotenv

dotenv_path = '.env'
load_dotenv(dotenv_path)

amo_base_url = os.environ.get("AMO_BASE_URL")
endpoint = '/api/v4/leads/30467665'
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

print(json.loads(res.text))
