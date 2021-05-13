import sys
import numpy as np
from collections import Counter
import matplotlib.patches

def createEllipticDisk(array,R1_X,R1_Y,W,C_X,C_Y,cell_w,cell_h):
	R2_X = (R1_X - W)
	R2_Y = (R1_Y - W)
	RES1 = []
	COORD1 = []
	RES2 = []
	COORD2 = []
	angle = 0

	for x in range(cell_w):
		for y in range(cell_h):
			if((((x - C_X)**2) / (R1_X **2) + ((((y - C_Y)**2)) / (R1_Y **2)))<= 1):
				COORD1.append((x,y))
				RES1.append(array[x][y])
	for x in range(cell_w):
		for y in range(cell_h):
			if((((x - C_X)**2) / (R2_X **2) + ((((y - C_Y)**2)) / (R2_Y **2))) <= 1):
				COORD2.append((x,y))
				RES2.append(array[x][y])

	intersection1 = Counter(RES1) & Counter(RES2)
	intersection2 = Counter(COORD1) & Counter(COORD2)

	RES_unique = list(set((Counter(RES1) - intersection1).elements()))
	COORD_unique = list(set((Counter(COORD1) - intersection2).elements()))

	return RES_unique,COORD_unique
