settings = dict(
    structure=dict(
        size=(1, 200, 200),  # (z, y, x)
        refractory_period=50,
        dysfunction_parameter=0.05,  # fraction of dysfunctional cells
        dysfunction_probability=0.05,
        x_coupling=1,
        y_coupling=1,  # probability of y linkage
        z_coupling=1,
        seed=None # 11-13_17-02-49 pretty, .61,.61
    ),
    sim=dict(
        pacemaker_period=220,  # pacemaker activation period
        runtime=1220,
    ),
    viewer=dict(
        cross_view =True,
        save=False,  # save file?
        cross_pos=50,
        interval=20,  # length of each frame in milliseconds
    ),
)
