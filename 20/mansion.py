import sys

import numpy as np


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return '({},{})'.format(self.x, self.y)


def read_directions(directions):
    result_stack = [] # Tracks the full set of results, each layer is the parent of the one after
    current_path = None # The path we are currently on
    branch_choices = None # The branches in the current branch statement

    for current in directions:
        if current in ['N', 'E', 'S', 'W']:
            current_path.append(current)

        elif current == '(' or current == '^':
            if current_path is not None:
                result_stack.append((current_path, branch_choices))
            current_path = []
            branch_choices = None

        elif current == ')' or current == '$':
            if branch_choices is not None:
                branch_choices.append(current_path)
            finished_path = branch_choices

            # Break out of the current layer, or do nothing if this is the highest layer
            if result_stack:
                current_path, branch_choices = result_stack.pop()
                current_path.append(finished_path)

        elif current == '|':
            branch_choices = [] if branch_choices is None else branch_choices
            branch_choices.append(current_path)
            current_path = []

    return current_path


def resize_map(mansion, pos, amount):
    # Create a new map and place the old one inside of it
    new_size = len(mansion) + amount*2
    new_mansion = np.full([new_size, new_size], '?', dtype=np.str)
    new_mansion[amount:amount+len(mansion), amount:amount+len(mansion)] = mansion

    new_pos = Point(pos.x+amount, pos.y+amount)
    return new_pos, new_mansion


def update_map(mansion, pos, direction):
    # Scale the map size if necessary
    current_size = len(mansion)
    if pos.x < 3 or pos.x > current_size-4 or pos.y < 3 or pos.y > current_size-4:
        pos, mansion = resize_map(mansion, pos, 2)

    if direction == 'N':
        mansion[pos.x, pos.y-2:pos.y] = ['.','-']
        pos.y -= 2

    elif direction == 'E':
        mansion[pos.x+1:pos.x+3, pos.y] = ['|','.']
        pos.x += 2

    elif direction == 'S':
        mansion[pos.x, pos.y+1:pos.y+3] = ['-', '.']
        pos.y += 2

    elif direction == 'W':
        mansion[pos.x-2:pos.x, pos.y] = ['.', '|']
        pos.x -= 2

    return pos, mansion

#def progress(cur_x, cur_y, directions):
    #if directions is empty:
        #return

    #current = directions[0]
    #while current is a char:
        #Update map to move in that direction
        #Update position
        #progress(directions[1:])
        #current = directions[0]
    #if current is a list:
        #for option in current:
            #progress(cur_x, cur_y, [option] + direction[1:])


def add_walls(mansion, pos):
    # Add Walls
    current_size = len(mansion)
    for x in range(current_size):
        for y in range(current_size):
            subregion = mansion[max(x-1, 0):x+2, max(y-1, 0):y+2]
            if mansion[x, y] == '?' and not ((subregion=='?') | (subregion=='#')).all():
                mansion[x, y] = '#'

    # Trim unused rows, first seeing how many rows will be trimmed to update pos
    trimmed_x = mansion[:pos.x][np.all(mansion[:pos.x] == '?', axis=1)].shape[0]
    trimmed_y = mansion[:,:pos.y][:, np.all(mansion[:,:pos.y] == '?', axis=0)].shape[1]
    pos.x -= trimmed_x
    pos.y -= trimmed_y

    mansion = mansion[~np.all(mansion == '?', axis=1)]
    mansion = mansion[:, ~np.all(mansion == '?', axis=0)]
    return pos, mansion


def print_mansion(mansion, pos=None):
    copy = mansion.copy()

    if pos:
        copy[pos.x, pos.y] = 'X'

    for row in np.transpose(copy):
        print(''.join(row))


def mansion(regex):
    # Read directions
    directions = read_directions(regex)

    # Create a map, start at size 10 (to grow as needed) and start in the middle
    mansion = np.full([5, 5], '?', dtype=np.str)
    pos = Point(2, 2)
    mansion[pos.x, pos.y] = '.' # Starting point

    pos, mansion = update_map(mansion, pos, 'S')
    pos, mansion = update_map(mansion, pos, 'S')
    pos, mansion = update_map(mansion, pos, 'S')

    pos, mansion = add_walls(mansion, pos)
    print_mansion(mansion, pos)


if __name__ == '__main__':
    mansion('^WNE$')
    #mansion('^N(E|W(N|S))N$')
    #mansion('^ENWWW(NEEE|SSE(EE|N))$')
    #mansion('^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$')