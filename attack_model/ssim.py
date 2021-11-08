from SSIM_PIL import compare_ssim
import sys
from PIL import Image
from skimage.metrics import structural_similarity as ssim
import numpy as np

def ssim_metric(img1,img2):
	image1 = Image.open(img1)
	image2 = Image.open(img2)
	image1 = np.array(image1)
	image2 = np.array(image2)
	value = ssim(image1, image2, data_range=image2.max() - image2.min(),multichannel=True)
	return value

if __name__ == '__main__':
	val = ssim_metric(sys.argv[1],sys.argv[2])
	print(val)