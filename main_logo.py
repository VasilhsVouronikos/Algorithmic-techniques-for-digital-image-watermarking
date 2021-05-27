import os
import sys
from embed_logo import embed
from extract_logo import extractLogoFromImage

INPUT_IMAGE = sys.argv[1]
LOGO_1 = sys.argv[2]
LOGO_2 = sys.argv[3]
WINDOW_SIZE = 8
REPC = (3,1)
SECRET_PAIRS = [((3,7),(4,0)),((4,1),(4,2)),((4,3),(4,4))] # secret pairs


def main():
	im = embed(INPUT_IMAGE,WINDOW_SIZE,LOGO_1,LOGO_2,REPC)
	#path = "watermarked_lena.jpg"
	extractLogoFromImage(im,WINDOW_SIZE,SECRET_PAIRS,REPC)
	return


if __name__ == "__main__":
    main()