import os
import matplotlib.pyplot as plt
import sys


def visualize_psnr(psnr_values1,psnr_values2,images,title):
	fig, ax = plt.subplots()
	plt.bar(range(len(psnr_values1)),height = psnr_values1,label = "key_method",bottom = psnr_values1,width = 0.5,align='center')
	plt.bar(range(len(psnr_values2)),height = psnr_values2,label = "logo_method",width = 0.5, align='center')
	plt.xticks(range(len(images)), images, size='small')
	plt.title("PSNR in filter = " + title +  "\nNote: y-axis bar height is the addition of 2 psnr values")
	plt.xlabel("image")
	plt.ylabel("PSNR")
	plt.legend()
	'''
	for index, value in enumerate(psnr_values2):
		plt.text(index,value, str(value),ha='center', va='bottom')
	for index, value in enumerate(psnr_values1):
		plt.text(index,value, str(value),ha='center', va='top')
	'''
	y_offset = -10
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


def visualize_ssim(ssim_values,images):
	return


if __name__ == '__main__':
	psnr_values1 = [18.91,22.15,17.71,19.26,26.15]
	psnr_values2 = [18.89,22.10,17.64,19.31,26.18]
	images = ["w_painting","w_sky","w_winter","w_temple","w_scenary"]
	visualize_psnr(psnr_values1,psnr_values2,images,sys.argv[1])
	#visualize_psnr(psnr_values2,images)
