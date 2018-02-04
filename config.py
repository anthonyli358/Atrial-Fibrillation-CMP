settings = dict(
    structure=dict(
        size=(25, 200, 200),  # (z, y, x)
        refractory_period=50,
        dysfunction_parameter=0.05,  # fraction of dysfunctional cells
        dysfunction_probability=0.05,
        x_coupling=1.,
        y_coupling=.061,  # probability of y linkage
        z_coupling=.061,
        seed=None  # 11-13_17-02-49 pretty, .61,.61
    ),
    sim=dict(
        pacemaker_period=220,  # pacemaker activation period
        runtime=3000,
    ),
)


# TODO: (ANDY) NUMBER OF LAYERS INVESTIGATION
