import requests
from utils.utils import return_date_for_records
from config_data.config import COMPANY_ID
from api.settings_api import headers_for_get
from api.utils_api import get_record


def selection_of_records_by_company(user_token):
    headers = headers_for_get.format(user_token)
    url = 'https://api.yclients.com/api/v1/user/records/'
    response = requests.get(url, headers=headers)
    response_json = response.json()
    records = response_json['data']
    records_of_client = []
    for record in records:
        company = record['company']
        id_company = company['id']
        if id_company != COMPANY_ID:
            continue
        else:
            records_of_client.append(record)
    return records_of_client


def get_title_and_date_of_records(records_of_client: list):
    records = {}
    for record in records_of_client:
        services = record['services']
        title = services[0]['title']
        date = record.get('date')
        new_date = return_date_for_records(date)
        title_date = ' '.join([title, new_date])
        record_id = record.get('id')
        records[title_date] = str(record_id)
    return records


def get_record_by_id(record_id, user_token):
    headers = headers_for_get.format(user_token)
    url = f'https://api.yclients.com/api/v1/user/records/{record_id}'
    response = requests.get(url, headers=headers)
    record = get_record(response)
    return record
