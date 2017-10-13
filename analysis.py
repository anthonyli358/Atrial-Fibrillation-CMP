import numpy as np


def sum_test(results, refractory_period, threshold):
    count = np.array([np.count_nonzero(result == refractory_period) for result in results])
    fraction = np.count_nonzero(count > threshold) / len(count)
    return count, fraction
