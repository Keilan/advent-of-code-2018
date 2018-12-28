import re
import sys

import tqdm
import numpy as np


def read_input():
    bots = []
    for line in sys.stdin:
        digits = [int(i) for i in re.findall('-?\d+', line)]
        bots.append(digits)

    return np.array(bots)


def count_in_range(bot, bots):
    """
    Returns the number of bots in range of the given bot.
    """
    x, y, z, r = bot

    # Get distances from the given bot
    xs = abs(bots[:, 0]-x)
    ys = abs(bots[:, 1]-y)
    zs = abs(bots[:, 2]-z)

    # Return count less than r
    return sum(xs+ys+zs < r)


def count_can_reach(x, y, z, bots):
    """
    Returns the number of bots that can reach (x,y,z).
    """
    # Get distances from the given bot
    xs = abs(bots[:, 0]-x)
    ys = abs(bots[:, 1]-y)
    zs = abs(bots[:, 2]-z)

    return sum((xs + ys + zs) <= bots[:, 3])


def random_search(coords, bots, iterations=100000):
    best = count_can_reach(*coords, bots=bots)
    best_coords = np.array(coords)
    import random

    count = 0
    while True:
        count += 1

        if count % 10000 == 0:
            print('  {} in range at {} - distance is {} - {} iterations'.format(best, best_coords,
                                                                                sum(abs(best_coords)),
                                                                                count))
        if count >= iterations:
            return best, best_coords

        new_coords = np.array([best_coords[0] + random.randint(-10000, 10000),
                               best_coords[1] + random.randint(-10000, 10000),
                               best_coords[2] + random.randint(-10000, 10000)])
        reachable = count_can_reach(*new_coords, bots=bots)

        if reachable > best:
            best = reachable
            best_coords = new_coords.copy()
            best, best_coords = minimize(best_coords, bots)
            best, best_coords = scan_region(best_coords, bots, 3)

        elif reachable == best and sum(abs(new_coords)) < sum(abs(best_coords)):
            best_coords = new_coords.copy()
            best, best_coords = minimize(best_coords, bots)
            best, best_coords = scan_region(best_coords, bots, 3)


def minimize(coords, bots):
    best = count_can_reach(*coords, bots=bots)
    best_coords = np.array(coords)

    # For each axis, reduce size bit by bit
    for axis in range(3):
        jump_size = 1000000
        while jump_size > 0:
            new_coords = best_coords.copy()
            new_coords[axis] -= jump_size

            reachable = count_can_reach(*new_coords, bots=bots)

            if reachable >= best:
                best = reachable
                best_coords = new_coords
            elif reachable == best:
                best_coords = new_coords
            else:
                jump_size //= 10

    #print('Minimized to {} {} - distance is {}'.format(best, best_coords, sum(abs(best_coords))))
    return best, best_coords


def scan_region(coords, bots, distance):
    best = count_can_reach(*coords, bots=bots)
    best_coords = np.array(coords)

    #pbar = tqdm.tqdm(desc='Scanning', total=(distance*2)**3)
    for x in range(best_coords[0]-distance, best_coords[0]+distance):
        for y in range(best_coords[1]-distance, best_coords[1]+distance):
            for z in range(best_coords[2]-distance, best_coords[2]+distance):
                reachable = count_can_reach(x, y, z, bots=bots)

                if reachable > best:
                    best = reachable
                    best_coords = np.array([x, y, z])

                elif reachable == best and sum(abs(np.array([x, y, z]))) < sum(abs(best_coords)):
                    best_coords = np.array([x, y, z])

                #pbar.update(1)

    #pbar.close()
    #print('Scanned to {} {} - distance is {}'.format(best, best_coords, sum(abs(best_coords))))
    return best, best_coords


def nanobots():
    bots = read_input()

    max_bot = bots[np.argmax(bots[:, 3])]  #The bot with the highest range
    print('The bot with the largest range has {} bots in range.'.format(
        count_in_range(max_bot, bots)))

    # Try all extreme points on spheres
    max_reachable = 0
    reachable_distance = float('inf')
    reachable_coords = None

    for bot in tqdm.tqdm(bots):
        r = bot[3]
        for radius in [1, r//2, r]: # Check some extra points for added granularity
            for axis in range(3):
                for mult in [-1, 1]:
                    coordinates = bot[:3]
                    coordinates[axis] += radius * mult
                    reachable = count_can_reach(*coordinates, bots=bots)

                    if reachable > max_reachable:
                        max_reachable = reachable
                        reachable_distance = sum(abs(coordinates))
                        reachable_coords = coordinates.copy()
                    elif reachable == max_reachable and reachable_distance > sum(abs(coordinates)):
                        reachable_distance = sum(abs(coordinates))
                        reachable_coords = coordinates.copy()

    print('Initial search found {} in range at {} - with a distance of {}'.format(max_reachable,
                                                                                  reachable_coords,
                                                                                  sum(abs(reachable_coords))))
    reachable, coords = random_search(reachable_coords, bots, iterations=10000)
    print('After random search best is {} in range at {} - with a distance of {}'.format(reachable,
                                                                                         coords,
                                                                                         sum(abs(coords))))

    # Alternate repeated scan and random search forever
    while True:
        # Repeat scan while better results exist
        distance, new_coords = scan_region(coords, bots, 1)
        count = 0
        while any(coords != new_coords) and count <= 1000000:
            count += 1

            if count % 10000 == 0:
                print('  {} in range at {} - distance is {} - {} iterations'.format(distance, new_coords,
                                                                                    sum(abs(new_coords)),
                                                                                    count))
            coords = new_coords
            distance, new_coords = scan_region(coords, bots, 1)

        print('After repeated scan best is {} in range at {} - with a distance of {}'.format(distance,
                                                                                             coords,
                                                                                             sum(abs(coords))))

        reachable, coords = random_search(new_coords, bots, iterations=100000)
        print('After random search best is {} in range at {} - with a distance of {}'.format(reachable,
                                                                                             coords,
                                                                                             sum(abs(coords))))


nanobots()
"""
Correct Answer
Current Best - 976 [45428220 46554241 13209446] - distance is 105191907
"""
