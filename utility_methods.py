import os


def create_dir(dir_name):
    if not os.path.exists('data/{}'.format(dir_name)):
        os.makedirs('data/{}'.format(dir_name))


def average(list):
    return int(sum(list) / len(list))


def count_max_consecutive(list, arg):
    max_count = 0
    count = 0
    for i in range(len(list) - 1):
        if list[i] == arg:
            count += 1
            max_count = max(max_count, count)
        else:
            count = 0

    return max_count
