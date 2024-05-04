from config_data.config import PARTNER_TOKEN, USER_TOKEN

headers = {
    'Authorization': f'Bearer {PARTNER_TOKEN}, User {USER_TOKEN}',
    'Accept': 'application/vnd.api.v2+json',
    'Content-type': 'application/json'
}

urls = {
    'get_free_staff':
        'https://api.yclients.com/api/v1/company/{}/staff/',
    'get_free_date':
        'https://api.yclients.com/api/v1/book_dates/{}?staff_id={}',
    'get_free_time':
        'https://api.yclients.com/api/v1/book_times/{}/{}/{}?',
    'get_free_services':
        'https://api.yclients.com/api/v1/book_services/{}?staff_id={}',
    'create_session_api':
        'https://api.yclients.com/api/v1/book_record/{}/',
    'get_ycl_id':
        'https://api.yclients.com/api/v1/company/{}/clients/search',
    'get_all_records_by_client':
        'https://api.yclients.com/api/v1/records/{}?client_id={}',
    'get_record_by_id':
        'https://api.yclients.com/api/v1/record/{}/{}',
    'edit_record':
        'https://api.yclients.com/api/v1/record/{}/{}',
    'delete_record':
        'https://api.yclients.com/api/v1/record/{}/{}'
}

request_body = {
    'create_session_api': {
            "phone": {},
            "fullname": {},
            "email": "",
            "comment": "",
            "type": "mobile",
            "notify_by_sms": 2,
            "notify_by_email": 24,
            "appointments": [
                {
                    "id": 1,
                    "services": [
                        {}
                    ],
                    "staff_id": int({}),
                    "datetime": {},
                }
            ]
    },
    'get_ycl_id': {
        "page": 1,
        "fields": [
            "id",
            "name",
            "phone"
        ],
        "order_by": "name",
        "order_by_direction": "desc",
        "operation": "AND"
    },
    'edit_record': {
        "staff_id": {},
        "services": [{
                "id": {}
            }
        ],
        "client": {
            "id": {}
        },
        "datetime": {},  # "2024-05-09 17:00:00"
        "seance_length": {}['seance_length']
    }
}
