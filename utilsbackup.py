import random

import requests
import json
import os
from dotenv import load_dotenv
from random import randint
import datetime


def get_refresh_posiflora():
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


def get_refresh_amo():
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
        res = requests.post(url=base_url + endpoint, data=params, headers=headers)
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


def find_field(amo_json, field_name, ex_value):
    for field in amo_json["custom_fields_values"]:
        if field["field_name"] == field_name:
            return field["values"][0]["value"]
    else:
        return ex_value


def get_lead(lead_id):
    dotenv_path = '.env'
    load_dotenv(dotenv_path)

    amo_base_url = os.environ.get("AMO_BASE_URL")
    endpoint = f'/api/v4/leads/{lead_id}'
    access_token = os.environ.get("AMO_ACCESS_TOKEN")

    headers = {
        'User-Agent': 'amoCRM-oAuth-client/1.0',
        'Authorization': f'Bearer {access_token}'
    }
    params = {
        'with': 'catalog_elements'
    }

    res = requests.get(url=amo_base_url + endpoint, headers=headers, params=params)
    a = res.json()

    return a


def get_item_data(amo_json):
    dotenv_path = '.env'
    load_dotenv(dotenv_path)

    amo_base_url = os.environ.get("AMO_BASE_URL")
    catalog_elements = []
    for catalog_element in amo_json["_embedded"]["catalog_elements"]:
        catalog_elements.append({"catalog_id": catalog_element["metadata"]["catalog_id"],
                                 "item_id": catalog_element["id"]
                                 })

    #catalog_id = amo_json["_embedded"]["catalog_elements"][0]["metadata"]["catalog_id"]
    #item_id = amo_json["_embedded"]["catalog_elements"][0]["id"]

    access_token = os.environ.get("AMO_ACCESS_TOKEN")

    headers = {
        'User-Agent': 'amoCRM-oAuth-client/1.0',
        'Authorization': 'Bearer {}'.format(access_token)
    }
    params = {
        'with': 'catalog_elements'
    }

    posi_items_id = []

    for element in catalog_elements:
        endpoint = f'/api/v4/catalogs/{element["catalog_id"]}/elements/{element["item_id"]}'
        resp = requests.get(url=amo_base_url + endpoint, headers=headers, params=params)
        posi_items_id.append(resp.json()["custom_fields_values"][0]["values"][0]["value"])

    #item_data = {
        #"item_name": a["name"],
        # "item_price": int(a["custom_fields_values"][1]["values"][0]["value"]),
        #"item_posi_id": a["custom_fields_values"][0]["values"][0]["value"]
    #}
    #print(item_data)
    return posi_items_id


def generate_posi_json(amo_json, item_data, spec_items):
    # quantity = int(amo_json["_embedded"]["catalog_elements"][0]["metadata"]["quantity"])
    # price = item_data["item_price"]

    offset = '06:00'

    delivery_time = find_field(amo_json, "Желаемое время доставки", "10:00")
    print(delivery_time)
    delivery_address = find_field(amo_json, "Адрес доставки", "Адрес не указан")
    print(delivery_address)
    phone_number = find_field(amo_json, "Телефон получателя", "0000000000")
    print(phone_number)
    payment_method = find_field(amo_json, "Способ оплаты", "Онлайн на сайте")
    print(payment_method)
    comment = find_field(amo_json, "Комментарии клиентов", "Без комментария")
    print(comment)
    card_text = find_field(amo_json, "Текст открытки", "Без открытки")
    print(card_text)
    epoch_delivery_date = find_field(amo_json, "Дата доставки", False)
    if epoch_delivery_date:
        delivery_date = datetime.datetime.fromtimestamp(epoch_delivery_date, datetime.timezone.utc).strftime("%Y.%m.%d")
    else:
        delivery_date = "Не указана"
    print(delivery_date)


    delivery_time_format = '%H:%M'
    offset_delivery_time = datetime.datetime.strptime(delivery_time, delivery_time_format) - datetime.datetime.strptime(
        offset, delivery_time_format)
    posi_json = f'''{{
    "data": {{
            "type": "orders",
            "attributes": {{
                "docNo": "{"test" + str(randint(0, 1000000))}",
                "date": "{datetime.date.today()}",
                "description": "{payment_method}",
                "budget": 0,
                "dueTime": "{datetime.datetime.fromtimestamp(amo_json['created_at'], datetime.timezone.utc).isoformat('T', 'seconds')}",
                "delivery": "true",
                "deliveryComments": "{comment}. Дата доставки: {delivery_date}. Текст открытки: {card_text}",
                "deliveryCity": "",
                "deliveryStreet": "{delivery_address}",
                "deliveryHouse": "",
                "deliveryApartment": "",
                "deliveryTimeFrom": "2022-05-28T{offset_delivery_time}+06:00",
                "deliveryTimeTo": "2022-06-28T{offset_delivery_time}+06:00",
                "deliveryContact": "{amo_json["custom_fields_values"][1]["values"][0]["value"]}",
                "deliveryPhoneCode": "7",
                "deliveryPhoneNumber": "{phone_number[2::]}",
                "createdAt": "{datetime.date.today()}T{datetime.datetime.now().strftime("%H:%M:%S")}+06:00",
                "fiscal": "true",
                "byBonuses": "false",
                "deliveryStatus": null
            }},
            "relationships": {{
                "store": {{
                    "data": {{
                        "type": "stores",
                        "id": "83ff37f7-4270-4aec-ac50-639262bf10bb"
                    }}
                }},
                "customer": {{
                    "data": null
                }},
                "source": {{
                    "data": {{
                        "type": "order-sources",
                        "id": "9bed7b59-94dc-4ce4-aac2-883aab1a148c"
                    }}
                }},
                "createdBy": {{
                    "data": {{
                        "type": "workers",
                        "id": "a79c3f57-d0e8-4121-9c3a-b5ddf9c76a3e"
                    }}
                }},
                "courier": {{
                    "data": {{
                        "type": "workers",
                        "id": "a79c3f57-d0e8-4121-9c3a-b5ddf9c76a3e"
                    }}
                }},
                "florist": {{
                    "data": {{
                        "type": "workers",
                        "id": "a79c3f57-d0e8-4121-9c3a-b5ddf9c76a3e"
                    }}
                }},
                "discounts": null,
                "lines": {{
                    "data": [
                        {spec_items}
                    ]
                }}
            }}
        }}
    }}'''
    f = open('res.json', 'w')
    f.write(posi_json)
    f.close()
    print('ok')
    return posi_json


def send_posi_order(posi_json):
    dotenv_path = '.env'
    load_dotenv(dotenv_path)

    posiflora_base_url = os.environ.get("POSIFLORA_BASE_URL")
    posiflora_access_token = os.environ.get("POSIFLORA_ACCESS_TOKEN")
    posiflora_refresh_token = os.environ.get("POSIFLORA_REFRESH_TOKEN")
    posiflora_order_url = posiflora_base_url + 'public/api/v1/orders'

    headers = {
        'Authorization': 'Bearer {}'.format(posiflora_access_token)
    }

    req = requests.post(posiflora_order_url, headers=headers, json=json.loads(posi_json))
    return req.json()


def get_specifications_items(specification_ids):
    dotenv_path = '.env'
    load_dotenv(dotenv_path)

    posiflora_base_url = os.environ.get("POSIFLORA_BASE_URL")
    posiflora_access_token = os.environ.get("POSIFLORA_ACCESS_TOKEN")
    posiflora_refresh_token = os.environ.get("POSIFLORA_REFRESH_TOKEN")

    headers = {
        'Authorization': 'Bearer {}'.format(posiflora_access_token)
    }
    bouquets_price = 0
    params = {'include': 'specVariants.specItems.item'}
    final_json = []
    for spec in specification_ids:
        posiflora_get_orders_url = posiflora_base_url + f'api/v1/specifications/{spec}'
        res = requests.get(url=posiflora_get_orders_url, params=params, headers=headers)
        bouquets_price += res.json()["data"]["attributes"]["maxPrice"]
        bouquet_name = res.json()["data"]["attributes"]["title"]
        print(bouquet_name)
        bouquets_url = posiflora_base_url + 'api/v1/bouquets?page[number]=1&page[size]=100'
        bouquets = requests.get(url=bouquets_url, headers=headers)
        for b in bouquets.json()["data"]:
            if bouquet_name in b["attributes"]["title"]:
                bouquet_id = b["id"]
                print(b["attributes"]["title"])
                break
        else:
            bouquet_id = '503aeee2-4947-45f0-bcdd-273be0fc4df4'

        bouquet_data = requests.get(url=posiflora_get_orders_url, headers=headers)
        items = []
        i = 0
        while i < len(res.json()["included"]) - 1:
            items.append([res.json()["included"][i], res.json()["included"][i + 1]])
            i += 2
        print(len(items))
        response = []
        for field in items:
            qty = field[1]["attributes"]["qty"]
            price = field[0]["attributes"]["priceMax"]
            item_id = field[0]["id"]
            json_pattern = f'''
            {{
                "id":null,
                "type":"order-lines",
                "attributes":{{
                   "qty":{qty},
                   "price":{price},
                   "totalAmount":{price * qty},
                   "totalAmountWithDiscount":{price * qty}
                }},
                "relationships":{{
                   "item":{{
                      "data":{{
                         "type":"inventory-items",
                         "id":"{item_id}"
                      }}
                   }},
                   "bouquet":{{
                      "data":{{
                         "type":"bouquets",
                         "id":"{bouquet_id}"
                      }}
                   }}
                }}
             }}
            '''
            response.append(json_pattern)
            respon = ','.join(response)
            final_json.append(respon)
    f = ','.join(final_json)
    return f, bouquets_price


def send_payment(posi_order, price):
    print(type(posi_order))
    payment_method = posi_order["data"]["attributes"]["description"]
    print(payment_method)
    payment_methods_ids = {
        "Онлайн на сайте": "7dd24feb-f4fd-4f78-81e8-c0efc4533454",
        "Kaspi": "a672111f-c3fa-4e68-bc78-57208e1b8c36"
    }

    payment_methods_id = payment_methods_ids[payment_method]
    print(payment_methods_id)
    # amount = posi_order["data"]["attributes"]["totalAmount"]
    order = posi_order["data"]["id"]

    order_string = f'''
    {{
      "data": {{
        "id":"dab9eb1c-f{random.randint(10, 99)}f-4f{random.randint(10, 99)}-8af3-b7ba17bd2da6",
        "type": "order-payments",
        "attributes": {{
          "paymentType": "payment",
          "date": "{datetime.date.today()}",
          "amount": {price},
          "description": "from online shop"
        }},
        "relationships": {{
          "method": {{
            "data": {{
              "type": "payment-methods",
              "id": "{payment_methods_id}"
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

    posiflora_payment_url = posiflora_base_url + f'public/api/v1/orders/{order}/payments'

    headers = {
        'Authorization': 'Bearer {}'.format(posiflora_access_token),
        'Content-Type': 'application/json'
    }

    data = json.loads(order_string)

    req = requests.post(posiflora_payment_url, headers=headers, json=data)
    print(req.text)


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
