import os,sys
from PIL import Image
import numpy as np
import cv2


def similarity(W1,W2):
	im1 = np.array(openImage(W1))
	im2 = W2

	ret,th = cv2.threshold(im1,170,255,cv2.THRESH_BINARY)

	error_bits = 0
	x = 64
	y = 64

	

	for i in range(x):
		for j in range(y):

			if(th[i,j] != im2[i,j]):
				error_bits = error_bits + 1


	similarity = error_bits / (x * y)


	print("Similarity(logo): " ,1 - similarity)
	


def similaritysip(SIP_OUTPUT,SIP):
	sum_correct = 0

	for i in range(len(SIP)):
		if(SIP_OUTPUT[i] == SIP[i]):
			sum_correct = sum_correct + 1

			
	C = sum_correct / len(SIP)

	return C

def calculate_C(W1,W2,SIP_INPUT,SIP_OUTPUT):
	im1 = np.array(openImage(W1))
	im2 = np.array(openImage(W2))

	mean_val_w1 = np.mean(im1)
	mean_val_w2 = np.mean(im2)
	
	sum1 = 0
	sumw1 = 0
	sumw2 = 0

	sum_correct = 0

	for i in range(64):
		for j in range(64):

			coef1 = np.abs(im1[i,j] - mean_val_w1)
			coef2 = np.abs(im2[i,j] - mean_val_w2)
			A = coef1 * coef2
			sum1 = sum1 + A

			sumw1 = sumw1 + ((im1[i,j] - mean_val_w1)**2)
			sumw2 = sumw2 + ((im2[i,j] - mean_val_w2)**2)


	NC = sum1 / (np.sqrt(sumw1) * np.sqrt(sumw2))

	for i in range(len(SIP_OUTPUT)):
		if(SIP_OUTPUT[i] == SIP_INPUT[i]):
			sum_correct = sum_correct + 1

	C = sum_correct / len(SIP_INPUT)


	print("NC in watermark: ",NC)
	print("C in watermark: ",C)


	return NC,C


def openImage(path):
	img = Image.open(path).convert('L')
	return img

if __name__ == '__main__':
	calculate_C()