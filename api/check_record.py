import requests

from config_data.config import COMPANY_ID, PARTNER_TOKEN
from utils.utils import return_date_iso8601

headers = {
    'Authorization': f'Bearer {PARTNER_TOKEN}',
    'Accept': 'application/vnd.api.v2+json',
    'Content-type': 'application/json'
}
url = f'https://api.yclients.com/api/v1/book_check/{COMPANY_ID}'


def check_record_for_create(state_data):
    time = state_data['time']
    year, month, day = state_data['date'].split('-')
    date_iso8601 = return_date_iso8601(year, month, day, time)
    service_id = state_data['service_id']
    staff_id = state_data['staff_id']
    body = {
        "appointments": [
            {
                "id": 1,
                "services": [
                    service_id
                ],
                "staff_id": staff_id,
                "datetime": date_iso8601
                }
        ]
    }
    response = requests.post(url, headers=headers,
                             json=body)
    return response
