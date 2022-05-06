import requests
import json
import os
from dotenv import load_dotenv
import datetime

order_string = f'''
{{
  "data": {{
    "id":"dab9eb1c-f25f-4f89-8af3-b7ba17bd2da6",
    "type": "order-payments",
    "attributes": {{
      "paymentType": "payment",
      "date": "{datetime.date.today()}",
      "amount": 8400,
      "description": "a"
    }},
    "relationships": {{
      "method": {{
        "data": {{
          "type": "payment-methods",
          "id": "07dd24feb-f4fd-4f78-81e8-c0efc4533454"
        }}
      }},
      "shift": {{
        "data": {{
          "type": "shifts",
          "id": "590d0a47-e51e-4a47-a753-1ed4b3c98358"
        }}
      }}
    }}
  }}
}}
'''

dotenv_path = '.env'
load_dotenv(dotenv_path)

posiflora_base_url = os.environ.get("POSIFLORA_BASE_URL")
posiflora_access_token = os.environ.get("POSIFLORA_ACCESS_TOKEN")
posiflora_refresh_token = os.environ.get("POSIFLORA_REFRESH_TOKEN")

order = "56a0dfc0-be91-495e-9c16-8fc5f099ba67"

posiflora_payment_url = posiflora_base_url + f'public/api/v1/orders/{order}/payments'


headers = {
    'Authorization': 'Bearer {}'.format(posiflora_access_token),
    'Content-Type': 'application/json'
}

data = json.loads(order_string)

req = requests.post(posiflora_payment_url, headers=headers, json=data)
print(req.text)
