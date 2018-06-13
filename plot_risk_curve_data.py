import h5py

with h5py.File('dat_analysis/new_risk_homogeneous/'.format(self.path), 'r') as model_data_file:
    model_array_list = model_data_file['array_list'][:]