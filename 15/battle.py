import sys
import copy


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
        reachable = filter_reachable(self.x, self.y, in_range, arena, units)

        # Sort by path_length, then reading order
        reachable = sorted(reachable, key=lambda t: (len(t[2][0]), t[0], t[1]))
        if len(reachable) == 0:
            return 'no-reachable', {}
        choice = reachable[0]

        # Find first path location in reading order (note that first element is the current pos)
        paths = choice[2]
        if len(paths[0]) > 1:
            paths = sorted(paths, key=lambda p: (p[1][0], p[1][1]))
            x, y = paths[0][1]
        else:
            x, y = choice[0], choice[1]  # No intermediate path, just move to destination

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
    print('filter', x, y)
    # Map units as walls for simplicity
    arena_copy = copy.deepcopy(arena)
    for u in units:
        arena_copy[u.x][u.y] = '#'
    arena_copy[x][y] = '.'  #Set this back to open as it's our starting point

    # Recursively find all reachable tiles and the minimum path
    def update_reachable(tile, reachable, path, paths):
        x, y = tile

        # Not reachable if a wall or unit
        if arena_copy[x][y] == '#':
            return

        # Already seen and faster
        if tile in reachable and len(paths[tile][0]) < len(path):
            return

        # Already seen and slower (delete existing)
        if tile in reachable and len(paths[tile][0]) > len(path):
            print('Deleting', tile)
            del paths[tile]

        # Add to reachable and update distances
        reachable.add(tile)
        if tile in paths:
            paths[tile].append(path)
            if len(paths[tile]) > 100:
                return
            print('Updating', tile, len(paths[tile]))
        else:
            print('Adding', tile)
            paths[tile] = [path]

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
    return [(t[0], t[1], paths[t]) for t in tiles]


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
            print('\nRound ', completed_rounds)
            print_arena(arena, units)

    sum_hit_points = sum([u.hp for u in units if not u.dead])
    print(sum_hit_points, sum_hit_points*completed_rounds)

battle()
