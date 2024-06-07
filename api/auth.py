import requests

import json

from config_data.config import COMPANY_ID, PARTNER_TOKEN

from utils.utils_db import add_client_in_db


def send_sms_code(phone, name):
    url = f'https://api.yclients.com/api/v1/book_code/{COMPANY_ID}'
    data = {
        "phone": phone,
        "fulname": name
    }
    headers = {
        'Authorization': f'Bearer {PARTNER_TOKEN}',
        'Accept': 'application/vnd.api.v2+json',
        'Content-type': 'application/json'
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        result = 'Код отправлен на ваш номер телефона.'
    else:
        result = 'Ошибка отправки кода.'
    return result


def auth(session, name, phone, code, telegram_id):
    url = 'https://api.yclients.com/api/v1/user/auth'
    data = {
        "phone": phone,
        "code": code
    }
    headers = {
        'Authorization': f'Bearer {PARTNER_TOKEN}',
        'Accept': 'application/vnd.api.v2+json',
        'Content-type': 'application/json'
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        data_of_response = response.text
        data_of_response = json.loads(data_of_response)
        print(data_of_response)
        data = data_of_response['data']
        user_token = data['user_token']
        add_client_in_db(session, name, telegram_id, phone, user_token)
        result = {'success': True, 'data': data}
    else:
        data_of_response = response.text
        meta = data_of_response['meta']
        message = meta['message']
        result = {'success': False, 'message': message}
    return result
