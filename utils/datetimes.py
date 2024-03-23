'''
datetimes.py
This module is from samueva97.
Do not modify it
'''
from datetime import datetime
from datetime import timezone



def now():
    '''
    Returns actual datetime in utc

    Returns
    -------
    datetime
    '''
    return datetime.now(timezone.utc)



def today():
    '''
    Returns actual day datetime on 00:00:00

    Returns
    -------
    datetime
    '''
    return now().replace(hour=0, minute=0, second=0, microsecond=0)



def from_timestamp(timestamp):
    '''
    Returns datetime from a utc timestamp

    Returns
    -------
    datetime
    '''
    return datetime.fromtimestamp(timestamp, timezone.utc)
