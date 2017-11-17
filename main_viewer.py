import cProfile

from viewer import Viewer


model_viewer = Viewer('11-14_16-42-40')

model_viewer.plot_model_stats()
model_viewer.animate_model_array()
# model_viewer.plot_model_array()
