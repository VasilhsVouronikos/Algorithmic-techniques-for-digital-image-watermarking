import os
import sys
import numpy as np
import cv2
import ast
import matplotlib.pyplot as plt
from scipy.signal.signaltools import wiener
from PIL import Image
from skimage.util import random_noise

ATTACK = sys.argv[1]
IMAGE = sys.argv[2]
ARGS = sys.argv[3]


class attackModel:

	def __init__(self):
		self.f_info = open('attack_info.txt','a')
		return

	def attackImage(self,image,attack_type,args):
		if(attack_type == 'filter'):
			ftype = args[0]
			kernel = args[1]
			print(type(args))
			self.filter(image,ftype,kernel)
		if(attack_type == 'jpeg'):
			quality = args[0]
			self.JPEGcompression(IMAGE,quality)
		if(attack_type == 'scale'):
			per = args[0] / 100
			self.scale(image,per)
		if(attack_type == 'crop'):
			x = args[0]
			y = args[1]
			ratiox = args[2]
			ratioy = args[3]
			self.crop(image,x,y,ratiox,ratioy)
		if(attack_type == 'rotate'):
			angle = args[0]
			self.rotate(image,angle)
		return

	def openImage(self,path):
		img = Image.open(path)
		return img

	def showImage(self,im):
		plt.imshow(im)
		plt.show()
		return

	def rotate(self,image,angle):
		img = self.openImage(image)
		name = image.split('.')[0]
		rotated_img = img.rotate(angle)
		self.showImage(rotated_img)
		rotated_img.save("rotated_images/rotated" + name + ".jpg")
		self.f_info.write(image + " : " + "rotation = " + str(angle) + " degrees"  + '\n')
		return

	def JPEGcompression(self,image,quality):
		print("Compressing image  = ",image," with quality = ",quality)
		im = self.openImage(image)
		NAME = image.split('.')[0]
		print(NAME)
		im.save("compressed_images/compressed_"+ NAME + str(quality) + ".jpg",
			optimize = True, 
			quality = quality)
		self.f_info.write(image + " : " + "compression_quality = " + str(quality) +  '\n')
		return

	def scale(self,image,ratio):
		img = self.openImage(image)
		im = np.array(img)
		name = image.split('.')[0]
		w = int(im.shape[0] * ratio)
		h = int(im.shape[1] * ratio)
		resized_img = cv2.resize(im,(w,h),interpolation = cv2.INTER_AREA)
		resized_img = Image.fromarray(resized_img)
		resized_img.save("scaled_images/scaled_" + name + ".jpg")
		self.f_info.write(image + " : " + "scale = " + str(ratio) + '\n')
		return

	def crop(self,image,x,y,ratiox,ratioy):
		img = self.openImage(image)
		im = np.array(img)
		name = image.split('.')[0]
		crop_img = im[y:y + ratiox, x:x + ratioy]
		crop_img = Image.fromarray(crop_img)
		crop_img.save("croped_images/filterd_gaussian_" + name + ".jpg")
		self.f_info.write(image + " : " + "cropx = " + str(x) + ":" + str(ratiox) + "cropy = " + str(y) + ":" + str(ratioy) + '\n')
		return

	def filter(self,image,mode,kernel):
		img = self.openImage(image)
		im = np.array(img)
		name = image.split('.')[0]
		print('Applying ',mode,' filter with kernel = ',kernel,' on image = ',image)
		if(mode == 'gaussian'):
			imblur = cv2.GaussianBlur(im,kernel,0)
			self.showImage(imblur)
			imblur = Image.fromarray(imblur)
			imblur.save("filtered_images/filterd_gaussian_" + name + ".jpg")
			self.f_info.write(image + " : " + "filter = " + mode + " with kernel = " + str(kernel) + '\n')
		if(mode == 'median'):
			medianim = cv2.medianBlur(im,kernel)
			self.showImage(medianim)
			medianim = Image.fromarray(medianim)
			medianim.save("filtered_images/filterd_median_" + name + ".jpg")
			self.f_info.write(image + " : " + "filter = " + mode + " with kernel = " + str(kernel) + '\n')
		if(mode == 'average'):
			blurim = cv2.blur(im,kernel)
			self.showImage(blurim)
			blurim = Image.fromarray(blurim)
			blurim.save("filtered_images/filterd_average_" + name + ".jpg")
			self.f_info.write(image + " : " + "filter = " + mode + " with kernel = " + str(kernel) + '\n')
		if(mode == 'gamma'):
			Correctedim = 255 * (im/255)**(1/kernel)
			self.showImage(Correctedim)
		if(mode == 'weiner'):
			filteredim = wiener(im, kernel,None)
			self.showImage(filteredim)
		if(mode == 'sharpening'):
			kernel = np.array([[0, -1, 0], 
                   				[-1, 5,-1], 
                   				[0, -1, 0]])
			image_sharp = cv2.filter2D(im, -1, kernel)
			self.showImage(image_sharp)
			image_sharp = Image.fromarray(image_sharp)
			image_sharp.save("filtered_images/filterd_sharpened_" + name + ".jpg")
			self.f_info.write(image + " : " + "filter = " + mode + " with kernel = " + str(kernel) + '\n')
		if(mode == "s&p"):
			noise_img = random_noise(img, mode='s&p',amount=0.3)
			noise_img = np.array(255*noise_img, dtype = 'uint8')
			self.showImage(noise_img)
		return

if __name__ == '__main__':
	model = attackModel()
	args = ast.literal_eval(ARGS)
	model.attackImage(IMAGE,ATTACK,args)
	