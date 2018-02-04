import cProfile

from viewer import Viewer


model_viewer = Viewer('12-06_00-05-40 (25)')

# model_viewer.plot_model_stats()
data = model_viewer.import_data()
circuit = model_viewer.circuit_search(data, (10, 50, 25), 500)
model_viewer.animate_model_array(data, layer=0, cross_view=True, cross_pos=25)
model_viewer.plot_circuit_3d(circuit)
