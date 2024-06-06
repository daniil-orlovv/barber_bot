import requests

from config_data.config import COMPANY_ID, PARTNER_TOKEN
from api.settings_api import urls


headers = {
    'Authorization': f'Bearer {PARTNER_TOKEN}',
    'Accept': 'application/vnd.api.v2+json',
    'Content-type': 'application/json'
}


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
