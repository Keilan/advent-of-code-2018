import re
import sys
import operator


def read_data():
    ip = None
    instructions = []

    for line in sys.stdin:
        data = line.split()

        if data[0] == '#ip':
            ip = int(data[1])
        else:
            instructions.append([data[0]] + [int(d) for d in data[1:]])

    return ip, instructions


def function_factory(given_operator, immediate_A=False, immediate_B=False):
    """
    Generates a function for the given operator and a boolean indicating which inputs to consider
    as immediate or from register
    """
    def f(register, A, B, C):
        result = register.copy()

        #Read from registers
        A = A if immediate_A else result[A]

        #Handle setitem seperately because the operator takes 3 values
        if given_operator == operator.setitem:
            given_operator(result, C, A)
        else:
            B = B if immediate_B else result[B] # Read here because it's ignored for setitem
            result[C] = int(given_operator(A, B))
        return result

    return f


def run_program(ip, instructions, initial_register, functions):
    register = initial_register.copy()
    count = 0
    print('Start', register)
    while 0 <= register[ip] < len(instructions):
        opcode, A, B, C = instructions[register[ip]]
        register = functions[opcode](register, A, B, C)

        # Iterate instructions
        register[ip] += 1 # Move to next instruction
        count += 1

        print(count, register, opcode, A, B, C)

        #if count == 100:
            #exit()


def flow():
    # Setup
    functions = {
        'addr': function_factory(operator.add),
        'addi': function_factory(operator.add, immediate_B=True),
        'mulr': function_factory(operator.mul),
        'muli': function_factory(operator.mul, immediate_B=True),
        'banr': function_factory(operator.and_),
        'bani': function_factory(operator.and_, immediate_B=True),
        'borr': function_factory(operator.or_),
        'bori': function_factory(operator.or_, immediate_B=True),
        'setr': function_factory(operator.setitem),
        'seti': function_factory(operator.setitem, immediate_A=True),
        'gtir': function_factory(operator.gt, immediate_A=True),
        'gtri': function_factory(operator.gt, immediate_B=True),
        'gtrr': function_factory(operator.gt),
        'eqir': function_factory(operator.eq, immediate_A=True),
        'eqri': function_factory(operator.eq, immediate_B=True),
        'eqrr': function_factory(operator.eq),
    }
    ip, instructions = read_data()

    #register = run_program(ip, instructions, [1, 0, 0, 0, 0, 0], functions)
    register = run_program(ip, instructions, [1, 10551383, 2, 0, 10551380, 5], functions)

flow()
