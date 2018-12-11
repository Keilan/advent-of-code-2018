import sys


def get_power(x, y, serial_number):
    """
    Simplify the power equation down to a single expression.
    """
    return (((((x + 10)*y + serial_number) * (x+10)) // 100) % 10) - 5


def get_grid_power(left_x, top_y, power_sums, size):
    """
    Given the top x and y values and the size of the grid to compute, this function uses the
    power sum grid to return the grid power in constant time.
    """
    # Get the far ends
    right_x = min(left_x + size - 1, 299)
    bottom_y = min(top_y + size - 1, 299)

    #print(left_x, top_y)
    return (
        power_sums[right_x][bottom_y]
        - (power_sums[left_x-1][bottom_y] if left_x != 0 else 0)
        - (power_sums[right_x][top_y-1] if top_y != 0 else 0)
        + (power_sums[left_x-1][top_y-1] if left_x != 0 and top_y != 0 else 0)
    )
    #power = 0
    #for x in range(left_x, left_x+size):
        #for y in range(top_y, top_y+size):
            #try:
                #power += grid[x][y]
            #except IndexError:
                #pass

    #return power


def print_matrix(m, limit=None):
    for x in range(300)[:limit]:
        line = ''
        for val in m[x][:limit]:
            line += f'{val:>4}'
        print(line)


def power():
    serial_number = 5535

    # Fill in matrix of all cell values
    power_levels = [[get_power(x, y, serial_number) for y in range(1, 301)] for x in range(1, 301)]

    # Create a new matrix where (x,y) is to sum of the power levels of the square from 1,1 to x,y
    power_sums = [[0] * 300 for _ in range(300)]

    # Handle the outside edges first
    power_sums[0][0] = power_levels[0][0]
    for idx in range(1,300):
        power_sums[idx][0] = power_sums[idx-1][0] + power_levels[idx][0]
        power_sums[0][idx] = power_sums[0][idx-1] + power_levels[0][idx]

    # Fill in the remainder
    for x in range(1, 300):
        for y in range(1, 300):
            power_sums[x][y] = (power_levels[x][y]
                                + power_sums[x-1][y]
                                + power_sums[x][y-1]
                                - power_sums[x-1][y-1])

    # Largest 3 x 3
    max_power = 0
    max_pos = None
    for x in range(300):
        for y in range(300):
            power = get_grid_power(x, y, power_sums, 3)
            if power is not None and power > max_power:
                max_power = power
                max_pos = (x,y)
    print(f'The best 3x3 grid has a power level of {max_power} at ({max_pos[0]+1},{max_pos[1]+1}).')


    max_power = 0
    max_pos = None
    for size in range(1, 301):
        for x in range(300):
            for y in range(300):
                power = get_grid_power(x, y, power_sums, size)
                if power is not None and power > max_power:
                    max_power = power
                    max_pos = (x,y,size)

    print(f'The best grid has a power level of {max_power} at ({max_pos[0]+1},{max_pos[1]+1}) with size {max_pos[2]}.')



power()
