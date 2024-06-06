from config_data.config import PARTNER_TOKEN


headers_bearer_token = {
    'Authorization': f'Bearer {PARTNER_TOKEN}',
    'Accept': 'application/vnd.api.v2+json',
    'Content-type': 'application/json'
}

headers_bearer_user_tokens = {
    'Authorization': 'Bearer {PARTNER_TOKEN}, User {}',
    'Accept': 'application/vnd.api.v2+json',
    'Content-type': 'application/json'
}


urls = {
    'get_free_staffs':
        'https://api.yclients.com/api/v1/book_staff/{}',
    'get_free_date':
        'https://api.yclients.com/api/v1/book_dates/{}?staff_id={}',
    'get_free_time':
        'https://api.yclients.com/api/v1/book_times/{}/{}/{}?',
    'get_free_services':
        'https://api.yclients.com/api/v1/book_services/{}?staff_id={}',
    'create_session_api':
        'https://api.yclients.com/api/v1/book_record/{}/',
    'get_all_services':
        'https://api.yclients.com/api/v1/book_services/{}',
    'feedback':
        'https://api.yclients.com/api/v1/comments/{}/{}'
}

request_body = {
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
    }
}
