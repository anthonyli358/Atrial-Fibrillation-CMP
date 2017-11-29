import os


def create_dir(dir_name):
    if not os.path.exists('data/{}'.format(dir_name)):
        os.makedirs('data/{}'.format(dir_name))
