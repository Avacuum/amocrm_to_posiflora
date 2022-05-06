import requests
import json
import os
from dotenv import load_dotenv
import datetime

customer_string = """
       {
   "meta":{
      "last_order":{
         "createdAt":"2022-03-27T06:10:37+00:00"
      }
   },
   "data":{
      "type":"customers",
      "id":"fb861db6-c2f7-4512-b6ee-6f5ad031b4ca",
      "attributes":{
         "title":"tesst testt",
         "birthday":null,
         "email":null,
         "instagram":null,
         "status":"on",
         "isPerson":true,
         "bonusCard":null,
         "notes":"f",
         "averageCheck":0,
         "ordersAmount":0,
         "ordersQty":0,
         "createdAt":"2022-03-26T13:07:07+00:00",
         "updatedAt":"2022-03-26T13:07:07+00:00",
         "spentPoints":0,
         "currentPoints":0,
         "gender":"female",
         "phone":"7478581103",
         "revision":8,
         "countryCode":7
      },
      "relationships":{
         "person":{
            "data":null
         },
         "discountGroups":{
            "data":[
               
            ]
         },
         "bonusGroup":{
            "data":null
         },
         "customerSources":{
            "data":[
               
            ]
         },
         "customerPreferences":{
            "data":[
               
            ]
         },
         "customerEvents":{
            "data":[
               
            ]
         }
      },
      "links":{
         "self":"\/customers\/fb861db6-c2f7-4512-b6ee-6f5ad031b4ca"
      }
   }
}
"""

dotenv_path = '.env'
load_dotenv(dotenv_path)

posiflora_base_url = os.environ.get("POSIFLORA_BASE_URL")
posiflora_access_token = os.environ.get("POSIFLORA_ACCESS_TOKEN")
posiflora_refresh_token = os.environ.get("POSIFLORA_REFRESH_TOKEN")
posiflora_order_url = posiflora_base_url + 'api/v1/customers'


headers = {
    'Authorization': 'Bearer {}'.format(posiflora_access_token)
}

data = json.loads(customer_string)

req = requests.post(posiflora_order_url, headers=headers, json=data)
print(req.text)