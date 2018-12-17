import re
import sys
import operator


def read_data():
    samples = []
    program = []
    in_sample = False
    in_program = False
    current_sample = None

    for line in sys.stdin:
        digits = [int(i) for i in re.findall(r'\d+', line)]

        if in_program:
            program.append(digits)
        elif 'Before' in line:
            in_sample = True
            current_sample = {'initial': digits}
        elif 'After' in line:
            in_sample = False
            current_sample['final'] = digits
            samples.append(current_sample)
        elif in_sample:
            current_sample['operation'] = digits
        elif len(digits) > 0:
            in_program = True
            program.append(digits)

    return samples, program


def function_factory(given_operator, immediate_A=False, immediate_B=False):
    """
    Generates a function for the given operator and a boolean indicating which inputs to consider
    as immediate or from register
    """
    def f(register, opcode, A, B, output):
        result = register.copy()

        #Read from registers
        A = A if immediate_A else result[A]
        B = B if immediate_B else result[B]

        #Handle setitem seperately because the operator takes 3 values
        if given_operator == operator.setitem:
            given_operator(result, output, A)
        else:
            result[output] = int(given_operator(A, B))
        return result

    return f


def find_matching_instructions(initial_register, final_register, opcode, A, B, output, functions):
    matches = []
    for op, f in functions.items():
        if f(initial_register, opcode, A, B, output) == final_register:
            matches.append(op)

    return matches

def map_instructions(samples, functions):
    mapping = {i: None for i in range(16)}

    # Using the existing maps, iterate through samples until all operations are accounted for
    for sample in samples:
        # Skip if known
        opcode = sample['operation'][0]
        if mapping[opcode] is not None:
            continue

        matches = find_matching_instructions(sample['initial'], sample['final'],
                                             *sample['operation'], functions)

        # Eliminate known matches
        possible_matches = [m for m in matches if m not in mapping.values()]
        if len(possible_matches) == 1:
            mapping[opcode] = possible_matches[0]

    # Verify mapping (ensure that identified function is an option for all inputs)
    for sample in samples:
        matches = find_matching_instructions(sample['initial'], sample['final'],
                                                     *sample['operation'], functions)
        mapped_operation = mapping[sample['operation'][0]]

        if mapped_operation not in matches:
            raise ValueError('Verification Failed')

    return mapping

def registers():
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
    samples, program = read_data()

    # Count the number matching at least 3
    at_least_3 = 0
    for sample in samples:
        matches = find_matching_instructions(sample['initial'], sample['final'],
                                             *sample['operation'], functions)
        if len(matches) >= 3:
            at_least_3 += 1
    print('{}/{} samples behave like at least 3 opcodes.'.format(at_least_3, len(samples)))

    # Match the op codes with the functions
    mapping = map_instructions(samples, functions)

    # Execute the program
    register = [0, 0, 0, 0]
    for idx, operation in enumerate(program):
        opcode, A, B, output = operation
        f = functions[mapping[opcode]]
        register = f(register, opcode, A, B, output)

    print('After executing the program, the final register is {}.'.format(register))

registers()
