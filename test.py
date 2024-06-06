date = '2024-6-20' # -> 2024-6-20 17:00
time = '17:00'
date_record = date
date_record_split = date_record.split('-')
time_record = time
time_record_split = time_record.split(':')
date_for_start_job = date_record_split + time_record_split
date_for_start_job = [int(x) for x in date_for_start_job]
print(date_for_start_job)
