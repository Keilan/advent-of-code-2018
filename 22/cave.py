import tqdm
import numpy as np
from sortedcontainers import SortedList

INFINITY = 1000000000  # Used for costs of impossible things
equipment_to_int = {
    'torch': 0,
    'climb': 1,
    'neither': 2
}
int_to_equipment = {v: k for k, v in equipment_to_int.items()}


def get_erosion_level(x, y, cave, depth, target):
    # Geologic index
    gi = None
    if (x, y) == (0, 0) or (x, y) == target:
        gi = 0
    elif x == 0:
        gi = y * 48271
    elif y == 0:
        gi = x * 16807
    else:
        gi = cave[x-1, y] * cave[x, y-1]

    # Erosion Level
    el = (gi + depth) % 20183
    return el


def movement_cost_function(type1, type2, equipment):
    """
    The cost of moving from an area of type 1 to type 2 where 0 is rocky, 1 is wet, and 2 is narrow.
    """
    if type1 == type2:
        return 1

    # There is only one common item between 2 different regions, so the direction isn't important
    type1, type2 = sorted([type1, type2])

    if type1 == 0 and type2 == 1 and equipment == 'climb':
        return 1
    elif type1 == 0 and type2 == 2 and equipment == 'torch':
        return 1
    elif type1 == 1 and type2 == 2 and equipment == 'neither':
        return 1

    return INFINITY  # Other movements are impossible


def tool_cost_function(terrain, tool):
    if terrain == 0 and tool in ['climb', 'torch']:
        return 7
    elif terrain == 1 and tool in ['climb', 'neither']:
        return 7
    elif terrain == 2 and tool in ['torch', 'neither']:
        return 7

    return INFINITY  # Other changes are impossible


def find_shortest_time(source, target, cave):
    """
    Use a modified version of Djikstra's algorithm.
    """
    # Initialize algorithm
    unvisited = set()
    distances = {}
    options = SortedList()  # Used for finding minimum - stores in format (distance, x, y, t)
    for x in range(cave.shape[0]):
        for y in range(cave.shape[1]):
            for t in equipment_to_int.values():
                unvisited.add((x, y, t))
                distances[(x, y, t)] = float('inf')
    progress_bar = tqdm.tqdm(total=len(unvisited))

    # Set source to 0
    distances[source[0], source[1], equipment_to_int['torch']] = 0
    options.add((0, source[0], source[1], equipment_to_int['torch']))

    # Iterate through set
    while unvisited:
        # Find unvisited node with minimum distance
        selected = options[0]
        selected_distance, sel_x, sel_y, sel_t = selected

        unvisited.remove((sel_x, sel_y, sel_t))
        options.remove(selected)
        progress_bar.update(1)

        # Update all by movement neighbours
        for x, y in [(sel_x+1, sel_y), (sel_x, sel_y+1), (sel_x-1, sel_y), (sel_x, sel_y-1)]:
            if (x, y, sel_t) in unvisited:
                # Compute time to move to this node
                time_to_move = movement_cost_function(cave[sel_x, sel_y], cave[x, y],
                                                       int_to_equipment[sel_t])
                new_distance = selected_distance + time_to_move

                # Set updated distance if new distance
                if new_distance < distances[(x, y, sel_t)]:
                    # Update options for minimum computation
                    options.discard((distances[x, y, sel_t], x, y, sel_t))
                    options.add((new_distance, x, y, sel_t))

                    distances[(x, y, sel_t)] = new_distance

        # Update all equipment neighbours
        for t in range(3):

            # Changing to the current tool makes no sense
            if t == sel_t:
                continue

            if (sel_x, sel_y, t) in unvisited:
                # Compute time to change
                time_to_change = tool_cost_function(cave[sel_x, sel_y], int_to_equipment[t])
                new_distance = selected_distance + time_to_change

                if new_distance < distances[(sel_x, sel_y, t)]:
                    # Update options for minimum computation
                    options.discard((distances[sel_x, sel_y, t], sel_x, sel_y, t))
                    options.add((new_distance, sel_x, sel_y, t))

                    distances[(sel_x, sel_y, t)] = new_distance

    progress_bar.close()
    return distances[(target[0], target[1], equipment_to_int['torch'])]


def cave(depth, target):
    # Create a numpy array from the cave mouth to the target - buffer of 100 for part 2
    cave = np.full([target[0] + 100, target[1] + 1000], -1)
    print('Traversing cave with shape {}.'.format(cave.shape))

    # Iterate over cave, filling in x and y values
    for x in range(cave.shape[0]):
        for y in range(cave.shape[1]):
            cave[x, y] = get_erosion_level(x, y, cave, depth, target)

    # Take the values mod 3 to get erosion levels
    cave %= 3

    print('The sum of risk levels is {}.'.format(cave[0:target[0]+1, 0:target[1]+1].sum()))

    # Use Djikstra's algorithm to find the fastest path
    time = find_shortest_time((0, 0), target, cave)
    print('The fastest time to reach the target is {} minutes.'.format(time))


def print_cave(cave):
    symbols = {
        0: '.',
        1: '=',
        2: '|',
    }

    for row in np.transpose(cave):
        output = ''
        for c in row:
            output += symbols[c]
        print(output)


cave(3066, (13, 726))
