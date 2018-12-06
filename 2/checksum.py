import sys

def check_for_repeats(string):
    """
    Returns a tuple of booleans, the first if duplicates exist, the second if triples do.
    """
    double = False
    triple = False

    counts = {}
    for c in sorted(string):
        if c in counts:
            counts[c] += 1
        else:
            counts[c] = 1

    values = counts.values()
    return (2 in values, 3 in values)


def compute_checksum():
    doubles = 0
    triples = 0
    for box_id in sys.stdin:
        double, triple = check_for_repeats(box_id)
        doubles += int(double)
        triples += int(triple)
    return doubles*triples


def count_differences(s1, s2):
    total = 0
    for c1,c2 in zip(s1,s2):
        if c1 != c2:
            total += 1
    return total


def find_common_letters(s1, s2):
    result = ''
    for c1,c2 in zip(s1,s2):
        if c1 == c2:
            result += c1
    return result


def find_close():
    boxes = []
    for box in sys.stdin:
        boxes.append(box)

    for pos, box1 in enumerate(boxes):
        for box2 in boxes[pos+1:]:
            diffs = count_differences(box1, box2)
            if diffs == 1:
                print(find_common_letters(box1, box2))
                exit()


print(find_close())
