import requests
import datetime
from config_data.config import COMPANY_ID

from api.settings_api import urls, headers


current_year = datetime.datetime.now().year


def edit_record(state_data):
    record_id = state_data['record_id']
    date = state_data['new_date']
    time = state_data['new_time']
    datetime = date + time
    url = urls['edit_record'].format(COMPANY_ID, record_id)

    data_for_request = {
        "staff_id": state_data['staff_id'],
        "services": [{
                "id": state_data['service_id']
            }
        ],
        "client": {
            "id": state_data['client_id']
        },
        "datetime": datetime,  # "2024-05-09 17:00:00"
        "seance_length": state_data['seance_length']
    }
    response = requests.put(url, headers=headers, json=data_for_request)
    return response.text
