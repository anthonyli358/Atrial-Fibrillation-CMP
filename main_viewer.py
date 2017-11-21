import cProfile

from viewer import Viewer


model_viewer = Viewer('11-21_14-27-37')

# model_viewer.plot_model_stats()
model_viewer.animate_model_array(cross_view=True, cross_pos=40)
# model_viewer.plot_model_array()
