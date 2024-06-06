import requests
from config_data.config import PARTNER_TOKEN


def delete_record(record_id, user_token):
    headers = {
        'Authorization': f'Bearer {PARTNER_TOKEN}, User {user_token}',
        'Accept': 'application/vnd.api.v2+json',
        'Content-type': 'application/json'
    }
    url = f'https://api.yclients.com/api/v1/user/records/{record_id}'
    requests.delete(url, headers=headers)
