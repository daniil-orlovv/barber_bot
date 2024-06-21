

def get_data_and_user_id(state_data, callback):
    date_record = state_data['date']
    date_record_split = date_record.split('-')
    time_record = state_data['time']
    time_record_split = time_record.split(':')
    date_of_record = date_record_split + time_record_split
    date_of_record = [int(x) for x in date_of_record]
    user_id = callback.from_user.id
    return date_of_record, user_id


def get_new_data_and_user_id(state_data, callback):
    date_record = state_data['new_date']
    date_record_split = date_record.split('-')
    time_record = state_data['new_time']
    time_record_split = time_record.split(':')
    date_of_record = date_record_split + time_record_split
    date_of_record = [int(x) for x in date_of_record]
    user_id = callback.from_user.id
    return date_of_record, user_id
