import requests
import json
import os
from dotenv import load_dotenv
import datetime

order_string = """{
    "data": {
            "type": "orders",
            "attributes": {
                "docNo": "144111",
                "date": "2022-05-03",
                "description": "Онлайн на сайте",
                "budget": 0,
                "dueTime": "2022-04-11T04:55:22+00:00",
                "delivery": "true",
                "deliveryComments": "test comment",
                "deliveryCity": "",
                "deliveryStreet": "ул. Сатпаева, 51",
                "deliveryHouse": "",
                "deliveryApartment": "",
                "deliveryTimeFrom": "2022-05-28T10:30:00+06:00",
                "deliveryTimeTo": "2022-06-28T10:30:00+06:00",
                "deliveryContact": "Алёна",
                "deliveryPhoneCode": "7",
                "deliveryPhoneNumber": "7774441111",
                "createdAt": "2022-05-03T06:57:02+06:00",
                "fiscal": "true",
                "byBonuses": "false",
                "deliveryStatus": null
            },
            "relationships": {
                "store": {
                    "data": {
                        "type": "stores",
                        "id": "83ff37f7-4270-4aec-ac50-639262bf10bb"
                    }
                },
                "customer": {
                    "data": null
                },
                "source": {
                    "data": {
                        "type": "order-sources",
                        "id": "9bed7b59-94dc-4ce4-aac2-883aab1a148c"
                    }
                },
                "createdBy": {
                    "data": {
                        "type": "workers",
                        "id": "a79c3f57-d0e8-4121-9c3a-b5ddf9c76a3e"
                    }
                },
                "courier": {
                    "data": {
                        "type": "workers",
                        "id": "a79c3f57-d0e8-4121-9c3a-b5ddf9c76a3e"
                    }
                },
                "florist": {
                    "data": {
                        "type": "workers",
                        "id": "a79c3f57-d0e8-4121-9c3a-b5ddf9c76a3e"
                    }
                },
                "discounts": null,
                "lines": {
                    "data": [
                        
        {
            "id":null,
            "type":"order-lines",
            "attributes":{
               "qty":3,
               "price":1500,
               "totalAmount":4500,
               "totalAmountWithDiscount":4500
            },
            "relationships":{
               "item":{
                  "data":{
                     "type":"inventory-items",
                     "id":"1a5456f2-8120-4ae4-8b3a-aaabea6f9ca8"
                  }
               },
               "specification":{
                  "data":{
                      "type": "specifications",
                        "id": "7c8ef3ba-2d7e-4b9c-ad32-5a6d6a865e40"
                  }
               }
            }
         },
        
        {
            "id":null,
            "type":"order-lines",
            "attributes":{
               "qty":1,
               "price":1400,
               "totalAmount":1400,
               "totalAmountWithDiscount":1400
            },
            "relationships":{
               "item":{
                  "data":{
                     "type":"inventory-items",
                     "id":"afd1264a-1133-40fc-85f7-e400721386e9"
                  }
               },
               "specification":{
                  "data":{
                      "type": "specifications",
                        "id": "7c8ef3ba-2d7e-4b9c-ad32-5a6d6a865e40"
                  }
               }
            }
         }
            ]
         }
      }
   }
}"""

dotenv_path = '.env'
load_dotenv(dotenv_path)

posiflora_base_url = os.environ.get("POSIFLORA_BASE_URL")
posiflora_access_token = os.environ.get("POSIFLORA_ACCESS_TOKEN")
posiflora_refresh_token = os.environ.get("POSIFLORA_REFRESH_TOKEN")
posiflora_order_url = posiflora_base_url + 'public/api/v1/orders'


headers = {
    'Authorization': 'Bearer {}'.format(posiflora_access_token)
}

#data = json.loads(order_string)
print(order_string)

req = requests.post(posiflora_order_url, headers=headers, json=json.loads(order_string))
print(req.text)
