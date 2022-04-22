import requests
import json
import os

from datetime import timedelta, date
from dotenv import load_dotenv

dotenv_path = '.env'
load_dotenv(dotenv_path)

amo_base_url = os.environ.get("AMO_BASE_URL")
endpoint = '/api/v4/account'
method = 'GET'
access_token = os.environ.get("AMO_ACCESS_TOKEN")
headers = {
    'User-Agent': 'amoCRM-oAuth-client/1.0',
    'Authorization': f'Bearer {access_token}'
}

res = requests.get(url=amo_base_url+endpoint, headers=headers)

print(json.loads(res.text))
