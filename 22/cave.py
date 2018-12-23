import tqdm
import numpy as np


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


def get_movement_time(type1, type2, equipment, to_target=False):
    """
    Calculates the movement time switching equipment (if needed) and moving between regions, where
    0 is rocky, 1 is wet, and 2 is narrow. Note that moving to the target is a special case where
    the region is rocky but you still need to switch to the torch. The new equipment being used
    is also returned.
    """
    # If the types are the same, no change is needed
    if type1 == type2:
        time, equipment = 1, equipment
    else:
        # There is only one common item between 2 different regions, so the direction isn't important
        type1, type2 = sorted([type1, type2])

        if type1 == 0 and type2 == 1:
            time, equipment = 1 if equipment == 'climb' else 8, 'climb'  # Climbing gear is the common item
        elif type1 == 0 and type2 == 2:
            time, equipment = 1 if equipment == 'torch' else 8, 'torch'
        elif type1 == 1 and type2 == 2:
            time, equipment = 1 if equipment == 'neither' else 8, 'neither'
        else:
            raise ValueError('Invalid type combination')

    # If we're moving to the target and not using the torch, at 7 minutes to switch
    if to_target and equipment != 'torch':
        time += 7

    return time, equipment


def find_shortest_time(source, target, cave):
    """
    Use a modified version of Djikstra's algorithm"""

    # Initialize algorithm
    unvisited = set()
    distances = {}
    equipment = {}  #The possible equipped items at the shortest path to (x,y)
    for x in range(cave.shape[0]):
        for y in range(cave.shape[1]):
            distances[(x, y)] = float('inf')
            unvisited.add((x, y))
    progress_bar = tqdm.tqdm(total=len(unvisited))

    # Set source to 0
    distances[(source[0], source[1])] = 0
    equipment[(source[0], source[1])] = ['torch']

    # Iterate through set
    while unvisited:
        # Find unvisited node with minimum ditance
        options = [(k, v) for k, v in distances.items() if k in unvisited]
        selected, selected_distance = min(options, key=lambda x: x[1])
        equipment_options = equipment[selected]

        unvisited.remove(selected)
        progress_bar.update(1)

        # Update all neighbours
        sel_x, sel_y = selected
        for current_equipment in equipment_options:
            for x, y in [(sel_x+1, sel_y), (sel_x, sel_y+1), (sel_x-1, sel_y), (sel_x, sel_y-1)]:
                if (x, y) in unvisited:
                    # Compute time to move to this node
                    to_target = (x, y) == target
                    time_to_move, new_equipment = get_movement_time(cave[sel_x, sel_y], cave[x, y],
                                                                    current_equipment, to_target)
                    new_distance = selected_distance + time_to_move

                    # Set updated distance if new distance
                    if new_distance < distances[(x, y)]:
                        distances[(x, y)] = new_distance
                        equipment[(x, y)] = [new_equipment]  # Shorter distance, overwrite

                    elif (new_distance == distances[(x, y)] and
                          new_equipment not in equipment[(x, y)]):
                        equipment[(x, y)].append(new_equipment)  # Add to list of options

    progress_bar.close()
    return distances[target]


def cave(depth, target):
    # Create a numpy array from the cave mouth to the target - buffer of 100 for part 2
    cave = np.full([target[0] + 1, target[1] + 1], -1)

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


cave(510, (10, 10))
cave(3066, (13, 726))

# Wrong - 1019
# Wrong - 1007
