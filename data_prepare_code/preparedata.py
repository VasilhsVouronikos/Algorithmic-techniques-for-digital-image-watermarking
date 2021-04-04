import sys
import os
import cv2

PARENT_DIR = "D:\\BSc-Watermarking\\KEY-DFT-code\\dataset\\archive\\wm-nowm\\valid\\no-watermark"
IMAGE_F1 = "D:\\BSc-Watermarking\\KEY-DFT-code\\images_for_test\\200 x 200"
IMAGE_F2 = "D:\\BSc-Watermarking\\KEY-DFT-code\\images_for_test\\500 x 500"
IMAGE_F3 = "D:\\BSc-Watermarking\\KEY-DFT-code\\images_for_test\\512 x 512"
IMAGE_F4 = "D:\\BSc-Watermarking\\KEY-DFT-code\\images_for_test\\768 x 768"
IMAGE_F5 = "D:\\BSc-Watermarking\\KEY-DFT-code\\images_for_test\\800 x 800"
IMAGE_F6 = "D:\\BSc-Watermarking\\KEY-DFT-code\\images_for_test\\1024 x 1024"


def main():
	COUNTER = 0
	#os.chdir("D:")
	#os.chdir(PARENT_DIR)
	for img in os.listdir(PARENT_DIR):
		im = cv2.imread(os.path.join(PARENT_DIR,img))
		#print(im.shape[1])
		if(im.shape[1] >= 200 and im.shape[1] < 300):
			new_im = cv2.resize(im,(200,200))
			cv2.imwrite(IMAGE_F1 + "\\image_" + str(COUNTER) + ".jpg", new_im)
			COUNTER += 1
		if(im.shape[1] >= 400 and im.shape[1] < 500):
			new_im = cv2.resize(im,(500,500))
			cv2.imwrite(IMAGE_F2 + "\\image_" + str(COUNTER) + ".jpg", new_im)
			COUNTER += 1
		if(im.shape[1] >= 500 and im.shape[1] < 600):
			new_im = cv2.resize(im,(512,512))
			cv2.imwrite(IMAGE_F3 + "\\image_" + str(COUNTER) + ".jpg", new_im)
			COUNTER += 1
		if(im.shape[1] >= 600 and im.shape[1] < 700):
			new_im = cv2.resize(im,(768,768))
			cv2.imwrite(IMAGE_F4 + "\\image_" + str(COUNTER) + ".jpg", new_im)
			COUNTER += 1
		if(im.shape[1] >= 700 and im.shape[1] < 800):
			new_im = cv2.resize(im,(800,800))
			cv2.imwrite(IMAGE_F5 + "\\image_" + str(COUNTER) + ".jpg", new_im)
			COUNTER += 1
		if(im.shape[1] >= 800 and im.shape[1] < 1000):
			new_im = cv2.resize(im,(1024,1024))
			cv2.imwrite(IMAGE_F6 + "\\image_" + str(COUNTER) + ".jpg", new_im)
			COUNTER += 1

if __name__ == '__main__':
	main()