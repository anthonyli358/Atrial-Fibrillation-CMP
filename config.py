settings = dict(
    structure=dict(
        size=(10, 200, 200),  # (z, y, x)
        refractory_period=50,
        dysfunction_parameter=0.05,  # fraction of dysfunctional cells
        dysfunction_probability=0.05,
        x_coupling=.59,
        y_coupling=.59,  # probability of y linkage
        z_coupling=.59,
        seed=None  # 11-13_17-02-49 pretty, .61,.61
    ),
    sim=dict(
        pacemaker_period=220,  # pacemaker activation period
        runtime=1000,
    ),
)

# TODO: VIEWER ARCHITECTURE - JUST USE MAIN VIEWER (VIEW EACH DATA SET INDIVIDUALLY) CAN CHANGE LATER IF COMPLICATED
# TODO: SURFACE IMAGING
# TODO: NUMBER OF LAYERS
# TODO: (1) HOW TO VISUALISE
# TODO: SHORTEST PATH
