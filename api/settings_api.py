from config_data.config import PARTNER_TOKEN, USER_TOKEN

headers_for_create = {
    'Authorization': f'Bearer {PARTNER_TOKEN}',
    'Accept': 'application/vnd.api.v2+json',
    'Content-type': 'application/json'
}


headers_for_edit = {
    'Authorization': f'Bearer {PARTNER_TOKEN}',
    'Accept': 'application/vnd.api.v2+json',
    'Content-type': 'application/json'
}


headers_for_get = {
    'Authorization': 'Bearer {PARTNER_TOKEN}, User {}',
    'Accept': 'application/vnd.api.v2+json',
    'Content-type': 'application/json'
}

headers_for_cancel = {
    'Authorization': 'Bearer {PARTNER_TOKEN}, User {}',
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
    'edit_record':
        'https://api.yclients.com/api/v1/record/{}/{}',
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
