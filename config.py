settings = dict(
    structure=dict(
        y_coupling=.13,  # probability of transverse connections
        dysfunction_parameter=0.05,  # fraction of dysfunctional cells
        dysfunction_probability=0.05,
        size=(200, 200, 1),  # (y, x, z)
        refractory_period=50,
        d3=True,
        z_coupling=.01,
        seed=None
    ),
    sim=dict(
        pacemaker_period=220,  # pacemaker activation period
        runtime=100,
    )
)
