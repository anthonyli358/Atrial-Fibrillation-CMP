import cProfile

from viewer import Viewer


model_viewer = Viewer('18-02-04_18-14-39')

# model_viewer.plot_model_stats()
data = model_viewer.import_data()
circuit = model_viewer.circuit_search(data, (10, 50, 155), 2000)
# model_viewer.animate_model_array(data, layer=0, cross_view=True, cross_pos=155)
model_viewer.plot_circuit_3d(circuit)
