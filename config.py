settings = dict(
    structure=dict(
        s_structural_homogeneity=0.01,  # Probability of transverse connections
        p_structural_homogeneity=0,
        dysfunction_parameter=0.05,  # Fraction of dysfunctional cells
        dysfunction_probability=0.05,
        substrate_size=(200, 200, 1),
        refractory_period=50,
        seed=None
    ),
    sim=dict(
        pacemaker_period=220,  # pacemaker activation period
        runtime=1000,
    )
)