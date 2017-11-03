settings = dict(
    structure=dict(
        size=(5, 200, 200),  # (z, y, x)
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
    ),
    viewer=dict(
        cross_view =True,  # Enable display of cut_through
        cross_pos=50,  # Location of cut_through
        interval=20,  # Length of each frame in milliseconds
        save=None,  # Specify location to save animation to
    ),
    output=False,  # Enable or disable file saving
)
