from SSIM_PIL import compare_ssim
import sys
from PIL import Image

def ssim(img1,img2):
	image1 = Image.open(img1)
	image2 = Image.open(img2)
	value = compare_ssim(image1, image2)
	print(value)

if __name__ == '__main__':
	ssim(sys.argv[1],sys.argv[2])