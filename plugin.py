import copy, datetime
from dateutil import rrule
from recurrent.event_parser import RecurringEvent
from beancount.core import data


__plugins__ = [ 'repete', ]

REPETE = 'repete'

def repete(entries, options):
    new_entries = []
    rubbish_bin = []
    for txn in data.filter_txns(entries):
        if REPETE in txn.meta:
            rubbish_bin.append(txn)
            re = RecurringEvent(now_date=txn.date)
            re.parse(txn.meta[REPETE])
            for i in rrule.rrulestr(re.get_RFC_rrule(), dtstart=txn.date):
                new = copy.deepcopy(txn)
                new = new._replace(date=i.date())
                del new.meta[REPETE]
                new_entries.append(new)

    for txn in rubbish_bin:
        entries.remove(txn)

    return entries + new_entries, []
