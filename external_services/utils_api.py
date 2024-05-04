

def get_record(response):
    response_json = response.json()
    record = {}
    data = response_json['data']
    services = data['services']
    staff = data['staff']
    client = data['client']
    record['service_id'] = services[0]['id']
    record['title'] = services[0]['title']
    record['cost'] = services[0]['cost']
    record['name_staff'] = staff['name']
    record['staff_id'] = staff['id']
    record['client_id'] = client['id']
    record['date'] = data['date']
    record['seance_length'] = data['seance_length']
    return record
