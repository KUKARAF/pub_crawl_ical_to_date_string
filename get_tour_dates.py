#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests 
from icalendar import Calendar
import recurring_ical_events
from itertools import tee, zip_longest
from datetime import datetime, timedelta




start_date = (2022, 4, 1)
end_date =   (2022, 5, 5)


a = requests.get("https://calendar.google.com/calendar/ical/139jndekp3dp397hui1pk9pf7g%40group.calendar.google.com/public/basic.ics")
data = a.content

cal = Calendar.from_ical(data)


events = recurring_ical_events.of(cal).between(start_date, end_date)
out = []
for event in events:
    start = event["DTSTART"].dt
    duration = event["DTEND"].dt - event["DTSTART"].dt
    out.append(start)




# printing original list
#print(out)


one_day = timedelta(days=1)

def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip_longest(a, b, fillvalue=None)

def collapse_ranges(sorted_iterable, inc):
    pairs = pairwise(sorted_iterable)
    for start, tmp in pairs:
        if inc(start) == tmp:
            for end, tmp in pairs:
                if inc(end) != tmp:
                    break
            yield start, end
        else:
            yield start

dates = out

#numbers = [11, 1, 2, 3, 5, 5, 6, 22, 20, 21, 9, 7, 6]

if __name__ == '__main__':
    import pprint
    a = []
    for each in collapse_ranges(sorted(set(dates)), lambda d: d + one_day):
        if isinstance(each, datetime):
            a.append(each.strftime("%d.%m"))
        elif isinstance(each, tuple):
            s,e=each
            date_range = str(s.strftime("%d.%m")) +"-"+ str(e.strftime("%d.%m"))
            a.append(date_range)
    #for each in collapse_ranges(sorted(set(numbers)), (1).__add__):
     #   pprint.pprint(each)
    print("; ".join(a))
