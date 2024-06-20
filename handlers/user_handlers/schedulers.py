import datetime
from handlers.user_handlers.feedbacks import get_feedback
from handlers.user_handlers.notifications import (notify_day, notify_hour,
                                                  notify_month, notify_week)


def create_jobs(scheduler, bot, user_id, date_of_record):

    time_for_feedback = datetime.datetime(*date_of_record) + datetime.timedelta(hours=2)
    one_day_notice = datetime.datetime(*date_of_record) - datetime.timedelta(days=1)
    two_hours_notice = datetime.datetime(*date_of_record) - datetime.timedelta(hours=2)
    after_four_weeks = datetime.datetime(*date_of_record) + datetime.timedelta(weeks=4)
    after_four_monts = datetime.datetime(*date_of_record) + datetime.timedelta(weeks=16)

    scheduler.add_job(get_feedback, 'date',
                      run_date=time_for_feedback, jobstore='default',
                      args=[bot, user_id], id=f'feedback_{user_id}')
    scheduler.add_job(notify_day, 'date',
                      run_date=one_day_notice, jobstore='default',
                      args=[bot, user_id], id=f'notify_day_{user_id}')
    scheduler.add_job(notify_hour, 'date',
                      run_date=two_hours_notice, jobstore='default',
                      args=[bot, user_id], id=f'notify_hour_{user_id}')
    scheduler.add_job(notify_week, 'date',
                      run_date=after_four_weeks, jobstore='default',
                      args=[bot, user_id], id=f'notify_week_{user_id}')
    scheduler.add_job(notify_month, 'date',
                      run_date=after_four_monts, jobstore='default',
                      args=[bot, user_id], id=f'notify_month_{user_id}')


def rescheduler_jobs(scheduler, user_id, date_of_record):

    time_for_feedback = datetime.datetime(*date_of_record) + datetime.timedelta(hours=2)
    one_day_notice = datetime.datetime(*date_of_record) - datetime.timedelta(days=1)
    two_hours_notice = datetime.datetime(*date_of_record) - datetime.timedelta(hours=2)
    after_four_weeks = datetime.datetime(*date_of_record) + datetime.timedelta(weeks=4)
    after_four_monts = datetime.datetime(*date_of_record) + datetime.timedelta(weeks=16)

    scheduler.reschedule_job(
        job_id=f'feedback_{user_id}', trigger='date', run_date=time_for_feedback)
    scheduler.reschedule_job(
        job_id=f'notify_day_{user_id}', trigger='date', run_date=one_day_notice)
    scheduler.reschedule_job(
        job_id=f'notify_hour_{user_id}', trigger='date', run_date=two_hours_notice)
    scheduler.reschedule_job(
        job_id=f'notify_week_{user_id}', trigger='date', run_date=after_four_weeks)
    scheduler.reschedule_job(
        job_id=f'notify_month_{user_id}', trigger='date', run_date=after_four_monts)


def remove_jobs(scheduler, user_id):
    scheduler.remove_job(f'feedback_{user_id}')
    scheduler.remove_job(f'notify_day_{user_id}')
    scheduler.remove_job(f'notify_hour_{user_id}')
    scheduler.remove_job(f'notify_week_{user_id}')
    scheduler.remove_job(f'notify_month_{user_id}')
