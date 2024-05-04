import requests

from config_data.config import COMPANY_ID
from external_services.settings_api import urls, headers


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
