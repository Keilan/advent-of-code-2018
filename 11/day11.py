import sys

def get_power(x, y, serial_number):
    power = x + 10
    power *= y
    power += serial_number
    power *= (x + 10)

    if power < 100:
        power = 0
    else:
        power = int(str(power)[-3])

    return power - 5

def get_grid_power(left_x, top_y, grid, size):
    """
    Top left x and y.
    """
    power = 0
    for x in range(left_x, left_x+size):
        for y in range(top_y, top_y+size):
            try:
                power += grid[x][y]
            except IndexError:
                pass

    return power


def power():
    serial_number = 5535
    grid = [[0] * 302 for y in range(1, 302)]  # Extra value to account for 1-based arrays

    # Fill in grid
    for x in range(1, 301):
        for y in range(1, 301):
            grid[x][y] += get_power(x, y, serial_number)

    max_power = 0
    for size in range(1, 301):
        print('Size', size)
        for x in range(1, 301):
            for y in range(1, 301):
                power = get_grid_power(x, y, grid, size)
                if power is not None and power > max_power:
                    max_power = power
                    print(power)
                    print('Coordinates', x, y, size)


power()
