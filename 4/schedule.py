import re
import sys


def parse_entry(entry):
    digits = re.findall(r'\d+', entry)

    if 'begins shift' in entry:
        return {'action': 'start', 'id': int(digits[-1]), 'time': [int(d) for d in digits[0:5]]}
    elif 'wakes' in entry:
        return {'action': 'wake', 'time': [int(d) for d in digits[0:5]]}
    elif 'falls' in entry:
        return {'action': 'sleep', 'time': [int(d) for d in digits[0:5]]}
    else:
        raise ValueError('Unhandled line')


def solution():
    # Get sorted schedule
    schedule = []
    guards = set()
    for line in sys.stdin:
        parsed = parse_entry(line)
        if parsed['action'] == 'start' and parsed['id'] not in guards:
            guards.add(parsed['id'])
        schedule.append(parsed)

    schedule.sort(key=lambda x: x['time'])

    # Setup variables for guards
    sleep = {guard_id: [0]*60 for guard_id in guards}

    current_guard = None
    current_sleep_time = None
    for entry in schedule:
        if entry['action'] == 'start':
            current_guard = entry['id']
        elif entry['action'] == 'sleep':
            current_sleep_time = entry['time'][4]
        elif entry['action'] == 'wake':
            for minute in list(range(current_sleep_time, entry['time'][4])):
                sleep[current_guard][minute] += 1
            current_sleep_time = None

    # Find guard with max sleep and most common minute
    most_minutes = 0
    max_guard = None
    sleepiest_minute = 0
    for guard, minutes in sleep.items():
        if sum(minutes) > most_minutes:
            most_minutes = sum(minutes)
            max_guard = guard
            sleepiest_minute = minutes.index(max(minutes))

    print(f'Guard {max_guard} slept {most_minutes} minutes and his most slept minute was {sleepiest_minute}')
    print(max_guard*sleepiest_minute)

    # Find guard most often asleep on the same minute
    max_guard = None
    max_minute_value = 0
    max_minute = 0
    for guard, minutes in sleep.items():
        if max(minutes) > max_minute_value:
            max_guard = guard
            max_minute = minutes.index(max(minutes))
            max_minute_value = max(minutes)

    print(f'Guard {max_guard} spent minute {max_minute} asleep {max_minute_value} times')
    print(max_guard*max_minute)

solution()