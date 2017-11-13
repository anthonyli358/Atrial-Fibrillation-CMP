settings = dict(
    structure=dict(
        size=(1, 200, 200),  # (z, y, x)
        refractory_period=50,
        dysfunction_parameter=0.05,  # fraction of dysfunctional cells
        dysfunction_probability=0.05,
        x_coupling=0.8,  # fraction of x linkage
        y_coupling=.2,
        z_coupling=.01,
        seed=None,
    ),
    sim=dict(
        pacemaker_period=220,  # pacemaker activation period
        runtime=1000,
    ),
    viewer=dict(
        cross_view =True,
        save=False,  # save file?
        cross_pos=50,
        interval=20,  # length of each frame in milliseconds
    ),
)
