import re
import copy
from enum import Enum


# Setup classes
class Army(Enum):
    Immune = 0
    Infection = 1


class Damage(Enum):
    Bludgeoning = 'Bludgeoning'
    Cold = 'Cold'
    Fire = 'Fire'
    Radiation = 'Radiation'
    Slashing = 'Slashing'


class Group:
    def __init__(self, army, id_number, units, hp, damage, damage_type, weaknesses, immunities,
                 initiative):
        self.army = army
        self.id_number = id_number
        self.units = units
        self.hp = hp
        self.damage = damage
        self.damage_type = damage_type
        self.weaknesses = weaknesses
        self.immunities = immunities
        self.initiative = initiative

    @property
    def name(self):
        return '{} {}'.format(self.army.name, self.id_number)

    @property
    def effective_power(self):
        return self.units * self.damage

    def __repr__(self):
        return '{} - {} units ({} HP, {} {} DMG, {} INT) - {} EP'.format(
            self.name, self.units, self.hp, self.damage, self.damage_type.name,
            self.initiative, self.effective_power
        )


def read_input(filename):
    groups = []
    current_army = None
    current_id = None

    for line in open(filename, 'r').readlines():
        if line.isspace():
            continue

        if 'Immune System' in line:
            current_army = Army.Immune
            current_id = 1
        elif 'Infection' in line:
            current_army = Army.Infection
            current_id = 1

        # Process unit information from line
        else:
            # Extract numerical values
            numbers = [int(d) for d in re.findall(r'\d+', line)]
            units, hp, damage, initiative = numbers

            # Extract damage type
            damage_type = Damage(line.split()[-5].title())

            # Extract initiative and weaknesses
            weaknesses = []
            immunities = []
            section = line[line.find('(')+1:line.find(')')]
            for data in section.split(';'):
                data = data.replace(',', '').split()  # Remove commas
                if data[0] == 'weak':
                    for weakness_type in data[2:]:
                        weaknesses.append(Damage(weakness_type.title()))
                elif data[0] == 'immune':
                    for immunity_type in data[2:]:
                        immunities.append(Damage(immunity_type.title()))

            g = Group(current_army, current_id, units, hp, damage, damage_type, weaknesses,
                      immunities, initiative)
            groups.append(g)
            current_id += 1

    return groups


def calculate_damage(attacker, defender):
    # No damage done if the defender is immune
    if attacker.damage_type in defender.immunities:
        return 0

    damage = attacker.effective_power

    # Apply weaknesses
    if attacker.damage_type in defender.weaknesses:
        damage *= 2

    return damage


def select_target(group, groups, unavailable):
    max_damage = 0
    target = None

    for other in groups:
        #Don't attack yourself or your own team
        if group.army == other.army:
            continue

        #Don't attack a group already being attacked or one that is dead
        if other in unavailable or other.units == 0:
            continue

        damage = calculate_damage(group, other)

        #Don't attack an immune group
        if damage == 0:
            continue

        if damage > max_damage:
            max_damage = damage
            target = other

        # Resolve ties
        elif damage == max_damage:
            if ((other.effective_power, other.initiative) >
                    (target.effective_power, target.initiative)):
                target = other

    return target


def apply_damage(group, damage):
    units_killed = damage//group.hp
    group.units = max(0, group.units - units_killed)


def both_alive(groups):
    alive = set()
    for g in groups:
        if g.units > 0:
            alive.add(g.army)

    return len(alive) == 2


def fight(groups):
    # Target selection
    targets = {}  # Map a group to the group they are attacking
    for group in sorted(groups, key=lambda g: (-g.effective_power, -g.initiative)):
        target = select_target(group, groups, targets.values())
        if target is not None:
            targets[group] = target

    # Attack
    for group in sorted(groups, key=lambda g: (-g.initiative)):
        # Groups with no units or no target cannot attack
        if group.units == 0 or group not in targets:
            continue

        target = targets[group]
        damage = calculate_damage(group, target)
        #print('{} deals {} damage to {}'.format(group.name, damage, target.name))
        apply_damage(target, damage)


def simulate_battle():
    initial_groups = read_input('input.txt')
    winner = None
    boost = 0

    while winner != Army.Immune:
        groups = copy.deepcopy(initial_groups)

        # Apply the boost
        for g in groups:
            if g.army == Army.Immune:
                g.damage += boost

        stalemate = False
        prev_units = sum([g.units for g in groups])
        fight_count = 1
        while both_alive(groups):
            fight(groups)
            fight_count += 1

            # Stalemate check
            current_units = sum([g.units for g in groups])
            if current_units == prev_units:
                stalemate = True
                break

            prev_units = current_units

        # Determine winner
        if stalemate:
            print('There was a stalemate (boost was {})'.format(boost))
        else:
            surviving_groups = [g for g in groups if g.units > 0]
            winner = surviving_groups[0].army

            print('{} won after {} fights with {} surviving units (boost was {}).'.format(
                winner.name, fight_count, sum([g.units for g in groups]), boost)
            )

        boost += 1


simulate_battle()
