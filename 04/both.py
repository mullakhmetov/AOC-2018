import re
import sys
import datetime
from collections import namedtuple, defaultdict, Counter

from pprint import pprint


RECORD_RE = re.compile(r'\[(.+)\].+((\#\d+)|(wakes|falls))')
Record = namedtuple('Record', ['id', 'dt', 'action'])


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).total_seconds() / 60)):
        yield start_date + datetime.timedelta(minutes=n)


def parse_record(record):
    m = RECORD_RE.match(record)
    dt, id_or_action = m.group(1), m.group(2)
    dt = datetime.datetime.fromisoformat(dt)
    id_ = action = None
    if '#' in id_or_action:
        id_ = id_or_action[1:]
        action = 'start'
    else:
        action = id_or_action

    return Record(id_, dt, action)


def main():
    with open('input.txt', 'r') as f:
        # ascending order by datetime
        records = sorted([parse_record(l.strip()) for l in f.readlines() if l.strip()], key=lambda r: r.dt)

    id_periods_d = defaultdict(list) # id: [dt, ...]
    current_id = None
    for record in records:
        if record.action == 'start':
            current_id = record.id
            continue

        id_periods_d[current_id].append(record.dt)

    asleep_minutes_count = defaultdict(int)
    id_asleep_minutes_d = defaultdict(Counter)
    for id_, periods in id_periods_d.items():
        # every odd datetime in periods is asleep dt and every even dt is awake one
        # pair them by zip
        for start, end in zip(periods[::2], periods[1::2]):
            asleep_minutes_count[id_] += (end - start).total_seconds() / 60
            for dt in daterange(start, end):
                id_asleep_minutes_d[id_].update([dt.minute])

    # descending order by total asleep minutes
    part_1_res_id = sorted(asleep_minutes_count.items(), key=lambda x: x[1], reverse=True)[0][0]
    # most_common item is like (%minute%, %occurrences_count%)
    part_1_res_minute = id_asleep_minutes_d[part_1_res_id].most_common()[0][0]
    part_1_res = int(part_1_res_id) * part_1_res_minute
    print(f'part 1: {part_1_res}')

    # descending order by most frequently asleep minute
    part_2_res_id, counter = sorted(id_asleep_minutes_d.items(), key=lambda x: x[1].most_common()[0][1], reverse=True)[0]
    part_2_res_minute = counter.most_common()[0][0]
    part_2_res = int(part_2_res_id) * part_2_res_minute
    print(f'part 2: {part_2_res}')


if __name__ == '__main__':
    main()
