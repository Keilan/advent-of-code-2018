import sys


def iterate_state(state, rules):
    result = ''
    for idx in range(0, len(state)):
        if idx < 2 or idx > len(state) - 3:
            result += '.'
            continue
        section = state[idx-2:idx+3]
        for r in rules:
            if section == r[0]:
                result += r[1]
                break
        else:
            result += '.'

    return result

def fast_sum(iterations=300):
    state = '#....#.....#......#....#....#.....#.......#.......#.......#....#....#....#.......#.......#........#.........#....#.....#.......#................................................'
    current = 266 + (iterations - 300)
    sum_points = 0
    for c in state:
        if c == '#':
            sum_points += current
        current += 1

    return sum_points

def day12():
    print(fast_sum(50000000000))
    initial_state = None
    rules = []
    for line in sys.stdin:
        if 'initial state' in line:
            initial_state = line.split()[2]
            initial_state = '.' * 5000 + initial_state + '.' * 5000
        elif '=>' in line:
            rules.append((line.split()[0], line.split()[-1]))

    state = initial_state
    for _ in range(600):
        state = iterate_state(state, rules)
    sum_points = 0
    current = -5000
    for c in state:
        if c == '#':
            sum_points += current
        current += 1
    print(sum_points)


    state = initial_state
    for _ in range(50000):
        state = iterate_state(state, rules)
        #print(state.find('#'))
        #import time
        #time.sleep(1)


        if _ > 300 and _ % 100 == 0:
            print(_)
            #print(state.find('#'), state.rfind('#'))
            #print(state[state.find('#'):state.rfind('#')+50])
            sum_points = 0
            current = -5000
            for c in state:
                if c == '#':
                    sum_points += current
                current += 1

            print(sum_points)
            print(fast_sum(_))
            print()

day12()
