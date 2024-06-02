import requests

from config_data.config import COMPANY_ID
from external_services.settings_api import urls, headers


main_master = '3251813'


def get_all_services():
    url = urls['get_all_services'].format(COMPANY_ID)
    response = requests.get(url, headers=headers)
    response_json = response.json()
    data = response_json['data']
    services = data['services']
    info_service = {}
    for service in services:
        info_service[service['title']] = service['price_min']
    return info_service


def feedback(mark, text, name):
    staff_id = main_master
    url = urls['feedback'].format(COMPANY_ID, staff_id)
    data_for_request = {
        "mark": mark,
        "text": text,
        "name": name
    }
    response = requests.post(url, headers=headers, json=data_for_request)
    print(response.text)
