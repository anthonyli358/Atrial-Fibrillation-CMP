import cProfile

from viewer import Viewer


model_viewer = Viewer('01-29_18-21-51')

# model_viewer.plot_model_stats()
data = model_viewer.import_data()
model_viewer.animate_model_array(data, highlight=model_viewer.circuit_search(data, (5, 130, 44), 600), layer=3, cross_view=True, cross_pos=44)
# model_viewer.plot_d3()
