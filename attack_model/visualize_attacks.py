import os
import matplotlib.pyplot as plt
import sys
import numpy as np


def visualize_psnr(psnr_values1,psnr_values2,images,title):
	fig, ax = plt.subplots()
	plt.bar(range(len(psnr_values1)),height = psnr_values1,label = "key_method",bottom = psnr_values1,width = 0.5,align='center')
	plt.bar(range(len(psnr_values2)),height = psnr_values2,label = "logo_method",width = 0.5, align='center')
	plt.xticks(range(len(images)), images, size='small')
	plt.title("SSIM in filter = " + title +  "\nNote: y-axis bar height is the addition of 2 psnr values")
	plt.xlabel("image")
	plt.ylabel("PSNR")
	plt.legend()
	
	y_offset = -25
	for bar in ax.patches:
	  ax.text(
      bar.get_x() + bar.get_width() / 2,
      bar.get_height() + bar.get_y() + y_offset,
      round(bar.get_height(),2),
      ha='center',
      color='w',
      weight='bold',
      size=8
  	)

	plt.show()
	return

def side_bar_chart(list1,list2,title,images,ylabel):
	w = 0.4
	fig, ax = plt.subplots()
	bar1 = np.arange(len(images))
	bar2 = [i+w for i in bar1]

	plt.bar(bar1,list1,w,label = "Sip")
	plt.bar(bar2,list2,w,label = "Logo")
	plt.xticks(range(len(images)), images, size='small')
	plt.xlabel("Q")
	plt.ylabel(ylabel)

	plt.title(ylabel +" in jpeg " + title)

	y_offset = -0.09
	for bar in ax.patches:
	  ax.text(
      bar.get_x() + bar.get_width() / 2,
      bar.get_height() + bar.get_y() + y_offset,
      round(bar.get_height(),2),
      ha='center',
      color='w',
      weight='bold',
      size=8
  	)

	plt.legend()
	plt.show()




if __name__ == '__main__':
	psnr_values1 = [0.97,0.96,0.95,0.94]
	psnr_values2 = [0.92,0.91,0.90,0.89]
	#psnr_values1 = [0.98,0.99,0.99,0.99,0.99]
	#psnr_values2 = [0.98,0.99,0.99,0.99,0.99]
	images = ["Q=80","Q=70","Q=60","Q=50"]
	#visualize_psnr(psnr_values1,psnr_values2,images,sys.argv[1])
	side_bar_chart(psnr_values1,psnr_values2,sys.argv[1],images,sys.argv[2])
	#visualize_psnr(psnr_values2,images)
