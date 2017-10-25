settings = dict(
    structure=dict(
        x_structural_homogeneity=.13,  # Probability of transverse connections
        y_structural_homogeneity=.01,
        dysfunction_parameter=0.05,  # Fraction of dysfunctional cells
        dysfunction_probability=0.05,
        substrate_size=(200, 200, 1),  # Planes rows columns
        refractory_period=50,
        seed=None
    ),
    sim=dict(
        pacemaker_period=220,  # pacemaker activation period
        runtime=1000,
    ),
    viewer=dict(
        cross_view =False,  # Enable display of cut_through
        cross_pos=50,  # Location of cut_through
        interval=20,  # Length of each frame in milliseconds
        save=None,  # Specify location to save animation to
    )
)