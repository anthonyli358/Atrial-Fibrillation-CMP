import datetime
import h5py
import numpy as np
import pandas as pd
from functools import reduce
from operator import mul
from shutil import move
from tempfile import mkstemp

import config as cfg
from utility_methods import *


class ModelRecorder:
    """
    A class to output the data for the model as it develops.
    """

    def __init__(self, model):
        """
        World Recorder Initialisation
        :param model: The model being recorded
        """
        self.model = model
        self.path = datetime.datetime.now().strftime('%y-%m-%d_%H-%M-%S')
        self.model_array_list = []
        self.model_stat_dict = {k: np.zeros(cfg.settings['sim']['runtime'] + 1, dtype='int32') for k in
                                ['excited', 'resting', 'refractory', 'failed']}

        create_dir('{}/data_files'.format(self.path))

        # Create a copy of the config file with parameters of initialisation
        fd, new_path = mkstemp()
        with open(new_path, 'w') as new_file:
            with open('config.py') as old_file:
                for line in old_file:
                    new_file.write(line.replace('seed=None', 'seed={}'.format(model.seed)))
        os.close(fd)  # prevent file descriptor leakage
        move(new_path, 'data/{}/config.py'.format(self.path))  # move new file

    def update_model_stat_dict(self):
        """Update statistic lists for the current model iteration."""

        stat_keys = ['excited', 'resting', 'refractory', 'failed']  # define manually as model_stats_dict not ordered
        stat_values = [np.sum(self.model.excited),
                       np.sum(self.model.resting),
                       reduce(mul, cfg.settings['structure']['size']) - (
                           np.sum(self.model.excited) + np.sum(self.model.resting)),
                       np.sum(self.model.failed)]

        for k, v in zip(stat_keys, stat_values):
            self.model_stat_dict[k][self.model.time] = v

    def output_model_stat_dict(self):
        """Output statistics in HDF5 file format for rapid output and analysis."""

        print("outputting model statistics...")

        stat_data_frame = pd.DataFrame.from_dict(self.model_stat_dict)
        stat_data_frame.to_hdf('data/{}/data_files/stat_data_frame'.format(self.path), 'stat_data_frame', mode='w')

    def update_model_array_list(self):
        """Update model array list for the current model iteration."""

        self.model_array_list.append(self.model.model_array.copy())

    def output_model_array_list(self):
        """Output numpy array list representing the model state for the current iteration in HDF5 file format."""

        print("outputting model array list...")

        with h5py.File('data/{}/data_files/model_array_list'.format(self.path), 'w') as model_data_file:
            model_data_file.create_dataset('array_list', data=self.model_array_list, dtype='uint8')
