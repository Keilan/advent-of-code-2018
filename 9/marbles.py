class Marble:
    def __init__(self, value, prev, next):
        self.value = value
        self.prev = prev
        self.next = next

    def __str__(self):
        return str(self.value)


def print_marbles(first_marble):
    """
    Prints a list of all the marbles, assuming the next and prev values are correctly formed.
    """
    start = id(first_marble)
    marbles = [first_marble.value]
    current = first_marble.next

    while(id(current) != start):
        marbles.append(current.value)
        current = current.next

    print('Marbles: ', marbles)


def place_marble(current, marble_value):
    """
    Given the current marble and the value of a new marble, creates a new marble in the correct
    spot.
    """
    # Get the two marbles on either side of the new marble and create it
    left = current.next
    right = left.next
    new_marble = Marble(marble_value, left, right)

    # Update the left and right marbles
    left.next = new_marble
    right.prev = new_marble

    return new_marble


def get_score(current, marble_value):
    """
    Removes the correct marble, sets the new current marble, and returns the score to be given
    to the current player.
    """
    remove_marble = current
    for _ in range(7):
        remove_marble = remove_marble.prev

    score = marble_value + remove_marble.value

    # Delete the marble by modifying the next and previous
    remove_marble.prev.next = remove_marble.next
    remove_marble.next.prev = remove_marble.prev

    return score, remove_marble.next


def marble_game(players, num_marbles):
    # Set score for each player to 0
    scores = [0] * players

    # Initialize the first marble, with previous and next as itself
    current = Marble(0, None, None)
    current.next = current
    current.previous = current

    for marble_value in range(1, num_marbles+1):
        if marble_value % 23 != 0:
            current = place_marble(current, marble_value)
        else:
            points, current = get_score(current, marble_value)
            scores[marble_value % players] += points

    print('The highest score is {}'.format(max(scores)))


marble_game(9, 25)
marble_game(10, 1618)
marble_game(13, 7999)
marble_game(17, 1104)
marble_game(21, 6111)
marble_game(30, 5807)
marble_game(404, 71852)
marble_game(404, 7185200)
