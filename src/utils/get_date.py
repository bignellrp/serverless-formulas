import datetime
from datetime import date, timedelta

today = date.today()

def next_weekday(d, weekday):
    '''Takes in todays date and weekday 
    returns the required day in isoformat'''
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return d + timedelta(days_ahead)

##Games are played on wednesday 
##so returns next wednesday's date
next_wednesday = next_weekday(today, 2).isoformat()

def find_closest_wednesday(date):
    WEDNESDAY = 3
    year, week, day = date.isocalendar()
    delta = timedelta(days=WEDNESDAY-day)
    return date + delta

closest_wednesday = find_closest_wednesday(today)

def find_last_wednesday(today):
    offset = (today.weekday() - 2) % 7
    last_wednesday = today - datetime.timedelta(days=offset)
    return last_wednesday

last_wednesday = find_last_wednesday(today).isoformat()