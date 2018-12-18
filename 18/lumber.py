import sys

import numpy as np

SIZE = 50


def read_area():
    area = np.empty([SIZE, SIZE], dtype=np.str)
    for i, line in enumerate(sys.stdin):
        area[i] = list(line.strip())
    return area


def find_next(x, y, area):
    tile = area[x, y]
    subregion = area[max(x-1, 0):x+2, max(y-1, 0):y+2]

    # Find counts, subtract current to get surrounding
    unique, counts = np.unique(subregion, return_counts=True)
    counts = dict(zip(unique, counts))
    counts[tile] -= 1

    # Determine new square
    if tile == '.' and counts.get('|', 0) >= 3:
        return '|'
    elif tile == '|' and counts.get('#', 0) >= 3:
        return '#'
    elif tile == '#' and (counts.get('#', 0) < 1 or counts.get('|', 0) < 1):
        return '.'
    return tile


def advance_minute(area):
    result = np.empty([SIZE, SIZE], dtype=np.str)
    for x in range(SIZE):
        for y in range(SIZE):
            result[x, y] = find_next(x, y, area)
    return result


def print_area(area):
    for r in area:
        print(''.join(r))
    print()

def lumber():
    area = read_area()
    initial = area.copy()

    for minute in range(10):
        area = advance_minute(area)

    # Output after 10 minutes
    unique, counts = np.unique(area, return_counts=True)
    counts = dict(zip(unique, counts))
    value = counts["|"]*counts["#"]

    print(f'After 10 minutes, there are {counts["|"]} wooded acres and {counts["#"]} lumberyards.')
    print(f'The resource value after 10 minutes is {counts["|"]*counts["#"]}.')

    # The pattern stabilizes around minute 500, get a list around then to find pattern
    area = initial.copy()

    pattern = []
    for minute in range(600):
        area = advance_minute(area)

        if minute >= 499:
            unique, counts = np.unique(area, return_counts=True)
            counts = dict(zip(unique, counts))
            value = counts["|"]*counts["#"]

            pattern.append(value)

    # Find cycle length (using the 500th minute to the next time it appears)
    cycle_length = pattern.index(pattern[0], 1)

    # Use the cycle length to get a value in the range found in pattern
    repetitions = (1000000000 - 500) // cycle_length
    pattern_location = 1000000000 - repetitions * cycle_length
    value = pattern[pattern_location-500]
    print(f'The resource value after 1000000000 minutes is {value}.')


lumber()