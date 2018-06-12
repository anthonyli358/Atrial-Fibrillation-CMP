import config
from model import Model
import numpy as np


def risk_curve_data(runs, repeats, nu_x, nu_yz, nu_av, time=100000):
    data = np.zeros(shape=(runs, repeats, 4))
    params = config.settings["structure"]
    params["x_coupling"], params["yz_coupling"] = nu_x, nu_yz
    tissue = Model(**params)
    for i in range(runs):
        for j in range(repeats):
            data[i][j][0] = tissue.seed
            data[i][j][1] = False
            data[i][j][2] = None
            data[i][j][3] = None
            for t in range(time):
                if t == 0:
                    tissue.activate_pacemaker()
                current_tissue = tissue.iterate()
                if np.intersect1d(current_tissue, [2]):
                    data[i][j][1] = True
                    data[i][j][2] = np.where(current_tissue == 2)
                    break
                elif not np.any(current_tissue):
                    data[i][j][3] = t
                    break
