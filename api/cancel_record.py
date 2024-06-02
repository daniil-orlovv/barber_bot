import requests
from config_data.config import COMPANY_ID

from api.settings_api import headers_for_cancel


def delete_record(record_id, user_token):
    headers = headers_for_cancel.format(user_token)
    url = f'https://api.yclients.com/api/v1/record/{COMPANY_ID}/{record_id}'
    requests.delete(url, headers=headers)
