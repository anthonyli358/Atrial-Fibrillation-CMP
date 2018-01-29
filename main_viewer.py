import cProfile

from viewer import Viewer


model_viewer = Viewer('12-13_03-42-36')

# model_viewer.plot_model_stats()
model_viewer.animate_model_array()
# highlight=model_viewer.circuit_search((0, 91, 44), 1000)
# model_viewer.plot_d3()
