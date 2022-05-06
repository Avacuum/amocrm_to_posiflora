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
        "type": "sessions",
        "attributes": {
            "username": f"{posiflora_username}",
            "password": f"{posiflora_password}"
        }
    }
}
json_dump = json.dumps(data)
print(auth_url)
print(json_dump)


def write_to_env(refresh_token, var_name='AMO_REFRESH_TOKEN', path='.env'):
    with open(path, 'r') as f:
        lines = f.readlines()
        d = {k: v for k, v in [line.replace('\n', '').split('=') for line in lines]}
        d[var_name] = refresh_token
    to_write = [k + '=' + v for k, v in d.items()]

    with open(path, 'w') as f:
        for l in to_write:
            f.write(l + '\n')


res = requests.post(url=auth_url, json=data, headers=headers)
print(json.loads(res.text))
res = json.loads(res.text)
print(type(res))
write_to_env(res['data']['attributes']['accessToken'], var_name='POSIFLORA_ACCESS_TOKEN')
write_to_env(res['data']['attributes']['refreshToken'], var_name='POSIFLORA_REFRESH_TOKEN')

