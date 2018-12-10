import re
import sys
import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        if other == 0:
            other = Point(0, 0)
        return Point(self.x + other.x, self.y + other.y)

    def __radd__(self, other):
        return self + other

    def __truediv__(self, scalar):
        return Point(self.x/scalar, self.y/scalar)

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __repr__(self):
        return f'{self.__class__.__name__} ({self.x}, {self.y})'

    def move(self, dx, dy):
        return Point(self.x + dx, self.y + dy)

    def distance(self, other):
        return math.sqrt(abs(self.x-other.x)**2 + abs(self.y-other.y)**2)


def point_mean(points):
    return sum(points)/len(points)


def average_distance(points):
    mean = point_mean(points)
    distance_sum = 0
    for p in points:
        distance_sum += mean.distance(p)
    return distance_sum/len(points)


def print_points(points):
    # Bounding box values
    min_x = min([p.x for p in points])
    max_x = max([p.x for p in points])
    min_y = min([p.y for p in points])
    max_y = max([p.y for p in points])

    # Create Grid and draw points
    grid = [['.'] * ((max_x - min_x) + 1) for _ in range(min_y, max_y+1)]
    for p in points:
        grid[p.y-min_y][p.x-min_x] = 'X'

    for row in grid:
        print(''.join(row))

def find_message():
    # Get Input
    points = []
    velocities = []
    for observation in sys.stdin:
        x, y, vx, vy = [int(d) for d in re.findall(r'-?\d+', observation)]
        points.append(Point(x, y))
        velocities.append((vx, vy))

    time = 0
    time_since_min = 0 # Break out once new minimums are not being found
    min_distance = average_distance(points)
    min_points = None

    while time_since_min < 1000:
        # Increment time and give measure of progress
        time += 1
        time_since_min += 1
        if time % 1000 == 0:
            sys.stdout.write('.')
            sys.stdout.flush()

        points = [p.move(v[0], v[1]) for p, v in zip(points, velocities)]
        new_average = average_distance(points)
        if new_average < min_distance:
            min_distance = new_average
            min_points = points.copy()
            time_since_min = 0

    print() # New line
    print(f'Minimum distance found at {time-time_since_min} seconds')
    print_points(min_points)

find_message()
