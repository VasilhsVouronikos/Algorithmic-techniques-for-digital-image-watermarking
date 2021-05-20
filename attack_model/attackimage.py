import os
import sys
import numpy as np
import cv2
import ast
import matplotlib.pyplot as plt
from scipy.signal.signaltools import wiener
from PIL import Image
from skimage.util import random_noise

class attackModel:

	def __init__(self):
		self.f_info = open('attack_info.txt','a')
		return

	def attackImage(self,image,attack_type,args,key,c):
		if(attack_type == 'filter'):
			ftype = args[0]
			kernel = args[1]
			path = self.filter(image,ftype,kernel,key,c)
		if(attack_type == 'jpeg'):
			quality = args[0]
			path = self.JPEGcompression(image,quality,key,c)
		if(attack_type == 'scale'):
			per = args[0] / 100
			self.scale(image,per)
		if(attack_type == 'crop'):
			x = args[0]
			y = args[1]
			ratiox = args[2]
			ratioy = args[3]
			path = self.crop(image,x,y,ratiox,ratioy,key,c)
		if(attack_type == 'rotate'):
			angle = args[0]
			path = self.rotate(image,angle)
		return path

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
		path = "rotated_images/rotated_" + name + ".jpg"
		rotated_img.save(path)
		self.f_info.write(image + " : " + "rotation = " + str(angle) + " degrees"  + '\n')
		return path

	def JPEGcompression(self,image,quality,key,c):
		print("Compressing image  = ",image," with quality = ",quality)
		im = self.openImage(image)
		NAME = image.split('.')[0]
		path = "compressed_images/compressed_"+ NAME + str(quality) + ".jpg"
		im.save(path,
			optimize = True, 
			quality = quality)
		self.f_info.write(image + " : " + "compression_quality = " + str(quality) + " ,extract watermark with key = "+ str(key) + " and c = " + str(c) +  '\n')
		return path

	def scale(self,image,ratio):
		img = self.openImage(image)
		im = np.array(img)
		name = image.split('.')[0]
		w = int(im.shape[0] * ratio)
		h = int(im.shape[1] * ratio)
		resized_img = cv2.resize(im,(w,h),interpolation = cv2.INTER_AREA)
		resized_img = Image.fromarray(resized_img)
		path = "scaled_images/scaled_" + name + ".jpg"
		resized_img.save(path)
		self.f_info.write(image + " : " + "scale = " + str(ratio) + '\n')
		return path

	def crop(self,image,x,y,ratiox,ratioy,key,c):
		
		img = self.openImage(image)
		im = np.array(img)
		name = image.split('.')[0]
		crop_img = im.copy()
		crop_img = Image.fromarray(crop_img)
		path = "croped_images/croped_" + name + ".jpg"
		crop_img.save(path)
		self.f_info.write(image + " : " + "mode = crop" + " ,extract watermark with key = "+ str(key) + " and c = " + str(c) + '\n')
		return path

	def filter(self,image,mode,kernel,key,c):
		img = self.openImage(image)
		im = np.array(img)
		name = image.split('.')[0]
		path = ""
		print('Applying ',mode,' filter with kernel = ',kernel,' on image = ',image)
		if(mode == 'gaussian'):
			imblur = cv2.GaussianBlur(im,kernel,0)
			self.showImage(imblur)
			imblur = Image.fromarray(imblur)
			path = "filtered_images/filterd_gaussian_" + name + ".jpg"
			imblur.save(path)
			self.f_info.write(image + " : " + "filter = " + mode + " with kernel = " + str(kernel) + '\n')
		if(mode == 'median'):
			medianim = cv2.medianBlur(im,kernel)
			self.showImage(medianim)
			medianim = Image.fromarray(medianim)
			path = "filtered_images/filterd_median_" + name + ".jpg"
			medianim.save(path)
			self.f_info.write(image + " : " + "filter = " + mode + " with kernel = " + str(kernel) + '\n')
		if(mode == 'average'):
			blurim = cv2.blur(im,kernel)
			self.showImage(blurim)
			blurim = Image.fromarray(blurim)
			path = "filtered_images/filterd_average_" + name + ".jpg"
			blurim.save(path)
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
			path = "filtered_images/filterd_sharpened_" + name + ".jpg"
			image_sharp.save(path)
			self.f_info.write(image + " : " + "filter = " + mode + " with kernel = " + str(kernel) + '\n')
		if(mode == "noise"):
			mean = float(kernel[0])
			std = float(kernel[1])
			noise_img = random_noise(im, mode='gaussian',var = std)
			noise_img = (255*noise_img).astype(np.uint8)
			self.showImage(noise_img)
			noise_img = Image.fromarray(noise_img)
			path = "filtered_images/filterd_noise_" + name + ".jpg"
			noise_img.save(path)
			self.f_info.write(image + " : " + "filter = " + mode + " ,with mean (μ) = " + str(mean) + " and standard diviation (σ) = " +  
				str(std) + " key = " + str(key) + " c = " + str(c)+ '\n')
		return path

	