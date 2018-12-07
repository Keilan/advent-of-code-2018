import sys

SIZE = 400

def find_closest(p, points):
    min_dist = 1000
    closest = None
    tied = False
    for i, point in enumerate(points):
        dist = abs(point[0]-p[0]) + abs(point[1]-p[1])
        if dist < min_dist:
            min_dist = dist
            closest = i + 1
            tied = False
        elif dist == min_dist:
            tied = True

    return closest if not tied else 0


def find_sum(p, points):
    total = 0
    for point in points:
        dist = abs(point[0]-p[0]) + abs(point[1]-p[1])
        total += dist
    return total

def task1():
    grid = [[0] * SIZE for _ in range(SIZE)]
    points = []
    for i, line in enumerate(sys.stdin):
        x, y = line.replace(' ', '').split(',')
        x, y = int(y), int(x)
        points.append((x, y))
        grid[y][x] = i + 1

    for x in range(SIZE):
        for y in range(SIZE):
            if grid[y][x] == 0:
                grid[y][x] = find_closest((x, y), points)

    #Find edges
    edges = set()
    for x in range(SIZE):
        edges.add(grid[x][0])
        edges.add(grid[x][-1])
        edges.add(grid[0][x])
        edges.add(grid[-1][x])

    max_count = 0
    value = None
    for i in range(1, len(points) + 1):
        if i in edges:
            continue
        else:
            total = sum([col.count(i) for col in grid])
            if total > max_count:
                max_count = total
                value = i

    print(f'Point {value+1} has a region size of {max_count}')

    sum_distances = [[0] * SIZE for _ in range(SIZE)]
    for x in range(SIZE):
        for y in range(SIZE):
            if sum_distances[y][x] == 0:
                sum_distances[y][x] = find_sum((x, y), points)

    safe_points = 0
    for x in range(SIZE):
        for y in range(SIZE):
            if sum_distances[x][y] < 10000:
                safe_points += 1

    print(f'The number of points less than {10000} is {safe_points}')


    #for r in grid:
        #print(''.join(str(r)))

task1()