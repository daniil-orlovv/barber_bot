import requests

from api.settings_api import urls
from config_data.config import COMPANY_ID, PARTNER_TOKEN

main_master = '3251813'


def get_feedback_master(mark, text, name, user_token):
    headers = {
        'Authorization': f'Bearer {PARTNER_TOKEN}, User {user_token}',
        'Accept': 'application/vnd.api.v2+json',
        'Content-type': 'application/json'
    }
    staff_id = main_master
    url = urls['get_feedback_master'].format(COMPANY_ID, staff_id)
    data_for_request = {
        "mark": mark,
        "text": text,
        "name": name
    }
    requests.post(url, headers=headers, json=data_for_request)


def get_feedback_company(mark, text, name, user_token):
    headers = {
        'Authorization': f'Bearer {PARTNER_TOKEN}, User {user_token}',
        'Accept': 'application/vnd.api.v2+json',
        'Content-type': 'application/json'
    }
    url = urls['get_feedback_company'].format(COMPANY_ID)
    data_for_request = {
        "mark": mark,
        "text": text,
        "name": name
    }
    requests.post(url, headers=headers, json=data_for_request)
