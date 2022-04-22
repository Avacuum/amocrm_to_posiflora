import requests
import json
import os
from dotenv import load_dotenv

dotenv_path = '.env'
load_dotenv(dotenv_path)

amo_secret_key = os.environ.get("AMO_SECRET_KEY")
amo_integration_id = os.environ.get("AMO_INTEGRATION_ID")
amo_auth_code = os.environ.get("AMO_AUTH_CODE")
amo_base_url = os.environ.get("AMO_BASE_URL")
amo_refresh_token = os.environ.get("AMO_REFRESH_TOKEN")
amo_redirect_uri = os.environ.get("AMO_REDIRECT_URI")


def refresh_tokens(base_url, client_id, client_secret, refresh_token, redirect_uri):
    endpoint = '/oauth2/access_token'
    method = 'POST'

    headers = {
        'User-Agent': 'amoCRM-oAuth-client/1.0'
    }
 
    params = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'redirect_uri': redirect_uri
    }
    res = requests.post(url=base_url+endpoint, data=params, headers=headers)
    return json.loads(res.text)


def write_to_env(refresh_token, var_name='AMO_REFRESH_TOKEN', dotenv_path='.env'):
    with open(dotenv_path, 'r') as f:
        lines = f.readlines()
        d = {k: v for k, v in [l.replace('\n', '').split('=') for l in lines]}
        d[var_name] = refresh_token
    to_write = [k + '=' + v for k, v in d.items()]
    
    with open(dotenv_path, 'w') as f:
        for l in to_write:
            f.write(l + '\n')


creds = refresh_tokens(amo_base_url, amo_integration_id, amo_secret_key, amo_refresh_token, amo_redirect_uri)

print(creds)

write_to_env(creds['refresh_token'])
write_to_env(creds['access_token'], var_name='AMO_ACCESS_TOKEN')
