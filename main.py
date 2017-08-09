import time
import af_model as af

structural_homogeneity = .18  # Probability of transverse connections
dysfunction_parameter = .1  # Fraction of dysfunctional cells
dysfunction_probability = .1
substrate_size = (300, 300)
pacemaker_period = 220  # pacemaker activation period
refractory_period = 50
runtime = 1000

start = time.time()
print('GENERATING SUBSTRATE')

substrate = af.Substrate(substrate_size, structural_homogeneity,
                         dysfunction_parameter, dysfunction_probability, refractory_period)

print('RUNNING SIMULATION')

results = af.simulation(runtime, pacemaker_period, substrate)

runtime = time.time() - start
print('SIMULATION COMPLETE IN {:.1f} SECONDS'.format(runtime))

print('ANIMATING RESULTS')
af.animate(results, save='testfig2.mp4')
