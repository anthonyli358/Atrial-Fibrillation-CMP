import time
import af_model as af
import numpy as np

structural_homogeneity = .05  # Probability of transverse connections
dysfunction_parameter = .05  # Fraction of dysfunctional cells
dysfunction_probability = .05
substrate_size = (200, 200, 10)
pacemaker_period = 220  # pacemaker activation period
refractory_period = 50
runtime = 1000
layer_linkage = .1

start = time.time()
print('GENERATING SUBSTRATE')

substrate = af.Substrate(substrate_size, structural_homogeneity,
                         dysfunction_parameter, dysfunction_probability, refractory_period, layer_linkage)

print('RUNNING SIMULATION')

results = af.simulation(runtime, pacemaker_period, substrate)

runtime = time.time() - start
print('SIMULATION COMPLETE IN {:.1f} SECONDS'.format(runtime))

# np.save('rotor_formation(0.18,0.1,0.1)x', results)

# print(results[:,:,:,0])
print('ANIMATING RESULTS')
af.animate(results, cross_view=True) # Cut through
# af.animate(results[:,:,:,0])  # Normal view
