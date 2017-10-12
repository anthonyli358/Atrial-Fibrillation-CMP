import numpy as np

def sum_test(results, refractory_period):
    count = [np.count_nonzero(results == refractory_period) for result in results]
    return count
