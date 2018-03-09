from analysis import *
from ecg import ECG
from viewer import Viewer


path = "mechanism/re-entry/18-03-08_20-24-36 (85, 136)"

model_viewer = Viewer(path)
data = model_viewer.import_data()

circuit = circuit_search(data, (12, 136, 85), 800)
circuit_type = circuit_quantify(data, circuit, 800)
# print(circuit_type)
# model_viewer.plot_circuit_3d(circuit)

# model_viewer.plot_model_stats()
model_viewer.animate_model_array(data[:200], layer=0)

# model_ecg = ECG([137, 100], 3, path)
# model_ecg.plot_ecg([i for i in range(len(data))], model_ecg.ecg())
