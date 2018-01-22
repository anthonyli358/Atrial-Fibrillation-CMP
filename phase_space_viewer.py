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



# # Data Extraction
# data = []
# for i in glob.glob('data_file_32_200_200*.npy'):
#     data.append(np.load(i))
# comb = []
# for i in data[:]:
#     comb.extend(i)
# # Data Extraction
# comb = np.array(comb)
# print(comb)
# comb = comb[np.lexsort((comb[:,1],comb[:,0]))]    # Sort Data
# print(comb[::100])
# comb = np.reshape(comb, (50,50,5))
# # np.save('Phase_Spaces/32_200_200.npy', comb)

# comb = np.load('3D_Data.npy')
# plt.figure()
# plt.imshow(comb[:,:,2], extent=(0,1,.99,0))
# plt.colorbar()
# plt.xlabel('yz_linkage')
# plt.ylabel('x_linkage')
# plt.title('3D Phase Space')
#
# plt.figure()
# plt.plot(comb[99,:,1], comb[50,:,2])
# plt.xlabel('yz_linkage')
# plt.ylabel('Mean Risk of Atrial Fibrillation')


comb=np.load('Phase_Spaces/16_200_200.npy')
plt.figure()
plt.imshow(comb[:,:,2], extent=(0,1,1,0))
plt.colorbar()
plt.xlabel('yz_linkage')
plt.ylabel('x_linkage')
plt.title('Risk')

plt.figure()
plt.imshow(comb[:,:,4], extent=(0,1,1,0))
plt.colorbar()
plt.xlabel('yz_linkage')
plt.ylabel('x_linkage')
plt.title('Transmission')

plt.figure()
plt.imshow(comb[:,:,3], extent=(0,1,1,0))
plt.colorbar()
plt.xlabel('yz_linkage')
plt.ylabel('x_linkage')
plt.title('Risk Deviation')

fig = plt.figure()

# names = glob.glob('Phase_Spaces/*_200_200.npy')
names = ['Phase_Spaces/1_200_200.npy', 'Phase_Spaces/2_200_200.npy',
         'Phase_Spaces/4_200_200.npy', 'Phase_Spaces/8_200_200.npy',
         'Phase_Spaces/16_200_200.npy', 'Phase_Spaces/32_200_200.npy']
print(names)
compilation = []
for i in names:
    compilation.append(np.load(i)[:,:,2])

for num, i in enumerate(compilation):
    ax = fig.add_subplot(100+len(names) * 10  + 1+num)
    ax.set_title(names[num][13:-4])
    ax.imshow(i, extent =(0,1,1,0))

fig.show()


plt.show()
