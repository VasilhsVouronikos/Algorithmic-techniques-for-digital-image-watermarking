import os
import sys
from PIL import Image,ImageOps
import numpy as np
import cv2
import matplotlib.pyplot as plt
from infinite import product
from itertools import count
import random
import itertools as it
import matplotlib.pyplot as plt
from zigzag import*
from scipy.fftpack import dct,idct

def dearnold(img):
    r, c = img.shape
    p = np.zeros((r, c), np.uint8)
    a = 1
    b = 1
    for i in range(r):
        for j in range(c):
            x = ((a * b + 1) * i - b * j) % r
            y = (-a * i + j) % c
            p[x, y] = img[i, j]
    return p


def openImage(im_path,mode):
    if(mode != None):
        im1 = Image.open(im_path)
        img = ImageOps.grayscale(im1)
    else:
        img = Image.open(im_path)
    return img
    
def applyDCT(cell):
    dc = dct(dct(cell.T, norm='ortho').T, norm='ortho')     
    return dc


def splitImagechannels(im):
    r,g,b = im.split()
    return g,b,r


def extractLogoFromImage(path,win_size,secret_pairs,rep_code):
    global secret_pg,secret_pb
    im = Image.open(path)
    gchannel,bchannel,rchannel = splitImagechannels(im)
    #print(path.filename)

    garray = np.array(gchannel)
    barray = np.array(bchannel)
    rarray = np.array(rchannel)

    list_logo1 = []
    list_logo2 = []

    N,M = gchannel.size
    

    k = 0
    l = 0
    for r in range(0,N,win_size):
        for c in range(0,M,win_size):
            if(k < 64 and l < 64):
                logo1_bit_stream = []
                logo2_bit_stream = []

                g_grid_cell = garray[r:r + win_size,c:c + win_size]
                b_grid_cell = barray[r:r + win_size,c:c + win_size]
                

                g_dct_cell = applyDCT(g_grid_cell)
                b_dct_cell = applyDCT(b_grid_cell)

                reorderedg = zigzag(g_dct_cell)
                reorderedb = zigzag(b_dct_cell)

                reshapedg = np.reshape(reorderedg, (8, 8))
               
                reshapedb = np.reshape(reorderedb, (8, 8))

                
                for h in range(rep_code[0]):
                    x1 = secret_pairs[h][0][0]
                    y1 = secret_pairs[h][0][1]
                    x2 = secret_pairs[h][1][0]
                    y2 = secret_pairs[h][1][1]
                    if(reshapedg[x1,y1] >= reshapedg[x2,y2]):
                        logo1_bit_stream.append(1)
                    else:
                        logo1_bit_stream.append(0)
                
                for h in range(rep_code[0]):
                    x1 = secret_pairs[h][0][0]
                    y1 = secret_pairs[h][0][1]
                    x2 = secret_pairs[h][1][0]
                    y2 = secret_pairs[h][1][1]
                    if(reshapedb[x1,y1] >= reshapedb[x2,y2]):
                        logo2_bit_stream.append(1)
                    else:
                        logo2_bit_stream.append(0)

                if(logo1_bit_stream.count(1) > logo1_bit_stream.count(0)):
                    list_logo1.append(255)
                else:
                    list_logo1.append(0)

                if(logo2_bit_stream.count(1) > logo2_bit_stream.count(0)):
                    list_logo2.append(255)
                else:
                    list_logo2.append(0)
            else:
                continue
            l += 1
        k += 1
        l = 0  
           
        
    l1 = np.array(list_logo1).reshape(-1, 64)
    l2 = np.array(list_logo2).reshape(-1, 64)
    original1 = dearnold(l1)
    original2 = dearnold(l2)
    plt.imshow(original1,cmap = 'gray')
    plt.title("logo1")
    plt.show()
    plt.imshow(original2,cmap = 'gray')
    plt.title("logo2")
    plt.show()