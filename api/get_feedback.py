import requests

from config_data.config import COMPANY_ID
from api.settings_api import urls, headers


main_master = '3251813'


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
