import config
from model import Model
import numpy as np


def risk_curve_data(runs, repeats, nu_x, nu_yz, angles=False, time=100000):
    data = np.zeros(shape=(runs, repeats, 4), dtype='int')
    params = config.settings["structure"]
    params["x_coupling"], params["yz_coupling"] = nu_x, nu_yz
    params['anglevars'] = angles
    for i in range(runs):
        tissue = Model(**params)
        for j in range(repeats):
            print('Run: {}, Repeat: {}'.format(i,j))
            tissue.excount.fill(0)  # Clear excitation count
            tissue.model_array.fill(0)  # Clear activations
            tissue.activate_pacemaker()  # Initialise new wavefront
            data[i][j][0] = tissue.seed
            data[i][j][1] = False
            data[i][j][2] = -1
            data[i][j][3] = -1
            for t in range(time):
                excitations = tissue.iterate()
                current_tissue = tissue.excount
                if np.intersect1d(current_tissue, [2]):
                    data[i][j][1] = True
                    data[i][j][2] = tissue.maxpos[0]
                    break
                elif not np.any(excitations):  # Maybe terminate when no excited cells instead of all resting?
                    data[i][j][3] = t
                    break
    return data


def gen_risk_pos():
    yzs = [0.11,0.12]
    xs = np.arange(0.8, .85, 0.01)
    save_loc='new_phase_space'  # Only works if folder exists already in data_analysis
    runs = 1
    repeats = 1
    time = 10000
    for yz in yzs:
        for x in xs:
            name = 'data_analysis/{}/{},{}.npy'.format(save_loc, str(x), str(yz))
            print('===========', name)
            result = risk_curve_data(runs, repeats, x, yz, False, time)
            np.save(name, result)

def gen_angle_pos():
    angle_endo = 20
    angle_epi = 45
    averages = np.arange(.3,.5001,.1,)
    save_loc ='angle_space'  # Only works if folder exists already in data_analysis
    runs = 1
    repeats = 1
    time = 10000
    for average in averages:
        angles = [angle_endo,angle_epi,average]
        name = 'data_analysis/{}/{},{},{:.2f}'.format(save_loc,angles[0],angles[1],angles[2])
        print('===========', name)
        result = risk_curve_data(runs,repeats, 0,0,averages,time)
        np.save(name, result)







if __name__ =='__main__':
    gen_angle_pos()

