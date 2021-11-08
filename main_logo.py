import os
import sys
from embed_logo import embed
from extract_logo import extractLogoFromImage

INPUT_IMAGE = sys.argv[1]
LOGO_1 = "logo11.png"
LOGO_2 = "logo12.png"
WINDOW_SIZE = 8
REPC = (11,1)
SECRET_PAIRS = [((1, 4), (2, 3)), ((3, 2), (4, 1)), ((5, 0), (6, 0)), ((5, 1), (4, 2)), ((3, 3), (2, 4)), ((1, 5), (0, 6)), ((0, 7), (1, 6)), ((2, 5), (3, 4)), 
((4, 3), (5, 2)), ((6, 1), (7, 0)), ((7, 1), (6, 2))] # secret pairs


def main():
	#im = embed(INPUT_IMAGE,WINDOW_SIZE,LOGO_1,LOGO_2,REPC)
	#path = "watermarked_lena.jpg"
	extractLogoFromImage(INPUT_IMAGE,WINDOW_SIZE,SECRET_PAIRS,REPC)
	return


if __name__ == "__main__":
    main()