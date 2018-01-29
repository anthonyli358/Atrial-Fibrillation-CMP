settings = dict(
    structure=dict(
        size=(10, 200, 200),  # (z, y, x)
        refractory_period=50,
        dysfunction_parameter=0.05,  # fraction of dysfunctional cells
        dysfunction_probability=0.05,
        x_coupling=1.,
        y_coupling=.1,  # probability of y linkage
        z_coupling=.1,
        seed=None  # 11-13_17-02-49 pretty, .61,.61
    ),
    sim=dict(
        pacemaker_period=220,  # pacemaker activation period
        runtime=1000,
    ),
)

# TODO: (ANTHONY) VIEWER ARCHITECTURE - JUST USE MAIN VIEWER (VIEW EACH DATA SET INDIVIDUALLY) CAN CHANGE LATER IF COMPLICATED
# TODO: (ANTHONY) SURFACE IMAGING
# TODO: (ANDY) NUMBER OF LAYERS INVESTIGATION
# TODO: (BOTH) (1) HOW TO VISUALISE - 3D & TRANSPARENT + CROSS SECTIONS
# TODO: (ANTHONY) SHORTEST PATH
# TODO: PYQT VS MAYAVI VS MATPLOTLIB
