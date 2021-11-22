import os
import matplotlib.pyplot as plt
import sys
import numpy as np

def side_bar_chart(list1,list2,title,images,ylabel):
	w = 0.2
	fig, ax = plt.subplots()
	bar1 = np.arange(len(images))
	bar2 = [i+w for i in bar1]

	plt.bar(bar1,list1,w,label = "Sip")
	plt.bar(bar2,list2,w,label = "Logo")
	plt.xticks(range(len(images)), images, size='small')
	plt.xlabel("Q")
	plt.ylabel(ylabel)

	if(sys.argv[4] == 'C'):
		A = "\n BER in B channel"
		plt.title(ylabel +" in attack = " + title + A)
	else:
		plt.title(ylabel +" in attack = " + title)

	y_offset = - float(sys.argv[3])
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


def visualize_line(values1,values2,values3,im):
	plt.plot(values1,values2,label = "Sip")
	plt.plot(values1,values3,label = "Logo")
	plt.xticks(range(len(values1)), images, size='small')
	plt.xlabel("Crop attacks")
	plt.ylabel("Quality")
	plt.title("Comparison of crop outputs in image = " + im + "\n" + "considering quality of logos and Sip")
	plt.legend()
	plt.show()




if __name__ == '__main__':
	psnr_values1 = [1.0,1.0]
	psnr_values2 = [0.81,0.88]
	#psnr_values1 = [0.98,0.99,0.99,0.99,0.99]
	#psnr_values2 = [0.98,0.99,0.99,0.99,0.99]
	images = ["w_sky","w_winter"]
	#visualize_psnr(psnr_values1,psnr_values2,images,sys.argv[1])
	
	side_bar_chart(psnr_values1,psnr_values2,sys.argv[1],images,sys.argv[2])
	'''
	im = "temple.jpg"
	attacks = ["128_cols","128_rows","256x256_white","256x256_black","350x350_white","350x350_black"]
	logo = ["acceptable","acceptable","acceptable","acceptable","bad","bad"]
	sip = ["acceptable","acceptable","very good","very good","very good","very good"]

	'''
	#visualize_line(attacks,sip,logo,im)
	#visualize_psnr(psnr_values2,images)
