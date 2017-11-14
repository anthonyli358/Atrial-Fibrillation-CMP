import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import glob

# ########## Correction Code #########
# data = np.load('phase_space_attempt1.npy').reshape(8,2500,5)
# for section in data:
#     actual = []
#     actual2 = []
#     actual3 = []
#     for i, res in enumerate(section):
#         actual.append(i*section[i,2]-section[i-1,2]*(i-1))
#         actual2.append(i * section[i,4] - section[i - 1,4] * (i - 1))
#         actual3.append(np.sqrt(i * section[i,3] * section[i,3] - section[i - 1,3] * section[i - 1,3] * (i - 1)))
#     section[:, 2] = actual
#     section[:, 4] = actual2
#     section[:, 3] = actual3
# data = data.reshape(200,100,5)
# ########## Correction Code #########

data = np.load('Phase_Spaces/Fixed_Data1.npy')

plt.figure()
plt.imshow(data[:,:,2], extent=(0,0.99,0.995,0))
plt.figure()
plt.imshow(data[:,:,4], extent=(0,0.99,0.995,0))
plt.figure()
plt.imshow(data[:,:,3], extent=(0,0.99,0.995,0))

#
# # Data Extraction
# data = []
# for i in glob.glob('phase_space_11_11_21*.npy')+glob.glob('phase_space_11_11_22*.npy'):
#     data.append(np.load(i))
# comb = []
# for i in data[1:]:
#     comb.extend(i)
# # Data Extraction

comb=np.load('Phase_Spaces/Data2.npy')
plt.figure()
plt.imshow(comb[:,:,2], extent=(0,1,1,0))
plt.colorbar()
plt.figure()
plt.imshow(comb[:,:,4], extent=(0,1,1,0))
plt.colorbar()
plt.figure()
plt.imshow(comb[:,:,3], extent=(0,1,1,0))
plt.colorbar()



plt.show()
