# Part 1
# import sys

# total = 0
# for line in sys.stdin:
#     operator = line[0]
#     value = line[1:]

#     if operator == '+':
#         total += int(value)
#     elif operator == '-':
#         total -= int(value)

# print(total)

# Part 2
import sys
input_list = []
for line in sys.stdin:
    operator = line[0]
    value = line[1:]
    input_list.append((operator,value))

total = 0
seen = set()
while True:
    for operator, value in input_list:
        if operator == '+':
            total += int(value)
        elif operator == '-':
            total -= int(value)

        if total in seen:
            print(total)
            exit()
        else:
            seen.add(total)

    print('Repeating List')
