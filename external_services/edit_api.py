import requests
import datetime
import logging
from utils.utils import return_date_for_records
from config_data.config import COMPANY_ID

from external_services.settings_api import urls, headers, request_body
from external_services.utils_api import get_record

logger = logging.getLogger(__name__)

current_year = datetime.datetime.now().year


def get_ycl_id(phone):
    url = urls['get_ycl_id'].format(COMPANY_ID)
    data_for_request = request_body['get_ycl_id']
    response = requests.post(url, headers=headers, json=data_for_request)
    response_json = response.json()
    data = response_json['data']
    clients = {}
    for client in data:
        print(f'Клиент: {client}')
        clients[client.get('phone')] = client.get('id')
    print(f'phone: {phone}')
    print(f'clients:{clients}')
    ycl_id = clients.get(phone)
    print(f'ycl_id:{ycl_id}')
    return ycl_id


def get_all_records_by_client(ycl_id):
    url = urls['get_all_records_by_client'].format(COMPANY_ID, ycl_id)
    response = requests.get(url, headers=headers)
    response_json = response.json()
    data = response_json['data']
    records = {}
    for record in data:
        services = record['services']
        title = services[0]['title']
        date = record.get('date')
        new_date = return_date_for_records(date)
        title_date = ' '.join([title, new_date])
        record_id = record.get('id')
        records[title_date] = str(record_id)
    return records


def get_record_by_id(record_id):
    url = urls['get_record_by_id'].format(COMPANY_ID, record_id)
    response = requests.get(url, headers=headers)
    record = get_record(response)
    return record


def edit_record(state_data):
    record_id = state_data['record_id']
    date = state_data['new_date']
    time = state_data['new_time']
    datetime = date + time
    url = urls['edit_record'].format(COMPANY_ID, record_id)

    data_for_request = {
        "staff_id": state_data['staff_id'],
        "services": [{
                "id": state_data['service_id']
            }
        ],
        "client": {
            "id": state_data['client_id']
        },
        "datetime": datetime,  # "2024-05-09 17:00:00"
        "seance_length": state_data['seance_length']
    }
    response = requests.put(url, headers=headers, json=data_for_request)
    return response.text


def delete_record(record_id):
    url = urls['delete_record'].format(COMPANY_ID, record_id)
    requests.delete(url, headers=headers)
