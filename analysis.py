import operator
from direction import Direction


def circuit_search(model_array_list, current_point, start_time):
    """Use extensive search algorithm to find rotor."""

    # Start at a time where start point is excited
    while model_array_list[start_time][current_point] != 50:
        start_time += 1

    path = []  # can't use set() as unordered
    trial_direction = (0, 0, 0)
    print(current_point, start_time)
    for i in range(400):
        try:
            while model_array_list[start_time - i][tuple(map(operator.add, current_point, trial_direction))] != 50:
                # disallow circuit at discontinuous boundaries
                (z, y, x) = tuple(map(operator.add, current_point, trial_direction))
                if z < 0 or x < 0:
                    raise IndexError
                trial_direction = Direction.random()
        except IndexError:
            valid_moves = [i for i in Direction.all_directions if i is not trial_direction]
            trial_direction = Direction.random(valid_moves)  # change current direction
            while model_array_list[start_time - i][tuple(map(operator.add, current_point, trial_direction))] != 50:
                trial_direction = Direction.random(valid_moves)
        # add tuples element wise
        current_point = tuple(map(operator.add, current_point, trial_direction))
        print(current_point)

        if current_point in path:
            # remove all indices before repeat
            return [(z, y % 200, x) for (z, y, x) in path[
                                                     next(i for i in range(len(path)) if path[i] == current_point):]]
        path.append(current_point)

    print("no path found")
    return False


def circuit_quantify(circuit, start_time):

    type = "focal"

    cells = []
    # # for i in fertile_lands:
    #     min_x, min_y, max_x, max_y = i[0][0], i[0][1], i[1][0], i[1][1]
    #     cells += [[x, y] for x in range(min_x, max_x + 1) for y in range(min_y, max_y + 1)]

    return type
