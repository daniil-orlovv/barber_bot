import requests
import json
import calendar



company_id = 977067
url = 'https://api.yclients.com/api/v1/book_record/977067/'
headers = {
    'Authorization': 'Bearer 2k3ub5wjf96f8fytz6eu, User ea1aa4b4bbe452623b8098776499b52d',
    'Accept': 'application/vnd.api.v2+json'
}
# data = {
#   "phone": "79312608569",
#   "fullname": "Даниил",
#   "email": "test@yclients.com",
#   "code": "38829",
#   "comment": "Запись на стрижку!",
#   "type": "mobile",
#   "notify_by_sms": 6,
#   "notify_by_email": 24,
#   "api_id": "777",
#   "appointments": [
#     {
#       "id": 1,
#       "services": [
#         14531077
#       ],
#       "staff_id": 2933362,
#       "datetime": "2024-01-18T14:30:00.000Z",
#       "custom_fields": {
#         "my_custom_field": 123,
#         "some_another_field": [
#           "first value",
#           "next value"
#         ]
#       }
#     }
#   ]
# }

# response = requests.post(url, headers=headers, json=data)
# print(response.text)


def get_free_date():
    url = 'https://api.yclients.com/api/v1/book_dates/977067?staff_id=2933362'
    response = requests.get(url, headers=headers)
    response_json = response.json()

    if "data" in response_json and "booking_days" in response_json["data"]:
        booking_days = response_json["data"]["booking_days"]
        quoted_dict = {
            key: [
                str(item) for item in value
            ] for key, value in booking_days.items()
        }

        return quoted_dict


def get_free_time(date):
    url = f'https://api.yclients.com/api/v1/book_times/977067/2933362/{date}?'
    response = requests.get(url, headers=headers)
    response_json = response.json()

    if "data" in response_json:
        data = response_json['data']
        free_times = []
        for item in data:
            free_times.append(item.get('time'))
    return free_times
