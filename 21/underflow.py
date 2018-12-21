import sys
import operator


# Copy helper functions from day 19
def read_data():
    ip = None
    instructions = []

    for line in open('input.txt', 'r').readlines():
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

        # Read from registers
        A = A if immediate_A else result[A]

        # Handle setitem seperately because the operator takes 3 values
        if given_operator == operator.setitem:
            given_operator(result, C, A)
        else:
            B = B if immediate_B else result[B] # Read here because it's ignored for setitem
            result[C] = int(given_operator(A, B))
        return result

    return f


def function_description_factory(given_operator, immediate_A=False, immediate_B=False):
    """
    Generates a function that prints the operation in python style code for ease of understanding.
    """
    symbols = {
        operator.add: '+',
        operator.mul: '*',
        operator.and_: '&',
        operator.or_: '|',
        operator.setitem: '=',
        operator.gt: '>',
        operator.eq: '=='
    }

    def f(A, B, C):
        target = f'r[{C}]'
        opA = str(A) if immediate_A else f'r[{A}]'
        opB = str(B) if immediate_B else f'r[{B}]'
        symbol = symbols[given_operator]


        if given_operator == operator.setitem:
            return f'{target} = {opA}'

        elif given_operator in [operator.gt, operator.eq, operator.and_, operator.or_]:
            return f'{target} = {opA} {symbol} {opB}'

        else:
            if opA == target:
                return f'{target} {symbol}= {opB}'
            elif opB == target:
                return f'{target} {symbol}= {opA}'
            else:
                return f'{target} = {opA} {symbol} {opB}'

    return f


def translate_instructions(instructions, descriptions):
    for idx, instruction in enumerate(instructions):
        opcode, A, B, C = instruction
        print(f'IP{idx}: {descriptions[opcode](A, B, C)}')


def run_program(ip, instructions, initial_register, functions, descriptions):
    register = initial_register.copy()
    count = 0
    print('Start', register)
    while 0 <= register[ip] < len(instructions):
        instruction_number = register[ip]
        opcode, A, B, C = instructions[instruction_number]
        #print(f'IP{instruction_number} - {descriptions[opcode](A, B, C)}')
        register = functions[opcode](register, A, B, C)

        # Iterate instructions
        register[ip] += 1 # Move to next instruction
        count += 1

        if instruction_number == 28:
            print(count, register)

    return register


def underflow():
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

    descriptions = {
        'addr': function_description_factory(operator.add),
        'addi': function_description_factory(operator.add, immediate_B=True),
        'mulr': function_description_factory(operator.mul),
        'muli': function_description_factory(operator.mul, immediate_B=True),
        'banr': function_description_factory(operator.and_),
        'bani': function_description_factory(operator.and_, immediate_B=True),
        'borr': function_description_factory(operator.or_),
        'bori': function_description_factory(operator.or_, immediate_B=True),
        'setr': function_description_factory(operator.setitem),
        'seti': function_description_factory(operator.setitem, immediate_A=True),
        'gtir': function_description_factory(operator.gt, immediate_A=True),
        'gtri': function_description_factory(operator.gt, immediate_B=True),
        'gtrr': function_description_factory(operator.gt),
        'eqir': function_description_factory(operator.eq, immediate_A=True),
        'eqri': function_description_factory(operator.eq, immediate_B=True),
        'eqrr': function_description_factory(operator.eq),
    }

    ip, instructions = read_data()
    #translate_instructions(instructions, descriptions)
    run_program(ip, instructions, [0, 0, 0, 0, 0, 0], functions, descriptions)


underflow()