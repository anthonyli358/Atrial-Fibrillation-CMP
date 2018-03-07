import operator
import numpy as np
from direction import Direction
from utility_methods import *
import matplotlib.pyplot as plt


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
                # disallow circuit path through discontinuous boundaries
                (z, y, x) = tuple(map(operator.add, current_point, trial_direction))
                if z < 0 or x < 0:
                    raise IndexError
                trial_direction = Direction.random()

        except IndexError:
            valid_moves = [i for i in Direction.all_directions if i != trial_direction]
            # corner cases (literally)
            # TODO: Y ALLOWED TO GO ABOVE 200 (mod it)
            # TODO: X AND Z PATH DISALLOWED MAKES WHILE LOOP INFINITE
            # 18-02-05_10-24-24
            (z, y, x) = current_point
            if z == 0:
                valid_moves = [i for i in valid_moves if i != (-1, 0, 0)]
            elif z == 24:
                valid_moves = [i for i in valid_moves if i != (1, 0, 0)]
            if x == 0:
                valid_moves = [i for i in valid_moves if i != (0, 0, -1)]
            elif x == 199:
                valid_moves = [i for i in valid_moves if i != (0, 0, 1)]

            trial_direction = Direction.random(valid_moves)  # change current direction
            while model_array_list[start_time - i][tuple(map(operator.add, current_point, trial_direction))] != 50:
                trial_direction = Direction.random(valid_moves)
        # add tuples element wise
        current_point = tuple(map(operator.add, current_point, trial_direction))
        # make negative y indices positive
        if current_point[1] < 0:
            current_point = (current_point[0], current_point[1] % 200, current_point[2])

        if current_point in path:
            # remove all indices before repeat
            return path[next(i for i in range(len(path)) if path[i] == current_point):]
        path.append(current_point)

    print("no path found")
    return False


def circuit_quantify(model_array_list, circuit, start_time):
    """Quantify circuit based on excitation pattern."""

    circuit_type = "focal"  # focal, re-entry, rotor

    x_min, x_max, y_min, y_max = 199, 0, 199, 0
    for (z, y, x) in circuit:
        x_min = x if x_min > x else x_min
        x_max = x if x_max < x else x_max
        y_min = y if y_min > y else y_min
        y_max = y if y_max < y else y_max

    # aperture boundaries
    x_min = 10 if x_min <= 10 else x_min
    x_max = 189 if x_max >= 189 else x_max
    y_min = 10 if y_min <= 10 else y_min
    y_max = 189 if y_max >= 189 else y_max

    # noise too high for larger aperture when linkage < 1
    aperture_cells = np.ix_([0], [y for y in range(y_min - 10, y_max + 10)], [x for x in range(x_min - 10, x_max + 10)])

    excited_average_list = []
    for i in range(150):  # 3 x refractory period
        excited = np.where(model_array_list[start_time - i][aperture_cells] == 50)
        excited_average_list.append([excited[2] + x_min - 10, excited[1] + y_min - 10])  # (x, y)

    excited_average_list_x = weighted_moving_average([xy_list[0] for xy_list in excited_average_list])
    excited_average_list_y = weighted_moving_average([xy_list[1] for xy_list in excited_average_list])
    excited_moving_average_list = [
        [x, y] for x in excited_average_list_x for y in excited_average_list_y]
    excited_move_list = [np.subtract(excited_moving_average_list[i + 1], excited_moving_average_list[i])
                         for i in range(len(excited_moving_average_list) - 1)]
    # excited_direction = [arr_direction(i) for i in excited_move_list]
    # consecutive_direction = count_max_consecutive(excited_direction)

    # if consecutive_direction >= 10:
    #     circuit_type = "re-entry"
    # TODO: % singular excited move
    # TODO: rotor
    # TODO: incomplete re-entry

    plt.plot(*zip(*excited_move_list))
    # plt.plot(excited_moving_average_list)
    plt.show()

    return excited_moving_average_list
