import requests
import datetime
from config_data.config import COMPANY_ID, PARTNER_TOKEN


current_year = datetime.datetime.now().year


def edit_record(state_data, user_token):

    headers = {
        'Authorization': f'Bearer {PARTNER_TOKEN}, User {user_token}',
        'Accept': 'application/vnd.api.v2+json',
        'Content-type': 'application/json'
    }

    record_id = state_data['record_id']
    date = state_data['new_date']
    time = state_data['new_time']
    datetime = date + time
    url = f'https://api.yclients.com/api/v1/book_record/{COMPANY_ID}/{record_id}'

    data_for_request = {
        "datetime": datetime
    }
    response = requests.put(url, headers=headers,
                            json=data_for_request)
    return response.text
