import cv2
import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import dft
from ellipticdisk import createEllipticDisk
from math import sqrt
from PIL import Image
import itertools as it
import threading, queue
import math

print("using opencv version: ",cv2.__version__)


class EmbedPermutation:
	def __init__(self):
		return
	def openImage(self,path):
		img = Image.open(path)
		return img

	def getFFTTransform(self,image,t):
		dft = cv2.dft(np.float32(image), flags = cv2.DFT_COMPLEX_OUTPUT)
		fftShift = np.fft.fftshift(dft)
		mag, phase = cv2.cartToPolar(fftShift[:,:,0], fftShift[:,:,1])
		mag_norm = mag / 180
		#plt.imshow(20*np.log(mag),cmap = 'gray')
		#plt.show()
		return mag_norm,phase

	def getIFFTTransform(self,mag,phase,t):
		#plt.imshow(20*np.log(mag*(t)),cmap = 'gray')
		#plt.show()
		r_factor = 5
		real, imag = cv2.polarToCart(mag*(180 - r_factor), phase)
		back = cv2.merge([real, imag])
		back_ishift = np.fft.ifftshift(back)
		img_back = cv2.idft(back_ishift,flags=cv2.DFT_SCALE)
		img_back = cv2.magnitude(img_back[:,:,0], img_back[:,:,1])
		return img_back
		

	def showImage(self,*image_args):
		for image in image_args:
			cv2.imshow('image',image)
			cv2.waitKey(0)
		cv2.waitKey(0)
		return

	def sortCells(self,mc,nonm,sip_cells):
		cell_list = []
		k = 0
		f = 0
		for i in range(len(sip_cells)):
			for j in range(len(sip_cells)):
				if(k < len(sip_cells) and sip_cells[k][0] == i and sip_cells[k][1] == j):
					cell_list.append(mc[k])
					k += 1
				else:
					cell_list.append(nonm[f])
					f += 1
		return cell_list

	def findOptimalIntensity(self,image):
		ret,th = cv2.threshold(image,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
		print(ret)
		return ret

	def getWatermarkedImage(self,im,sip,SIZE,name):
		img = self.openImage(im)

		w,h = img.size

		outim_w = math.floor((w / SIZE))
		outim_h = math.floor((h / SIZE))

		new_w = outim_w * SIZE
		new_h = outim_h * SIZE

		#new_img = img.resize((new_w,new_h))
		#new_img.save(name + ".jpg")
		#img1 = self.openImage(name + ".jpg")

		r,g,b = img.split()


		th1 = self.findOptimalIntensity(np.array(r))
		#th2 = self.findOptimalIntensity(np.array(g))
		#th3 = self.findOptimalIntensity(np.array(b))

		r_img = self.embedPermutationToChannel(r,sip,SIZE,th1)
		g_img = self.embedPermutationToChannel(g,sip,SIZE,th1)
		b_img = self.embedPermutationToChannel(b,sip,SIZE,th1)

		red = Image.fromarray(r_img)
		green = Image.fromarray(g_img)
		blue = Image.fromarray(b_img)

		rgb = Image.merge('RGB', (red,green,blue))
		# If image after embeding has different size here we resize it to original
		#rgb = cv2.resize(rgb, None, interpolation = cv2.INTER_AREA)
		#rgb.thumbnail(size)
		rgb.save("watermarked_" + name + ".jpg")
		return

	def mergeCellsToImage(self,m,unm,w,h,sip_cells):
		sorted_cells = self.sortCells(m,unm,sip_cells)
		N = len(sip_cells)
		display = np.empty(((w-1)*N, (h-1)*N), dtype=np.uint8)

		for i, j in it.product(range(N), range(N)):
			arr = sorted_cells[i*N+j]
			
			x,y = i*(w-1), j*(h-1)
			display[x : x + (w-1), y : y + (h-1)] = arr
				
		
		return display

	def modifyMagnitude(self,mag_marked,mag_rest,D_array,sip_cells,gw,gh,totsu):
		modified_cells = []
		unmodified_cells = []

		for i in range(len(mag_rest)):

			MAGNITUDE = mag_rest[i][0]
			PHASE = mag_rest[i][1]
			original_cell = self.getIFFTTransform(MAGNITUDE,PHASE,totsu)
			unmodified_cells.append(original_cell)
			#print("rest ",(mag_rest[i][5] - mag_rest[i][4]))

		for i in range(len(mag_marked)):

			MAGNITUDE = mag_marked[i][0]
			PHASE = mag_marked[i][1]
			RED_AN = mag_marked[i][2]
			BLUE_AN = mag_marked[i][3]
			AVG_R = mag_marked[i][4]
			AVG_B = mag_marked[i][5]
			COORD_R = mag_marked[i][6]
			COORD_B = mag_marked[i][7]
			a = np.amax(MAGNITUDE)
			#print(AVG_R,AVG_B,D_array[i])
			#plt.imshow(MAGNITUDE,cmap = 'gray')
			#plt.show()
			#print(COORD_R)
			for j in range(gw):
				for k in range(gh):
					for t in range(len(COORD_R)):
						if(j == COORD_R[t][0] and k == COORD_R[t][1]):
							#print("mag ",MAGNITUDE[j,k])
							val = (AVG_B - AVG_R) + (D_array[i] + 3.0)
							MAGNITUDE[j,k] += val# change magnitude of red region cells
					'''
					for t in range(len(COORD_B)):
						if(j == COORD_B[t][0] and k == COORD_B[t][1]):
							#print(COORD_R[t][0],COORD_R[t][1])
							val = (AVG_B - AVG_R) + (D_array[i] + 340)
							MAGNITUDE[j,k] =  a#val# change magnitude of red region cells
					'''
			#plt.imshow(MAGNITUDE,cmap = 'gray')
			#plt.show()
			#print(COORD_R)
			original_cell = self.getIFFTTransform(MAGNITUDE,PHASE,totsu)
			modified_cells.append(original_cell)
			#print("MOD ",(AVG_B - AVG_R))
		return modified_cells,unmodified_cells

	def embedPermutationToChannel(self,channel,sip,SIZE,t):
		grid_cell_num = 0
		sip_cells = []
		print(t)

		# STEP 1: FIND 2D REPRESANTAION OF SIP

		A_matrix = []
		for i in range(0,len(sip)):
			row = []
			for j in range(0,SIZE):
				if(j == sip[i] - 1):
					row.append("*")
					sip_cells.append((i,j))
				else:
					row.append("-")
			A_matrix.append(row)


		# STEP 2: COMPUTE IMAGE SIZE

		N,M = channel.size
		channel_array = np.array(channel)
		#print(channel_array.shape)
		#channel_array = cv2.resize(channel_array,(200,200))

		# GET THE SIZE OF EACH GRID SHELL

		grid_size_w = math.floor((N / SIZE))
		grid_size_h = math.floor((M / SIZE))

		# FOR EACH GRID CELL COMPUTE FFT MAGNITUDE AND PHASE:
		# ALSO COMPUTE IMAGINARY RED AND BLUE ANULUS RADIOUSES:

		RED_WIDTH = 2
		BLUE_WIDTH = 2

		RED_RADIOUS_X = math.floor((N / (2 * SIZE)))
		RED_RADIOUS_Y = math.floor((M / (2 * SIZE)))

		BLUE_RADIOUS_X = (RED_RADIOUS_X - RED_WIDTH)
		BLUE_RADIOUS_Y = (RED_RADIOUS_Y - RED_WIDTH)

		MaxDRows = []
		MaxD = []
		avgR  = []
		avgB = []
		avg = []
		x = 0
		y = 0
		i = 0
		c = 0
		mag_red_blue = []
		mag_rest = []
		l = 0
		k = 0
		if(N % grid_size_w == 0):
			l = N
			k = M
		else:
			l = N - grid_size_w
			k = M - grid_size_h
		for r in range(0,l, grid_size_w):
			for c in range(0,k, grid_size_h):
				grid_cell_num += 1
				AVG_RED = 0
				AVG_BLUE = 0
				mag_sum_red = 0
				mag_sum_blue = 0
				D = 0
				c +=1

				grid_cell = channel_array[r:r + grid_size_w-1,c:c + grid_size_h-1]
				#print(grid_cell.shape)
				#print(channel_array[r:r + grid_size_w,c:c + grid_size_h].shape)
				#np.reshape(grid_cell,(40,40))
				#print(grid_cell.shape)
				#print(r,c)
				mag,phase = self.getFFTTransform(grid_cell,t)
				#print(mag.shape)
	
				cx = int(grid_cell.shape[0] / 2)
				cy = int(grid_cell.shape[1] / 2)

			
				red,coord_red = createEllipticDisk(mag,RED_RADIOUS_X,RED_RADIOUS_Y,RED_WIDTH,cx,cy,grid_size_w-1,grid_size_h-1)
				blue,coord_blue = createEllipticDisk(mag,BLUE_RADIOUS_X,BLUE_RADIOUS_Y,BLUE_WIDTH,cx,cy,grid_size_w-1,grid_size_h-1)
				

				AVG_RED = sum(red) / len(red)
				AVG_BLUE = sum(blue) / len(blue)
				avg.append(AVG_RED)

				if(AVG_BLUE <= AVG_RED):
					D = abs(AVG_BLUE - AVG_RED)
				else:
					D = 0

				MaxD.append(D)

				if(i < len(sip_cells) and sip_cells[i][0] == x and sip_cells[i][1] == y): # for every marked sip cell take the magnitude,red,blue
					mag_red_blue.append((mag,phase,red,blue,AVG_RED,AVG_BLUE,coord_red,coord_blue))
					i += 1
				else:
					mag_rest.append((mag,phase,red,blue,AVG_RED,AVG_BLUE,coord_red,coord_blue))

				y += 1
			MaxDRows.append(max(MaxD))
			del MaxD[:]
			x += 1
			y = 0
		m,unm = self.modifyMagnitude(mag_red_blue,mag_rest,MaxDRows,sip_cells,grid_size_w,grid_size_h,t)
		img = self.mergeCellsToImage(m,unm,grid_size_w,grid_size_h,sip_cells)

		return img

