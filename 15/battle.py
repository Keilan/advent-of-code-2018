import sys
import copy
import time


class Unit:
    #Used to uniquely identify combatants (assumes less than 27 of each)
    goblin_id = 'a'
    elf_id = 'A'

    def __init__(self, race, x, y, hp, attack):
        if race == 'goblin':
            self.name = Unit.goblin_id
            Unit.goblin_id = chr(ord(Unit.goblin_id) + 1)
        elif race == 'elf':
            self.name = Unit.elf_id
            Unit.elf_id = chr(ord(Unit.elf_id) + 1)

        self.race = race
        self.x = x
        self.y = y
        self.hp = hp
        self.attack = attack
        self.dead = False

    def enemy_race(self):
        if self.race == 'goblin':
            return 'elf'
        elif self.race == 'elf':
            return 'goblin'
        else:
            raise ValueError('Invalid race')

    def find_open_tiles(self, arena, units):
        """
        Returns a list of all open tiles adjacent to the unit.
        """
        tiles = []
        for x, y in [(self.x+1, self.y), (self.x, self.y+1), (self.x-1, self.y), (self.x, self.y-1)]:
            if arena[x][y] == '.':
                tiles.append((x, y))
        return tiles

    def find_adjacent_targets(self, arena, units):
        """
        Returns a list of all adjacent targets in range.
        """
        in_range = []
        targets = []
        for x, y in [(self.x+1, self.y), (self.x, self.y+1), (self.x-1, self.y), (self.x, self.y-1)]:
            if arena[x][y] != '#':
                other = unit_at(x, y, units)
                if other is not None and other.race != self.race and not other.dead:
                    targets.append(other)

        return targets

    def find_in_range_tiles(self, arena, units):
        # Find tiles in range to an enemy
        in_range_tiles = set()  #Set to avoid duplicates
        for u in units:
            if u.race == self.race:
                continue
            in_range_tiles.update(u.find_open_tiles(arena, units))

        return in_range_tiles

    def perform_attack(self, arena, targets):
        # Sort targets by hit points, and then position
        target = sorted(targets, key=lambda t: (t.hp, t.x, t.y))[0]

        # Reduce hit points and check if dead
        target.hp -= self.attack

        if target.hp <= 0:
            target.dead = True

        return {'target': target}

    def perform_turn(self, arena, units):
        """
        Returns a result, and a dictionary containing any extra required info about what happened
        during the turn.
        """
        # Verify that unit hasn't died
        if self.dead:
            return 'dead', {}

        # Verify that enemies are still present
        targets = [u for u in units if u.race == self.enemy_race() and not u.dead]
        if len(targets) == 0:
            return 'no-targets', {}

        # Check for in-range targets
        targets = self.find_adjacent_targets(arena, units)
        if len(targets) > 0:
            data = self.perform_attack(arena, targets)
            return 'attack', data

        # Find reachable tiles
        in_range = self.find_in_range_tiles(arena, units)
        reachable, paths = filter_reachable(self.x, self.y, in_range, arena, units)

        # Sort by path_length, then reading order
        reachable = sorted(reachable, key=lambda t: (t[2], t[0], t[1]))
        if len(reachable) == 0:
            return 'no-reachable', {}
        dest_x, dest_y, distance = reachable[0]

        # Find first step towards destination
        x, y = find_next_step((self.x, self.y), (dest_x, dest_y), paths)
        # Update position
        self.x = x
        self.y = y

        # Check for in-range targets after moving
        targets = self.find_adjacent_targets(arena, units)
        if len(targets) > 0:
            data = self.perform_attack(arena, targets)
            return 'move-attack', data
        else:
            return 'moved', {'pos': (x, y)}

    def __repr__(self):
        return '{}{} {}: {}/{} at ({},{})'.format('Dead ' if self.dead else '',
                                                  self.race.title(), self.name, self.hp,
                                                  self.attack, self.x, self.y)


def read_arena():
    arena = []
    units = []
    for x, line in enumerate(sys.stdin):
        line = line.strip()

        # Extract units from line
        extracted = ''
        for y, c in enumerate(line):
            if c == 'G':
                goblin = Unit('goblin', x, y, 200, 3)
                units.append(goblin)
                extracted += '.'
            elif c == 'E':
                elf = Unit('elf', x, y, 200, 3)
                units.append(elf)
                extracted += '.'
            else:
                extracted += c

        arena.append(list(extracted))

    return arena, units


def print_arena(arena, units):
    arena_copy = copy.deepcopy(arena)

    #Draw units
    for unit in units:
        if unit.dead:
            continue

        arena_copy[unit.x][unit.y] = unit

    for row in arena_copy:
        row_end = ''
        for tile in row:
            if isinstance(tile, Unit):
                row_end += '{}({}), '.format(tile.name, tile.hp)
                tile = tile.name
            print(tile, end='')
        print('  ', row_end)


def unit_at(x, y, units):
    """
    Returns the unit present at x,y or None.
    """
    for u in units:
        if u.x == x and u.y == y:
            return u
    return None


def filter_reachable(x, y, tiles, arena, units):
    """
    Given a list of tiles and an x,y coordinate, returns only the tiles in the list that
    are reachable from the given coordinate, adding a third value, indicating the distance to
    reach the tile.
    """
    # Map units as walls for simplicity
    arena_copy = copy.deepcopy(arena)
    for u in units:
        if u.dead:
            continue
        arena_copy[u.x][u.y] = '#'
    arena_copy[x][y] = '.'  #Set this back to open as it's our starting point

    # Recursively find all reachable tiles and the minimum path
    def update_reachable(tile, reachable, path, paths):
        """
        Tile specifies the x,y coordinates of the starting point, reachable is the set of all
        reachable tiles, path is the current path travelled to get to this point, and paths is a
        dictionary mapping an (x,y) tuple to a dictionary mapping (prev_x, prev_y), to
        the distance travelled to get to the given key via (prev_x, prev_y).
        """
        #sys.stdout.write('.')
        x, y = tile

        # Not reachable if a wall or unit
        if arena_copy[x][y] == '#':
            return

        # Get previous space for updating path
        prev_space = (path[-1][0], path[-1][1]) if path else None

        # Already seen and faster
        if tile in reachable and prev_space in paths[tile] and paths[tile][prev_space] <= len(path):
            return

        # Add to reachable and update distances
        reachable.add(tile)

        distance = len(path) if prev_space is not None else float('inf')
        if tile in paths:
            paths[tile][prev_space] = distance
        else:
            paths[tile] = {prev_space: distance}

        # Add all adjacent
        path = path + ((x, y),)
        for adjacent_tile in [(x+1, y), (x, y+1), (x-1, y), (x, y-1)]:
            update_reachable(adjacent_tile, reachable, path, paths)

    reachable = set()
    paths = {}
    update_reachable((x, y), reachable, (), paths)

    # Filter out unreachable tiles
    tiles = tiles.intersection(reachable)

    # Append distances
    return [(t[0], t[1], min(paths[t].values())) for t in tiles], paths


def find_next_step(start, end, paths):
    """
    Given initial and final (x,y) coordinates and a dictionary of partial paths, return the
    next step towards reaching
    """
    def find_paths(start, current, distance, paths, choices):
        """
        Given the start point, and the current point, builds a dictionary indicating the first step
        and the minimum distance to the end using that step. Distance indicates the distance from
        current to end.
        """
        # Find all paths resulting in the minimum distance
        options = []
        min_distance = min(paths[current].values())
        for option, distance in paths[current].items():
            if distance == min_distance:

                # If we find the beginning, break out
                if option == start:
                    if option not in choices or choices[current] < distance + min_distance:
                        choices[current] = distance + min_distance
                    return

                # Add to list of options
                options.append(option)

        # For each path, recursively find minimal paths
        for option in options:
            find_paths(start, option, min_distance, paths, choices)

    choices = {}
    find_paths(start, end, 0, paths, choices)
    choices = sorted(choices.keys())
    return choices[0]


def perform_round(arena, units):
    """
    Performs a round of moving and combat, returns True if the full round is executed.
    """
    # Order units and split into goblins and elves
    units = [u for u in sorted(units, key=lambda u: (u.x, u.y)) if not u.dead]

    for unit in units:
        result, data = unit.perform_turn(arena, units)
        if result == 'no-targets':
            return False  #Nothing to attack, game over

    return True


def battle():
    start = time.time()
    round_end = time.time()
    arena, units = read_arena()

    print('Start')
    print_arena(arena, units)
    completed_rounds = 0
    completed = True

    while completed:
        completed = perform_round(arena, units)

        if not completed:
            print('Game Over')
        else:
            completed_rounds += 1
            print('\nRound {} - {:.2f}s/{:.2f}s'.format(completed_rounds,
                                                      time.time() - round_end,
                                                      time.time() - start))
            round_end = time.time()
            print_arena(arena, units)

    remaining_units = [u for u in units if not u.dead]
    sum_hit_points = sum([u.hp for u in remaining_units])
    print('{} race won with {} remaining hit points in {} rounds'.format(remaining_units[0].race.title(),
                                                                         sum_hit_points,
                                                                         completed_rounds))
    print('Final Score is {}'.format(sum_hit_points*completed_rounds))
    print('Completed in {:.2f}s'.format(time.time() - start))

battle()


"""
Part 1
1. 206585 - Wrong, too low
"""
