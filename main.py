import time
import af_model as af
import numpy as np

structural_homogeneity = .16  # Probability of transverse connections
dysfunction_parameter = .1  # Fraction of dysfunctional cells
dysfunction_probability = .1
substrate_size = (500, 500, 1)
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
# af.animate(results[:,:,50,:]) # Cut through
af.animate(results[:,:,:,0])  # Normal view
