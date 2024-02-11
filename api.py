import os
import requests
from dotenv import load_dotenv
from config import BASE_URL

load_dotenv()
PARTNER_TOKEN = os.getenv('PARTNER_TOKEN', default='partner_key')
USER_TOKEN = os.getenv('USER_TOKEN', default='user_token')


company_id = 977067
staff_id = 2933362
url = 'https://api.yclients.com/api/v1/book_record/977067/'
headers = {
    'Authorization': f'Bearer {PARTNER_TOKEN}, User {USER_TOKEN}',
    'Accept': 'application/vnd.api.v2+json'
}
# data = {
#   "phone": "79312608569",
#   "fullname": "Даниил",
#   "email": "test@yclients.com",
#   "code": "38829",
#   "comment": "Запись на стрижку!",
#   "type": "mobile",
#   "notify_by_sms": 6,
#   "notify_by_email": 24,
#   "api_id": "777",
#   "appointments": [
#     {
#       "id": 1,
#       "services": [
#         14531077
#       ],
#       "staff_id": 2933362,
#       "datetime": "2024-01-18T14:30:00.000Z",
#       "custom_fields": {
#         "my_custom_field": 123,
#         "some_another_field": [
#           "first value",
#           "next value"
#         ]
#       }
#     }
#   ]
# }

# response = requests.post(url, headers=headers, json=data)
# print(response.text)


def get_free_staff():
    url = f'{BASE_URL}/company/{company_id}/staff/'
    response = requests.get(url, headers=headers)
    response_json = response.json()
    names = []

    if 'data' in response_json:
        data = response_json['data']
        for item in data:
            names.append(item.get('name'))

    return names


def get_free_date():
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


def get_free_time(date):
    url = f'{BASE_URL}/book_times/{company_id}/{staff_id}/{date}?'
    response = requests.get(url, headers=headers)
    response_json = response.json()

    if 'data' in response_json:
        data = response_json['data']
        free_times = []
        for item in data:
            free_times.append(item.get('time'))
    return free_times


def get_free_services():
    url = f'{BASE_URL}/book_services/{company_id}?staff_id={staff_id}'
    response = requests.get(url, headers=headers)
    response_json = response.json()
    if 'data' in response_json:
        data = response_json['data']
        free_services = []
        services = data.get('services')
        for service in services:
            free_services.append(service.get('title'))
    return free_services
