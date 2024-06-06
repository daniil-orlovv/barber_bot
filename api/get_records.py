import requests
from utils.utils import return_date_for_records
from utils.utils_db import get_phone_by_telegram_id
from config_data.config import COMPANY_ID, PARTNER_TOKEN, USER_TOKEN
from api.utils_api import get_record


def selection_of_records_by_company(session, telegram_id):
    headers = {
        'Authorization': f'Bearer {PARTNER_TOKEN}, User {USER_TOKEN}',
        'Accept': 'application/vnd.api.v2+json',
        'Content-type': 'application/json'
    }
    url = f'https://api.yclients.com/api/v1/records/{COMPANY_ID}'
    response = requests.get(url, headers=headers)
    response_json = response.json()
    records = response_json['data']
    print(records)
    records_of_client = []
    phone_from_db = get_phone_by_telegram_id(session, telegram_id)
    print(f'телефон из дб: {phone_from_db}')
    for record in records:
        client = record['client']
        phone = client['phone']
        print(f'телефон из json: {phone}')
        if phone == phone_from_db:
            records_of_client.append(record)
    print(records_of_client)
    return records_of_client


def get_title_and_date_of_records(records_of_client: list):
    records = {}
    print(records_of_client)
    for record in records_of_client:
        services = record['services']
        print(services)
        title = services[0]['title']
        print(title)
        date = record.get('date')
        print(date)
        new_date = return_date_for_records(date)
        title_date = ' '.join([title, new_date])
        record_id = record.get('id')
        records[title_date] = str(record_id)
    return records


def get_record_by_id(record_id, user_token):
    headers = {
        'Authorization': f'Bearer {PARTNER_TOKEN}, User {USER_TOKEN}',
        'Accept': 'application/vnd.api.v2+json',
        'Content-type': 'application/json'
    }
    url = f'https://api.yclients.com/api/v1/record/{COMPANY_ID}/{record_id}'
    response = requests.get(url, headers=headers)
    record = get_record(response)
    return record
