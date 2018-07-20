# import numpy as np

settings = dict(
    structure=dict(
        size=[25, 200, 200],  # (z, y, x)
        refractory_period=50,   # tau, refractory period of cells
        dysfunction_parameter=0.05,  # delta, fraction of dysfunctional cells
        dysfunction_probability=0.05,  # epsilon, probability of dysfunctional cell failing
        x_coupling=.8,  # nu_x, probability of x linkage
        yz_coupling=0.13,  # nu_yz, probability of y and z linkage
        angle_toggle=True,  # use angular definition of coupling
        angle_vars=[24, 42, .31],  # theta(z=0), theta(z=max), magnitude of connectivity
        seed=3305209965,  # set a specific seed for structure & epsilon. Defaults from 'uint32'
        dys_seed=None,  # if not None, epsilon fire randomly
        # Ablate a list of points upon tissue initialisation
        # Use read_af_pos_data() in plot_risk_curve_data.py to generate data
        # Can use np.load("file.npy") to set ablated_tissue=sublist[1:], set seed=sublist[0] where sublist=list[0].etc
        ablated_tissue=None  # list of points to ablate, 2mm by default (can change in model.py)
    ),
    sim=dict(
        pacemaker_period=200,  # pacemaker activation period
        runtime=1000,
    ),
    QTviewer=dict(
        x_cross_pos=50,
        y_cross_pos=50,
        z_cross_pos=0,
    ),
    viewer=dict(
        cross_view=True,
        save=False,  # save file?
        cross_pos=50,
        interval=1,  # length of each frame in milliseconds,
    ),
    view='Gauss_filter'
)
