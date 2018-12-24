import re
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

    def __repr__(self):
        return '{} {} - {} units with {} HP, {} {} damage, initiative {}'.format(
            self.army.name, self.id_number, self.units, self.hp, self.damage_type, self.damage,
            self.initiative
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
                    for damage_type in data[2:]:
                        weaknesses.append(Damage(damage_type.title()))
                elif data[0] == 'immune':
                    for damage_type in data[2:]:
                        immunities.append(Damage(damage_type.title()))

            g = Group(current_army, current_id, units, hp, damage, damage_type, weaknesses,
                      immunities, initiative)
            groups.append(g)
            current_id += 1

    return groups


def simulate_battle():
    groups = read_input('test.txt')
    print(groups)


simulate_battle()
