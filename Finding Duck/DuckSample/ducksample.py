import sys
import cv2 as cv
import numpy as np


def main():
	cv.namedWindow('duckimg', cv.WINDOW_AUTOSIZE)
	img = cv.imread('full_duck.jpg')
	#if not img:
	#	print('nothing been reas')
	b,g,r = cv.split(img)
	cv.imshow('rduckimg',r)
	cv.imshow('duckimg', img)
	
	c = cv.waitKey(1200)
	if c >= 0: 
		return -1
	return 0
	
if __name__ == "__main__":
	main()