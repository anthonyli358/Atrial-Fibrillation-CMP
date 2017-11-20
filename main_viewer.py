import cProfile

from viewer import Viewer


model_viewer = Viewer('11-20_20-09-43')

# model_viewer.plot_model_stats()
model_viewer.animate_model_array(cross_view=True, cross_pos=80)
# model_viewer.plot_model_array()
