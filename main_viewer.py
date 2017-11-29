import cProfile

from viewer import Viewer


model_viewer = Viewer('11-29_10-36-12')

# model_viewer.plot_model_stats()
# model_viewer.animate_model_array(cross_view=True, cross_pos=80, remove_refractory=True)
model_viewer.plot_model_array()
# model_viewer.plot_d3()
