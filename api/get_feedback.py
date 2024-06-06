import requests

from config_data.config import COMPANY_ID, PARTNER_TOKEN
from api.settings_api import urls


main_master = '3251813'


def feedback(mark, text, name, user_token):
    headers = {
        'Authorization': f'Bearer {PARTNER_TOKEN}, User {user_token}',
        'Accept': 'application/vnd.api.v2+json',
        'Content-type': 'application/json'
    }
    staff_id = main_master
    url = urls['feedback'].format(COMPANY_ID, staff_id)
    data_for_request = {
        "mark": mark,
        "text": text,
        "name": name
    }
    response = requests.post(
        url, headers=headers, json=data_for_request)
    print(response.text)
