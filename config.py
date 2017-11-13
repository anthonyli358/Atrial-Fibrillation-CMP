settings = dict(
    structure=dict(
        size=(200, 200, 1),  # (y, x, z)
        refractory_period=50,
        dysfunction_parameter=0.05,  # fraction of dysfunctional cells
        dysfunction_probability=0.05,
        y_coupling=.13,  # probability of y linkage
        z_coupling=.01,
        seed=None
    ),
    sim=dict(
        pacemaker_period=220,  # pacemaker activation period
        runtime=1000,
    )
)

# TODO: CHECK POSSIBLE TO GET A WAVEFRONT / FIBRILLATION
# TODO: 1D, 2D, 3D
