import requests
from requests.exceptions import ConnectionError, Timeout
import datetime
import logging
from http import HTTPStatus
from utils.utils import return_date_for_records

from config_data.config import BASE_URL, PARTNER_TOKEN, USER_TOKEN, COMPANY_ID
from utils.utils import return_date_iso8601

logger = logging.getLogger(__name__)

# USER_TOKEN = 'ce3c36b63eb89c2f212d06ecce95f761'
# PARTNER_TOKEN = 'cc9arzfwhzmcyd9rzdpu'
# COMPANY_ID = '1045579'

current_year = datetime.datetime.now().year
headers = {
    'Authorization': f'Bearer {PARTNER_TOKEN}, User {USER_TOKEN}',
    'Accept': 'application/vnd.api.v2+json',
    'Content-type': 'application/json'
}


def get_free_staff():
    try:
        url = f'{BASE_URL}/company/{COMPANY_ID}/staff/'
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code != HTTPStatus.OK:
            logger.error(f'Bad response: {response.status_code}')
        response_json = response.json()
        staffs = {}

        if 'data' not in response_json:
            logger.error('Ключ "data" не найден в response_json')
            raise KeyError('Ключ "data" не найден в response_json')
        else:
            data = response_json['data']
            for item in data:
                staffs[item.get('name')] = str(item.get('id'))

        return staffs
    except ConnectionError as error:
        logger.error(f'Ошибка соединения: {error}')
    except Timeout as error:
        logger.error(f'Превышено время ожидания ответа: {error}')


def get_free_date(staff_id):
    try:
        url = f'{BASE_URL}/book_dates/{COMPANY_ID}?staff_id={staff_id}'
        response = requests.get(url, headers=headers)
        if response.status_code != HTTPStatus.OK:
            logger.error(f'Bad response: {response.status_code}')
        response_json = response.json()

        if ('data' not in response_json
           and 'booking_days' not in response_json['data']):
            logger.error(
                'Ключи "data" и "booking_days" не найдены в response_json')
            raise KeyError(
                'Ключи "data" и "booking_days" не найдены в response_json')
        else:
            booking_days = response_json['data']['booking_days']
            quoted_dict = {
                key: [
                    str(item) for item in value
                ] for key, value in booking_days.items()
            }

            return quoted_dict
    except ConnectionError as error:
        logger.error(f'Ошибка соединения: {error}')
    except Timeout as error:
        logger.error(f'Превышено время ожидания ответа: {error}')


def get_free_time(staff_id, date):
    try:
        url = f'{BASE_URL}/book_times/{COMPANY_ID}/{staff_id}/{date}?'
        response = requests.get(url, headers=headers)
        if response.status_code != HTTPStatus.OK:
            logger.error(f'Bad response: {response.status_code}')
        response_json = response.json()

        if 'data' not in response_json:
            logger.error('Ключ "data" отсутствует в response_json')
            raise KeyError('Ключ "data" отсутствует в response_json')
        else:
            data = response_json['data']
            free_times = []
            for item in data:
                free_times.append(item.get('time'))
            return free_times
    except ConnectionError as error:
        logger.error(f'Ошибка соединения: {error}')
    except Timeout as error:
        logger.error(f'Превышено время ожидания ответа: {error}')


def get_free_services(staff_id):
    try:
        url = f'{BASE_URL}/book_services/{COMPANY_ID}?staff_id={staff_id}'
        response = requests.get(url, headers=headers)
        response_json = response.json()
        if 'data' not in response_json:
            logger.error('Ключ "data" не найден в response_json')
            raise KeyError('Ключ "data" не найден в response_json')
        else:
            data = response_json['data']
            free_services = {}
            services = data.get('services')
            for item in services:
                free_services[item.get('title')] = str(item.get('id'))
            return free_services
    except ConnectionError as error:
        logger.error(f'Ошибка соединения: {error}')
    except Timeout as error:
        logger.error(f'Превышено время ожидания ответа: {error}')


async def create_session_api(data):
    try:
        if not data:
            logger.error('В "data" отсутствуют данные!')

        time = data['time']
        year, month, day = data['date'].split('-')
        date_iso8601 = return_date_iso8601(year, month, day, time)
        service_id = get_free_services(data['staff_id'])[data['service_title']]

        url = f'https://api.yclients.com/api/v1/book_record/{COMPANY_ID}/'
        data_for_request = {
            "phone": data['phone'],
            "fullname": data['name'],
            "email": "",
            "comment": "",
            "type": "mobile",
            "notify_by_sms": 2,
            "notify_by_email": 24,
            "appointments": [
                {
                    "id": 1,
                    "services": [
                        service_id
                    ],
                    "staff_id": int(data['staff_id']),
                    "datetime": date_iso8601,
                }
            ]
            }

        response = requests.post(url, headers=headers, json=data_for_request)
        if response.status_code != HTTPStatus.CREATED:
            logger.error(
                f'Bad response: {response.status_code}:{response.text}')
            return response
        return response
    except ConnectionError as error:
        logger.error(f'Ошибка соединения: {error}')
    except Timeout as error:
        logger.error(f'Превышено время ожидания ответа: {error}')


def get_ycl_id(state_data: dict):
    url = f'https://api.yclients.com/api/v1/company/{COMPANY_ID}/clients/search'
    data_for_request = {
        "page": 1,
        "fields": [
            "id",
            "name",
            "phone"
        ],
        "order_by": "name",
        "order_by_direction": "desc",
        "operation": "AND"
    }
    response = requests.post(url, headers=headers, json=data_for_request)
    response_json = response.json()
    data = response_json['data']
    clients = {}
    for client in data:
        clients[client.get('phone')] = client.get('id')
    phone = state_data['phone']
    ycl_id = clients.get(phone)
    return ycl_id


def get_all_records_by_client(ycl_id):
    url = f'https://api.yclients.com/api/v1/records/{COMPANY_ID}?client_id={ycl_id}'
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
    url = f'https://api.yclients.com/api/v1/record/{COMPANY_ID}/{record_id}'
    response = requests.get(url, headers=headers)
    response_json = response.json()
    print(response_json)
    record = {}
    data = response_json['data']
    print(data)
    services = data['services']
    print(services)
    staff = data['staff']
    client = data['client']
    print(staff)
    record['service_id'] = services[0]['id']
    record['title'] = services[0]['title']
    record['cost'] = services[0]['cost']
    record['name_staff'] = staff['name']
    record['staff_id'] = staff['id']
    record['client_id'] = client['id']
    record['date'] = data['date']
    record['seance_length'] = data['seance_length']
    return record


def edit_record(state_data):
    record_id = state_data['record_id']
    date = state_data['new_date']
    time = state_data['new_time']
    datetime = date + time
    url = f'https://api.yclients.com/api/v1/record/{COMPANY_ID}/{record_id}'

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
    url = f'https://api.yclients.com/api/v1/record/{COMPANY_ID}/{record_id}'
    response = requests.delete(url, headers=headers)
