import os
import sys
import numpy as numpy
import cv2


ATTACK = sys.argv[1]
IMAGE = sys.argv[2]



class attackModel:

	def __init__(self):
		self.ATTACK_LIST = {

			"COMPRESION" : None,
			"GAUSIAN_NOISE" : None,
			"ROTATION" : None,
			"SCALING" : None,
			"CROPING" : None
		}
		return

	def showInfo(self):
		print("Availiable attacks:","\n")
		for f in self.ATTACK_LIST:
			print("attack: ",f,"\n")
		return

	def attackImage(self,image,attack_type):
		return

	def openImage(self,path):
		img = cv2.imread(path)
		return img

	def showImage(self,im):
		cv2.imshow('filtered image',im)
		cv2.waitKey(0)
		return

if __name__ == '__main__':
	model = attackModel()
	model.showInfo()