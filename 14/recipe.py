def perform_attempt(scoreboard, index1, index2):
    # Get new scores
    combined = scoreboard[index1] + scoreboard[index2]
    score1 = combined // 10
    score2 = combined % 10

    # Update scoreboard
    scores_added = []
    if score1 != 0:
        scores_added.append(score1)
    scores_added.append(score2)
    scoreboard.extend(scores_added)

    # Update positions
    index1 = (index1 + 1 + scoreboard[index1]) % len(scoreboard)
    index2 = (index2 + 1 + scoreboard[index2]) % len(scoreboard)
    return index1, index2, scores_added


def score_after(attempts):
    # Setup initial score
    scoreboard = [3,7]
    elf1 = 0
    elf2 = 1

    #Perform initial attempts
    while len(scoreboard) < attempts+10:
        elf1, elf2, _ = perform_attempt(scoreboard, elf1, elf2)

    last_10 = scoreboard[attempts:attempts+10]
    print('The 10 recipes after recipe {} have scores: {}'.format(
        attempts, ''.join(str(i) for i in last_10)))


def find_sequence(sequence):
    # Convert integer sequence to list
    sequence = [int(i) for i in sequence]
    # Setup initial score
    scoreboard = [3,7]
    elf1 = 0
    elf2 = 1

    # The number of elements in the sequence that we've seen up to this point
    idx = 0

    # Check for initial sequence
    for score in scoreboard:
        if score == sequence[idx]:
            idx += 1
        else:
            idx = 0

    #Perform initial attempts
    while idx < len(sequence):
        elf1, elf2, scores_added = perform_attempt(scoreboard, elf1, elf2)
        for score in scores_added:
            if score == sequence[idx]:
                idx += 1
            elif score == sequence[0]:
                idx = 1
            else:
                idx = 0

            #Break if finished
            if idx == len(sequence):
                break

    # Find amount before
    scores_before = len(scoreboard) - len(sequence)
    if scoreboard[-len(sequence):] != sequence:
        scores_before -= 1 #Ignore final idx if unused
    print('The sequence {} first appears after {} recipes'.format(sequence, scores_before))


    #last_10 = scoreboard[attempts:attempts+10]
    #print('The 10 recipes after recipe {} have scores: {}'.format(
        #attempts, ''.join(str(i) for i in last_10)))


score_after(323081)
find_sequence('5158916')
find_sequence('01245')
find_sequence('92510')
find_sequence('59414')
find_sequence('323081')