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

    path = [current_point]  # can't use set() as unordered
    trial_direction = (1, 0, 0)
    print(current_point, start_time)
    for i in range(1, 400):
        try:
            # make y continuous
            (z, y, x) = current_point
            if y == 199 and model_array_list[start_time - i][(current_point[0], 0, current_point[2])] == 50:
                trial_direction = (0, 1, 0)
            else:
                remaining_moves = list(Direction.all_directions)
                while model_array_list[start_time - i][tuple(map(operator.add, current_point, trial_direction))] != 50:
                    # disallow circuit path through discontinuous boundaries
                    (z, y, x) = tuple(map(operator.add, current_point, trial_direction))
                    if z < 0 or x < 0:
                        raise IndexError
                    # if no remaining moves then excitations caused by pacemaker
                    remaining_moves.remove(trial_direction)
                    if len(remaining_moves) == 0:
                        raise Exception("Traced pacemaker excitations, select a time with atrial fibrillation!")
                    trial_direction = Direction.random(remaining_moves)

        except IndexError:
            remaining_moves = list(Direction.all_directions)
            remaining_moves.remove(trial_direction)
            # corner cases (literally), may have already been removed as the trial_direction
            (z, y, x) = current_point
            if z == 0:
                remaining_moves = [i for i in remaining_moves if i != (-1, 0, 0)]
            elif z == 24:
                remaining_moves = [i for i in remaining_moves if i != (1, 0, 0)]
            if x == 0:
                remaining_moves = [i for i in remaining_moves if i != (0, 0, -1)]
            elif x == 199:
                remaining_moves = [i for i in remaining_moves if i != (0, 0, 1)]

            trial_direction = Direction.random(remaining_moves)  # change current direction
            while model_array_list[start_time - i][tuple(map(operator.add, current_point, trial_direction))] != 50:
                # if no remaining moves then excitations caused by pacemaker
                remaining_moves.remove(trial_direction)
                if len(remaining_moves) == 0:
                    raise Exception("Traced pacemaker excitations, select a time with atrial fibrillation!")
                trial_direction = Direction.random(remaining_moves)

        # add tuples element wise
        current_point = tuple(map(operator.add, current_point, trial_direction))
        # fix y indices, checking better than always creating a new tuple
        if current_point[1] < 0 or current_point[1] > 199:
            current_point = (current_point[0], current_point[1] % 199, current_point[2])

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

    # noise too high for larger aperture due to randomness
    aperture_cells = np.ix_([0], [y for y in range(y_min, y_max)], [x for x in range(x_min, x_max)])

    excited_average_list = []
    for i in range(150):  # 3 x refractory period
        excited = np.where(model_array_list[start_time - i][aperture_cells] == 50)
        if len(excited[0]) > 0:
            excited_average_list.append([average(excited[2] + x_min), average(excited[1]) + y_min])  # (x, y)

    excited_average_list_x = weighted_moving_average([xy_list[0] for xy_list in excited_average_list])
    excited_average_list_y = weighted_moving_average([xy_list[1] for xy_list in excited_average_list])
    excited_moving_average_list = [
        [excited_average_list_x[i], excited_average_list_y[i]] for i in range(len(excited_average_list_x))]
    excited_move_list = [np.subtract(excited_moving_average_list[i + 1], excited_moving_average_list[i])
                         for i in range(len(excited_moving_average_list) - 1)]
    # excited_direction = [arr_direction(i) for i in excited_move_list]
    # consecutive_direction = count_max_consecutive(excited_direction)
    excited_move_list = [np.round(np.subtract(excited_average_list[i + 1], excited_average_list[i])).tolist()
                         for i in range(len(excited_average_list) - 1)]
    percent_singular = count_singular(excited_move_list) / len(excited_move_list)

    if percent_singular >= 0.9:
        circuit_type = "re-entry"
    # TODO: % singular excited move
    # TODO: rotor
    # TODO: incomplete re-entry

    print(len(excited_moving_average_list))
    c = np.arange(len(excited_moving_average_list))
    plt.scatter(*zip(*excited_moving_average_list), c=c)
    # plt.plot(excited_moving_average_list)
    plt.colorbar()
    plt.show()

    return percent_singular
