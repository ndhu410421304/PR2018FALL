import numpy as np
import cv2

m = np.fromfile('mask.dat', dtype=int)
m = np.reshape(m, (-1, 2))
Z = np.float32(m)


print(m[3])
print(Z[3])

print(np.sum([255,255,255]).sum())