import os
import sys
import numpy as np
import cv2
import ast
import matplotlib.pyplot as plt
from scipy.signal.signaltools import wiener
from PIL import Image
from skimage.util import random_noise
from scipy import ndimage

class attackModel:

	def __init__(self):
		self.f_info = open('attack_info.txt','a')
		return

	def attackImage(self,image,attack_type,args,key,c,m):
		if(attack_type == 'filter'):
			ftype = args[0]
			kernel = args[1]
			path = self.filter(image,ftype,kernel,key,c,m)
		if(attack_type == 'jpeg'):
			quality = args[0]
			path = self.JPEGcompression(image,quality,key,c,m)
		if(attack_type == 'scale'):
			per = args[0] / 100
			path = self.scale(image,per,m)
		if(attack_type == 'crop'):
			path = self.crop(image,args)
		if(attack_type == 'rotate'):
			angle = args[0]
			path = self.rotate(image,angle,m)
		return path

	def openImage(self,path):
		img = Image.open(path)
		return img

	def showImage(self,im):
		plt.imshow(im)
		plt.show()
		return

	def rotate(self,image,angle,m):
		img = self.openImage(image)
		name = image.split('.')[0]
		rotated_img = img.rotate(angle,resample = 0)
		self.showImage(rotated_img)
		path = "rotated_images/rotated_" + name + ".jpg"
		rotated_img.save(path,quality=100,subsampling=0)
		self.f_info.write(image + " : " + "rotation = " + str(angle) + " degrees"  + '\n')
		return path

	def JPEGcompression(self,image,quality,key,c,m):
		print("Compressing image  = ",image," with quality = ",quality)
		im = self.openImage(image)
		print(im.filename)
		NAME = image.split('.')[0]
		path = "compressed_images/compressed_"+ m + "_"+ NAME + str(quality) + ".jpg"
		im.save(path,'jpeg',
			quality = quality)
		self.f_info.write(image + " : " + "compression_quality = " + str(quality) + " ,extract watermark with key = "+ str(key) + " and c = " + str(c) +  '\n')
		#im = Image.open(path)
		return path

	def scale(self,image,ratio,m):
		if(m == 'key'):
			img = self.openImage(image)
			im = np.array(img)
			name = image.split('.')[0]
			w = int(im.shape[0] * ratio)
			h = int(im.shape[1] * ratio)
			resized_img = cv2.resize(im,(w,h),interpolation = cv2.INTER_AREA)
			self.showImage(resized_img)
			resized_img = Image.fromarray(resized_img)
			path = "scaled_images/scaled_" + name + ".jpg"
			resized_img.save(path,quality=100,subsampling=0)
			self.f_info.write(image + " : " + "scale = " + str(ratio) + '\n')
		else:
			img = self.openImage(image)
			im = np.array(img)
			name = image.split('.')[0]
			w = int(im.shape[0] * ratio)
			h = int(im.shape[1] * ratio)
			resized_img = cv2.resize(im,(w,h),interpolation = cv2.INTER_AREA)
			self.showImage(resized_img)
			resized_img = cv2.resize(resized_img,(im.shape[0],im.shape[1]),interpolation = cv2.INTER_AREA)
			self.showImage(resized_img)
			path = "scaled_images/scaled_" + name + ".jpg"
			resized_img = Image.fromarray(resized_img)
			resized_img.save(path,quality=100,subsampling=0)
		return path

	def crop(self,image,args):
		path = ""
		img = self.openImage(image)
		im = np.array(img)
		NAME = image.split('.')[0]
		arg1 = int(args[0])
		arg2 = int(args[1])
		arg3 = args[2]
		if(arg3 == "cols"):
			im[:,:arg1] = 1
			im[:,-arg1:] = 1
			self.showImage(im)
			im = Image.fromarray(im)
			path = "croped_images/croped_cols_" + str(arg1) + "_" + NAME + ".jpg"
			im.save(path,quality=100,subsampling=0)
		elif(arg3 == "rows"):
			im[0:arg1,:] = 1
			im[im.shape[0] - arg1:im.shape[0],:] = 1
			self.showImage(im)
			im = Image.fromarray(im)
			path = "croped_images/croped_rows_" + str(arg1) + "_" + NAME + ".jpg"
			im.save(path,quality=100,subsampling=0)
		else:
			if(arg3 == "white"):
				im[0:arg1,0:arg1] = 255
				#im[im.shape[0] - arg1:im.shape[0],:] = 1
				self.showImage(im)
				im = Image.fromarray(im)
				path = "croped_images/croped_wite_" + str(arg1) + "_" + NAME + ".jpg"
				im.save(path,quality=100,subsampling=0)
			elif(arg3 == "black"):
				im[0:arg1,0:arg1] = 0
				#im[im.shape[0] - arg1:im.shape[0],:] = 1
				self.showImage(im)
				im = Image.fromarray(im)
				path = "croped_images/croped_black_" + str(arg1) + "_" + NAME + ".jpg"
				im.save(path,quality=100,subsampling=0)
			else:
				im[192:256,256:320] = 255
				self.showImage(im)
				im = Image.fromarray(im)
				path = "croped_images/croped_center_" + str(arg1) + "_" + NAME + ".jpg"
				im.save(path,quality=100,subsampling=0)
		return path

	def filter(self,image,mode,kernel,key,c,m):
		img = self.openImage(image)
		im = np.array(img)
		name = image.split('.')[0]
		path = ""
		print('Applying ',mode,' filter with kernel = ',kernel,' on image = ',image)
		if(mode == 'gaussian'):
			imblur = cv2.GaussianBlur(im,kernel,0.5,0.5)
			self.showImage(imblur)
			imblur = Image.fromarray(imblur)
			path = "filtered_images/filterd_gaussian_" + name + ".jpg"
			imblur.save(path,quality=100,subsampling=0)
			self.f_info.write(image + " : " + "filter = " + mode + " with kernel = " + str(kernel) + '\n')
		if(mode == 'median'):
			medianim =  ndimage.median_filter(im, size=(2,2))
			self.showImage(medianim)
			medianim = Image.fromarray(medianim)
			path = "filtered_images/filterd_median_" + name + ".jpg"
			medianim.save(path,quality=100,subsampling=0)
			self.f_info.write(image + " : " + "filter = " + mode + " with kernel = " + str(kernel) + '\n')
		if(mode == 'average'):
			blurim = cv2.blur(im,kernel)
			self.showImage(blurim)
			blurim = Image.fromarray(blurim)
			path = "filtered_images/filterd_average_" + name + ".jpg"
			blurim.save(path,quality=100,subsampling=0)
			self.f_info.write(image + " : " + "filter = " + mode + " with kernel = " + str(kernel) + '\n')
		if(mode == 'gamma'):
			gamma = kernel
			invGamma = 1.0 / gamma
			table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
			img = cv2.LUT(im, table)
			img = Image.fromarray(img)
			self.showImage(img)
			path = "filtered_images/filterd_gamma_" + name + ".jpg"
			img.save(path,quality=100,subsampling=0)
		if(mode == 'sharpening'):
			kernel = np.array([[0, -1, 0], 
                   				[-1, 5,-1], 
                   				[0, -1, 0]])
			image_sharp = cv2.filter2D(im, -1, kernel)
			self.showImage(image_sharp)
			image_sharp = Image.fromarray(image_sharp)
			path = "filtered_images/filterd_sharpened_" + name + ".jpg"
			image_sharp.save(path,quality=100,subsampling=0)
			self.f_info.write(image + " : " + "filter = " + mode + " with kernel = " + str(kernel) + '\n')
		if(mode == "noise"):
			mean = float(kernel[0])
			std = float(kernel[1])
			noise_img = random_noise(im, mode='gaussian',var = std)
			noise_img = (255*noise_img).astype(np.uint8)
			self.showImage(noise_img)
			noise_img = Image.fromarray(noise_img)
			path = "filtered_images/filterd_noise_" + name + ".jpg"
			noise_img.save(path,quality=100,subsampling=0)
			self.f_info.write(image + " : " + "filter = " + mode + " ,with mean (μ) = " + str(mean) + " and standard diviation (σ) = " +  
				str(std) + " key = " + str(key) + " c = " + str(c)+ '\n')
		if(mode == 'HEQ'):
			img = cv2.cvtColor(im, cv2.COLOR_BGR2YCrCb)
			y, cr, cb = cv2.split(img)
			y_eq = cv2.equalizeHist(y)
			img_y_cr_cb_eq = cv2.merge((y_eq, cr, cb))
			img_rgb = cv2.cvtColor(img_y_cr_cb_eq, cv2.COLOR_YCR_CB2BGR)
			self.showImage(img_rgb)
			img_rgb = Image.fromarray(img_rgb)
			path = "filtered_images/filterd_HEQ_" + name + ".jpg"
			img_rgb.save(path,quality=100,subsampling=0)
		return path

	