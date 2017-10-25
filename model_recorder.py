import os
import h5py
from collections import OrderedDict
from shutil import move
from tempfile import mkstemp


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
        self.model_list = []
        self.model_data = OrderedDict([('excited', []), ('refractory', []), ('resting', []), ('failed', [])])

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

    def generate_model_stats(self):
        """Add statistics for the current model iteration to a list."""

        model_param = ['excited', 'refractory', 'resting', 'failed']
        model_append = [self.model.excited, self.model.refractory, self.model.resting, self.model.failed]

        for param_list, x in zip(model_param, model_append):
            self.model_data[param_list].append(x)

    def output_model_stats(self):
        """Output statistics in HDF5 file format for rapid output and analysis."""

        print('outputting model statistics...')

        model_data_file = h5py.File(os.path.join('data/{}/data_files/model_statistics'.format(self.model.seed)), 'w')

        for k, v in self.model_data.items():
            model_data_file.create_dataset(k, data=v)

# TODO: OUTPUT MODEL AT EACH TIMESTEP OR OVERALL?
