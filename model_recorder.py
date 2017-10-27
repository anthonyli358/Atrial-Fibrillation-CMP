import datetime
import h5py
import numpy as np
import os

from functools import reduce
from operator import mul
from shutil import move
from tempfile import mkstemp

import config as cfg


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
        self.path = model.seed if cfg.settings['structure']['seed'] is None else datetime.datetime.now().strftime(
            '%y-%m-%d_%H-%M-%S')
        self.model_array_list = []
        self.model_stat_dict = {k: np.zeros(cfg.settings['sim']['runtime'] + 1) for k in
                                ['excited', 'resting', 'refractory', 'inactive']}

        # Create output directories if they don't exist
        if not os.path.exists(os.path.join('data', self.path, 'data_files')):
            os.makedirs(os.path.join('data', self.path, 'data_files'))

        # Create a copy of the config file with parameters of initialisation
        fd, new_path = mkstemp()
        with open(new_path, 'w') as new_file:
            with open('config.py') as old_file:
                for line in old_file:
                    new_file.write(line.replace('seed=None', 'seed={}'.format(model.seed)))
        os.close(fd)  # prevent file descriptor leakage
        move(new_path, os.path.join('data', self.path, 'config.py'))  # move new file

    def update_model_stats(self):
        """Update statistic lists for the current model iteration."""

        # Defining and zipping lists in order using a for loop (better coding practice) would be slower
        self.model_stat_dict['excited'][self.model.time] = np.sum(self.model.excited)
        self.model_stat_dict['resting'][self.model.time] = np.sum(self.model.resting)
        self.model_stat_dict['refractory'][self.model.time] = reduce(mul, cfg.settings['structure']['size']) - (
            np.sum(self.model.excited) + np.sum(self.model.resting))
        self.model_stat_dict['inactive'][self.model.time] = np.sum(self.model.inactive)

    def output_model_stats(self):
        """Output statistics in HDF5 file format for rapid output and analysis."""

        print("outputting model statistics...")

        with h5py.File('data/{}/data_files/model_statistics'.format(self.path), 'w') as model_stats_file:
            for k, v in self.model_stat_dict.items():
                model_stats_file.create_dataset(k, data=v, dtype='int32')

    def update_model_array_list(self):
        """Update model array list for the current model iteration."""

        self.model_array_list.append(self.model.model_array)

    def output_model_array_list(self):
        """Output numpy array list representing the model state for the current iteration in HDF5 file format."""

        print("outputting model array list...")

        with h5py.File('data/{}/data_files/model_array_list'.format(self.path), 'w') as model_data_file:
            model_data_file.create_dataset('array_list', data=self.model_array_list, dtype='int16')
