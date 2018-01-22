import cProfile

from viewer import Viewer


model_viewer = Viewer('12-13_03-42-36')

# model_viewer.plot_model_stats()
model_viewer.animate_model_array(highlight=model_viewer.time_since_last_excitation([1000, 2000]))
# model_viewer.plot_model_array(highlight=model_viewer.time_since_last_excitation([0, 300]))
# model_viewer.plot_d3()
