from analysis import *
from ecg import ECG
from viewer import Viewer


path = "12-06_02-14-33 (rotor_52)"

model_viewer = Viewer(path)
data = model_viewer.import_data()

# circuit = circuit_search(data, (12, 10, 100), 1000)
# circuit_type = circuit_quantify(data, circuit, 500, path=path)
# print(circuit_type)
# model_viewer.plot_circuit_3d(circuit)

# model_viewer.plot_model_stats()
model_viewer.plot_model_array(data, start=1235)
# model_viewer.animate_model_array(data, layer=0)

circuit = circuit_search(data, (12, 136, 113), 500)
circuit_type = circuit_quantify(data, circuit, 500)
print(circuit_type)
# model_viewer.plot_circuit_3d(circuit)

# model_ecg = ECG([137, 100], 3, path)
# model_ecg.plot_ecg([i for i in range(len(data))], model_ecg.ecg())
