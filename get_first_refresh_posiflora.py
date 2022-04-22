import requests
import json
import os
from dotenv import load_dotenv

dotenv_path = '.env'
load_dotenv(dotenv_path)

posiflora_username = os.environ.get("POSIFLORA_USERNAME")
posiflora_password = os.environ.get("POSIFLORA_PASSWORD")
posiflora_base_url = os.environ.get("POSIFLORA_BASE_URL")
auth_url = f"{posiflora_base_url}public/api/v1/sessions"

headers = {'Content-Type': 'application/json'}

data = {
    "data": {
        "type": "string",
        "attributes": {
            "username": f"{posiflora_username}",
            "password": f"{posiflora_password}"
        }
    }
}

res = requests.post(url=auth_url, json=data, headers=headers)
print(json.loads(res.text))
