#this is the program for testing if I do some wrong in programing
import numpy as np
import cv2

m = np.fromfile('mask.dat', dtype=int)
m = np.reshape(m, (-1, 2))
Z = np.float32(m)
maskimg = cv2.imread("mask.png",3)


print(m[3])
print(Z[3])

print(np.sum([255,255,255]).sum())

print(np.sum(m).sum())

print(maskimg)

m2 = np.sum(maskimg)
print(m2)

print("A")

arr = np.array(maskimg[13674:13720][2456:2502])
print(arr)

print(maskimg[13697][2479].sum())