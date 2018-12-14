import sys
from enum import Enum
import numpy as np


class Direction(Enum):
    UP = '^'
    DOWN = 'v'
    LEFT = '<'
    RIGHT = '>'


class Turn(Enum):
    LEFT = 0
    STRAIGHT = 1
    RIGHT = 2


class Cart:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.turn = Turn.LEFT
        self.crashed = False

    def step(self, tracks):
        tile = tracks[self.x, self.y]

        # If turning, update direction
        if tile == '/':
            if self.direction == Direction.UP:
                self.direction = Direction.RIGHT
            elif self.direction == Direction.DOWN:
                self.direction = Direction.LEFT
            elif self.direction == Direction.LEFT:
                self.direction = Direction.DOWN
            elif self.direction == Direction.RIGHT:
                self.direction = Direction.UP

        elif tile == '\\':
            if self.direction == Direction.UP:
                self.direction = Direction.LEFT
            elif self.direction == Direction.DOWN:
                self.direction = Direction.RIGHT
            elif self.direction == Direction.LEFT:
                self.direction = Direction.UP
            elif self.direction == Direction.RIGHT:
                self.direction = Direction.DOWN

        elif tile == '+':
            if self.turn == Turn.LEFT:
                if self.direction == Direction.UP:
                    self.direction = Direction.LEFT
                elif self.direction == Direction.LEFT:
                    self.direction = Direction.DOWN
                elif self.direction == Direction.DOWN:
                    self.direction = Direction.RIGHT
                elif self.direction == Direction.RIGHT:
                    self.direction = Direction.UP

                self.turn = Turn.STRAIGHT
            elif self.turn == Turn.STRAIGHT:
                self.turn = Turn.RIGHT
            elif self.turn == Turn.RIGHT:
                if self.direction == Direction.UP:
                    self.direction = Direction.RIGHT
                elif self.direction == Direction.LEFT:
                    self.direction = Direction.UP
                elif self.direction == Direction.DOWN:
                    self.direction = Direction.LEFT
                elif self.direction == Direction.RIGHT:
                    self.direction = Direction.DOWN

                self.turn = Turn.LEFT

        # Advance based on direction
        if self.direction == Direction.UP:
            self.y -= 1
        elif self.direction == Direction.DOWN:
            self.y += 1
        elif self.direction == Direction.LEFT:
            self.x -= 1
        elif self.direction == Direction.RIGHT:
            self.x += 1

    def __repr__(self):
        return 'Cart (Facing {} at ({},{}))'.format(self.direction.name, self.x, self.y)


def read_initial_map():
    # Read Data from stdin
    max_x = 0
    max_y = 0  #First input is 0th line
    data = []
    for line in sys.stdin:
        # Replace newlines
        line = line.replace('\n', '').replace('\r', '')

        if line.isspace():
            continue

        # Update max values
        max_y += 1
        max_x = max(max_x, len(line))

        data.append(line)

    carts = []
    # Create map and extract carts
    tracks = np.empty([max_x, max_y], dtype=np.unicode_)
    for y, line in enumerate(data):
        for x, c in enumerate(line):

            # Extract cart information
            if c in ['^', 'v', '<', '>']:
                carts.append(Cart(x, y, Direction(c)))

                if c in ['^', 'v']:
                    c = '|'
                else:
                    c = '-'

            tracks[x, y] = c

    return tracks, carts


def print_map(tracks, carts):
    copy = tracks.copy()
    for cart in carts:
        copy[cart.x, cart.y] = cart.direction.value

    for row in np.transpose(copy):
        print(''.join(row))

    print()  #Blank line


def tick(tracks, carts):
    # Sort carts by x,y position
    carts = sorted(carts, key=lambda c: (c.y, c.x))
    for cart in carts:
        if cart.crashed:
            continue

        cart.step(tracks)

        # Check for collisions
        for other in carts:
            if other.crashed:
                continue

            if id(cart) != id(other) and (cart.x, cart.y) == (other.x, other.y):
                print('Collision at ({},{})'.format(cart.x, cart.y))
                cart.crashed = True
                other.crashed = True

    return carts


def remaining_carts(carts):
    total = 0
    for cart in carts:
        if not cart.crashed:
            total += 1
    return total


def cart():
    tracks, carts = read_initial_map()

    ticks = 0
    while remaining_carts(carts) > 1:
        ticks += 1
        print(ticks)
        carts = tick(tracks, carts)

    for cart in carts:
        if not cart.crashed:
            print('The last cart is at ({},{})'.format(cart.x, cart.y))
            break

cart()
