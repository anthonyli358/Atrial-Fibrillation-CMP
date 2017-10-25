import os
import h5py
import numpy as np
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
        self.model_array_list = np.zeros(cfg.settings['sim']['runtime'])
        self.model_data_dict = dict(
            excited=np.zeros(cfg.settings['sim']['runtime']),
            resting=np.zeros(cfg.settings['sim']['runtime']),
            refractory=np.zeros(cfg.settings['sim']['runtime']),
            failed=np.zeros(cfg.settings['sim']['runtime'])
        )

        # Create output directories if they don't exist
        if not os.path.exists(os.path.join('data', model.seed, 'data_files')):
            os.makedirs(os.path.join('data', model.seed, 'data_files'))

        # Create a copy of the config file with parameters of initialisation
        fd, new_path = mkstemp()
        with open(new_path, 'w') as new_file:
            with open('config.py') as old_file:
                for line in old_file:
                    new_file.write(line.replace('seed=None', 'seed={}'.format(model.seed)))
        os.close(fd)  # prevent file descriptor leakage
        move(new_path, os.path.join('data', model.seed, 'config.py'))  # move new file

    def update_model_stats(self):
        """Update statistic lists for the current model iteration."""

        model_keys = ['excited', 'resting', 'refractory, ''failed']
        model_values = [np.sum(self.model.excited), np.sum(self.model.resting),
                        np.sum(self.model.excited) - np.sum(self.model.resting), np.sum(self.model.inactive)]

        for k, v in zip(model_keys, model_values):
            self.model_data_dict[k][self.model.time] = v

    def output_model_stats(self):
        """Output statistics in HDF5 file format for rapid output and analysis."""

        print('outputting model statistics...')

        model_data_file = h5py.File(os.path.join('data/{}/data_files/model_statistics'.format(self.model.seed)), 'w')

        for k, v in self.model_data_dict.items():
            model_data_file.create_dataset(k, data=v, dtype='int32')

    def update_model_array_list(self):
        """Update model array list for the current model iteration."""

        self.model_array_list[self.model.time] = self.model.model_array
