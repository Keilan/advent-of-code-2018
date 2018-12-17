import re
import sys

import numpy as np


def read_map():
    # Read input and find edges and lowest point
    min_x, max_x, min_y, max_y = 500, 500, 0, 0
    veins = []
    for line in sys.stdin:
        digits = [int(i) for i in re.findall('\d+', line)]
        fixed_axis = line[0]
        fixed_point = digits[0]
        vein_range = (digits[1], digits[2])

        if fixed_axis == 'x':
            min_x = min(min_x, fixed_point)
            max_x = max(max_x, fixed_point)
            for y in vein_range:
                min_y = min(min_y, y)
                max_y = max(max_y, y)

        elif fixed_axis == 'y':
            min_y = min(min_y, fixed_point)
            max_y = max(max_y, fixed_point)
            for x in vein_range:
                min_x = min(min_x, x)
                max_x = max(max_x, x)

        veins.append((fixed_axis, fixed_point, vein_range))

    # Create matrix - note the various constant additions are to leave exactly one empty column on
    # each side of the final output
    ground_map = np.full([max_x-min_x+3, max_y+2], '.')
    for fixed_axis, fixed_point, vein_range in veins:
        if fixed_axis == 'x':
            ground_map[fixed_point-min_x+1, vein_range[0]:vein_range[1]+1].fill('#')
        elif fixed_axis == 'y':
            ground_map[vein_range[0]-min_x+1:vein_range[1]-min_x+2, fixed_point].fill('#')

    # Calculate the spring location using the scaling given
    spring = 500 - min_x + 1

    return spring, min_y, max_y, ground_map


def print_map(ground_map, spring=None):
    copy = ground_map.copy()
    if spring:
        copy[spring, 0] = '+'

    for row in np.transpose(copy):
        print(''.join(row))
    print()


# Helper functions for flow simulation
def find_boundaries(x, y, ground_map):
    """
    Returns two tuples for the left and right, each containing an x position and string
    indicating if that position is a 'wall' or a 'drop'.
    """
    initial_x = x

    # Find Left boundary
    left_boundary = None
    while left_boundary is None:
        x -= 1
        if ground_map[x, y] == '#':
            left_boundary = (x, 'wall')
        if ground_map[x, y] in '.' and ground_map[x, y+1] == '.':
            left_boundary = (x, 'drop')

    # Find Right boundary
    right_boundary = None
    while right_boundary is None:
        x += 1
        try:
            if ground_map[x, y] == '#':
                right_boundary = (x, 'wall')
        except:
            # Debugging issue - seems related to hitting existing streams
            print_map(ground_map[x-5:x,y-3:y+3])
        if ground_map[x, y] == '.' and ground_map[x, y+1] == '.':
            right_boundary = (x, 'drop')

    return left_boundary, right_boundary


def simulate_flow(ground_map, spring, lower_bound):
    # Track list of sources that still need to be processed - allows us to handle multiple
    # spillover points one at a time
    sources = {(spring, 0)}

    while len(sources) > 0:
        source = sources.pop()
        reached_bound = False
        x, y = source

        # Find floor
        while ground_map[x, y+1] == '.':
            if y == lower_bound:
                reached_bound = True
                break

            y += 1
            ground_map[x, y] = '|'

        # Repeatedly find boundaries until there is a spill
        if not reached_bound:
            left, right = find_boundaries(x, y, ground_map)
            while left[1] == 'wall' and right[1] == 'wall':
                # Fill in tiles
                ground_map[left[0]+1:right[0], y].fill('~')

                # Move up and repeat
                y -= 1
                left, right = find_boundaries(x, y, ground_map)

            if left[1] == 'drop' and right[1] == 'wall':
                ground_map[left[0]:right[0], y].fill('|')
                sources.add((left[0], y))
            elif left[1] == 'wall' and right[1] == 'drop':
                ground_map[left[0]+1:right[0]+1, y].fill('|')
                sources.add((right[0], y))
            elif left[1] == 'drop' and right[1] == 'drop':
                ground_map[left[0]:right[0]+1, y].fill('|')
                sources.add((left[0], y))
                sources.add((right[0], y))

def water():
    spring, min_y, max_y, ground_map = read_map()
    #print_map(ground_map, spring)
    simulate_flow(ground_map, spring, max_y)
    print_map(ground_map, spring)
    #count_water_tiles(ground_map)


water()

# Account for min y in case there's a gap between the spring and the first basin