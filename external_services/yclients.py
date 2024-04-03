import os
import requests
import datetime

from dotenv import load_dotenv
from config_data.config import BASE_URL

load_dotenv()
PARTNER_TOKEN = os.getenv('PARTNER_TOKEN', default='partner_key')
USER_TOKEN = os.getenv('USER_TOKEN', default='user_token')
COMPANY_ID = os.getenv('COMPANY_ID', default='company_id')

current_year = datetime.datetime.now().year
company_id = COMPANY_ID
headers = {
    'Authorization': f'Bearer {PARTNER_TOKEN}, User {USER_TOKEN}',
    'Accept': 'application/vnd.api.v2+json'
}


def get_free_staff():
    url = f'{BASE_URL}/company/{company_id}/staff/'
    response = requests.get(url, headers=headers)
    response_json = response.json()
    staffs = {}

    if 'data' in response_json:
        data = response_json['data']
        for item in data:
            staffs[item.get('name')] = str(item.get('id'))

    return staffs


def get_free_date(staff_id):
    url = f'{BASE_URL}/book_dates/{company_id}?staff_id={staff_id}'
    response = requests.get(url, headers=headers)
    response_json = response.json()

    if 'data' in response_json and 'booking_days' in response_json['data']:
        booking_days = response_json['data']['booking_days']
        quoted_dict = {
            key: [
                str(item) for item in value
            ] for key, value in booking_days.items()
        }

        return quoted_dict


def get_free_time(staff_id, date):
    url = f'{BASE_URL}/book_times/{company_id}/{staff_id}/{date}?'
    response = requests.get(url, headers=headers)
    response_json = response.json()

    if 'data' in response_json:
        data = response_json['data']
        free_times = []
        for item in data:
            free_times.append(item.get('time'))
    return free_times


def get_free_services(staff_id):
    url = f'{BASE_URL}/book_services/{company_id}?staff_id={staff_id}'
    response = requests.get(url, headers=headers)
    response_json = response.json()
    if 'data' in response_json:
        data = response_json['data']
        free_services = {}
        services = data.get('services')
        for item in services:
            free_services[item.get('title')] = str(item.get('id'))
    return free_services


async def create_session_api(data):

    time = data['time']
    year, month, day = data['date'].split('-')
    date_iso8601 = f'{year}-{int(month):02}-{int(day):02}T{time}:00+0300'
    service_id = get_free_services(data['staff_id'])[data['service_title']]

    url = f'https://api.yclients.com/api/v1/book_record/{company_id}/'
    data_for_request = {
        "phone": data['phone'],
        "fullname": data['name'],
        "email": data['email'],
        # "code": "38829",
        "comment": data['comment'],
        "type": "mobile",
        "notify_by_sms": 2,
        "notify_by_email": 24,
        # "api_id": "777",  # Необязательный параметр
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

    requests.post(url, headers=headers, json=data_for_request)
