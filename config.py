settings = dict(
    structure=dict(
        s_structural_homogeneity=.13,  # Probability of transverse connections
        p_structural_homogeneity=.01,
        dysfunction_parameter=0.05,  # Fraction of dysfunctional cells
        dysfunction_probability=0.05,
        substrate_size=(200, 200, 10),
        refractory_period=50,
        seed=3901440440
    ),
    sim=dict(
        pacemaker_period=220,  # pacemaker activation period
        runtime=1000,
    )

)