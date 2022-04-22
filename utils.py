import requests
import json
import os
from dotenv import load_dotenv


def get_lead(lead_id):
    dotenv_path = '.env'
    load_dotenv(dotenv_path)

    amo_base_url = os.environ.get("AMO_BASE_URL")
    endpoint = f'/api/v4/leads/{lead_id}'
    access_token = os.environ.get("AMO_ACCESS_TOKEN")
    method = 'GET'

    headers = {
        'User-Agent': 'amoCRM-oAuth-client/1.0',
        'Authorization': f'Bearer {access_token}'
    }
    params = {
        'with': 'catalog_elements'
    }

    res = requests.get(url=amo_base_url + endpoint, headers=headers, params=params)

    print(json.loads(res.text))
    return json.loads(res.text)


def get_id_from_url(url):
    url = str(url)
    res = ''
    add_numbers = False
    for symbol in url:
        if symbol == '=':
            add_numbers = True
            continue
        if add_numbers:
            if symbol == '&':
                return int(res)
            res += symbol
