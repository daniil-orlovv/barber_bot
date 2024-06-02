import requests


USER_TOKEN = '420ab5c67606ab449059fa89baa35ed7'
PARTNER_TOKEN = 'cc9arzfwhzmcyd9rzdpu'
COMPANY_ID = '1055113'

headers = {
    'Authorization': f'Bearer {PARTNER_TOKEN}, User {USER_TOKEN}',
    'Accept': 'application/vnd.api.v2+json',
    'Content-type': 'application/json'
}


def create_list_records_of_company


def get_all_records_of_client_by_company():
    url = 'https://api.yclients.com/api/v1/user/records/'
    response = requests.get(url, headers=headers)
    response_json = response.json()
    records = response_json['data']
    print(records)
    client_records = []
    for record in records:
        print(record)
        company = record['company']
        print(company)
        id_company = company['id']
        print(id_company)
        if str(id_company) != COMPANY_ID:
            continue
        else:
            client_records.append(record)
    return client_records


print(f'Записи по моей компании: {get_all_records_of_client_by_company()}')
