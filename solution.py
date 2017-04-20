assignments = []


def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s + t for s in A for t in B]


rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]

diagonal1_unit = [[rows[s] + cols[s] for s in range(len(rows))]]
diagonal2_unit = [[rows[s] + cols[-1 * s - 1] for s in range(len(rows))]]

unitlist = row_units + column_units + square_units + diagonal1_unit + diagonal2_unit
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # to record twins found
    twins_found = []

    # Find all instances of naked twins
    for box, possibilities in values.items():
        # does who have only two numbers in their posibilities
        if len(possibilities) == 2:
            # searching only by units (colums, row, squares and diagonals)
            for unit in units[box]:
                twins = [(box, boxInUnit) for boxInUnit in unit if
                         (values[boxInUnit] == values[box] and box != boxInUnit)]

                if (len(twins) > 0):
                    # if twins found, add to the list of twints including the unit
                    for twin in twins:
                        if twin not in twins_found:
                            twins_found.append((twins, unit))

    if len(twins_found) > 0:
        # Eliminate the naked twins as possibilities for their peers in the correspondient unit
        for twins, unit in twins_found:
            boxTwin1 = twins[0][0]
            boxTwin2 = twins[0][1]
            for box in unit:  # for every box in unit
                if (box != boxTwin1 and box != boxTwin2):
                    # erasing values of other peers in unit
                    values[box] = values[box].replace(values[boxTwin1][0], '').replace(values[boxTwin2][1], '')
                    assign_value(values, box, values[box])

    return values


def grid_values(grid):
    """Convert grid string into {<box>: <value>} dict with '.' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '.' if it is empty.
    """
    # assertion to check long
    assert len(grid) == 81
    dictionary = dict(zip(boxes, list(grid)))

    for box, possibilities in dictionary.items():
        dictionary[box] = possibilities if possibilities != '.' else '123456789'
    return dictionary


def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    for box, possibilities in values.items():
        if len(possibilities) == 1:
            # is a box with a already defined value
            for peerBox in peers[box]:  # erase not possible values of peers posibilities
                values[peerBox] = values[peerBox].replace(possibilities, '')
                assign_value(values, peerBox, values[peerBox])
    return values


def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in unitlist:  # independient search by every unit
        for num in range(1, 10):
            # find the number of times where num appears in a unit
            digit = [box for box in unit if str(num) in values[box]]
            if len(digit) == 1:
                # if this appers once in a unit then assgin digit to the box 
                values[digit[0]] = str(num)
                assign_value(values, digit[0], values[digit[0]])
    return values


def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Using the Eliminate Strategy
        values = eliminate(values)
        # Using the Only Choice Strategy
        values = only_choice(values)
        # Appliying naked twins strategy
        values = naked_twins(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])

        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after

        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values


def search(values):

    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)

    if values is False:
        return False  ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values  ## Solved!

    # Choose one of the unfilled squares with the fewest possibilities
    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)

    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

    return attempt


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = search(grid_values(grid))

    return values;


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    # mine
    # diag_sudoku_grid = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'

    solution = solve(diag_sudoku_grid)
    display(solution)

    try:
        from visualize import visualize_assignments

        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
