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

#res = requests.request("POST", auth_url, data=json_dump, headers=headers)
res = requests.post(url=auth_url, json=data, headers=headers)
print(json.loads(res.text))
res = json.loads(res.text)
print(type(res))
write_to_env(res['data']['attributes']['accessToken'], var_name='POSIFLORA_ACCESS_TOKEN')
write_to_env(res['data']['attributes']['refreshToken'], var_name='POSIFLORA_REFRESH_TOKEN')

#d = {
#    'data':
#        {'type': 'sessions',
#         'id': 'current',
#         'attributes':
#             {'expireAt': '2022-04-22T21:21:49+00:00',
#              'refreshExpireAt': '2022-05-22T20:21:49+00:00',
#              'accessToken': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE2NTA2NTg5MDksImV4cCI6MTY1MDY2MjUwOSwiY3VzdG9tZXIiOiIxNDE2MSIsImlkIjoiMzEyZmRmNzMtOTczNy00ZDgwLTgyYmEtZWU1YzY4YzI3MThiIiwibG9naW4iOiJhc2V0LmRldiJ9.bOpCV7SoQUhcpBZYCP6vQU-5ve4-UEmr8fPPEOQrO_kwqpF5DyELddGKrUnpDz2szV8mhV7GdIfMCPxZ8iyKnO_pfK20lMGcm1xe1LHsM1umdVPLNLodnIko8W5vkZWDXQXq0YueYvUUMDHDv2UXng-seT9uL_iu2dhd95ZGNZCMhPv6LhC23FGXLFliLlB_jDyWwR9d9B0-LX7QEKYPs07qIP1FyIp-_g62DJQ0JyZohnDpBY2IsT_KhTfjGddtC0b2vZ-LmpIvB9o8XujAFQYB585oA2ZCFjgpA0pWlk-lHDztlLwYBOR_fcmGWTK1dNq0tCUyDhe9KSq7mEV6QA', 'refreshToken': 'abb4c176-95ba-4c33-8536-4ff94b576cbf', 'saasCustomerId': 14161}, 'relationships': {'worker': {'data': {'type': 'workers', 'id': 'b2422bb6-6cfd-444a-b5c7-495a5c07714a'}}}}}
