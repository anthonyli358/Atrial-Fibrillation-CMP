settings = dict(
    structure=dict(
        size=[25, 200, 200],  # (z, y, x)
        refractory_period=50,   # tau, refractory period of cells
        dysfunction_parameter=0.05,  # delta, fraction of dysfunctional cells
        dysfunction_probability=0.05,  # epsilon, probability of dysfunctional cell failing
        x_coupling=0.8,  # nu_x, probability of x linkage
        yz_coupling=.12,  # nu_yz, probability of y and z linkage
        seed=None,  # set a specific seed. Defaults from 'uint32'
        angle_toggle=False,  # Use angular definition of coupling
        angle_vars=[20,45,.35],  # theta(z=0), theta(z=max), magnitude of connectivity
    ),
    sim=dict(
        pacemaker_period=220,  # pacemaker activation period
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
        interval=1,  # length of each frame in milliseconds
    ),
)
