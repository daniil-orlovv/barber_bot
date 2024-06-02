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
