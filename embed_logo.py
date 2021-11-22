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
import math

global secret_pg,secret_pb
#pairsg = [((2,0),(3,0)),((2,1),(3,1)),((2,2),(3,2)),((2,5),(2,6)),((2,7),(3,0)),((3,1),(3,2)),((3,3),(3,4)) # mid bands
    #,((3,5),(3,6)),((3,7),(4,0)),((4,1),(4,2)),((4,3),(4,4))]
#pairsg = [((1, 4), (2, 3)), ((3, 2), (4, 1)), ((5, 0), (6, 0)), ((5, 1), (4, 2)), ((3, 3), (2, 4)), ((1, 5), (0, 6)), ((0, 7), (1, 6)), ((2, 5), (3, 4)), 
#((4, 3), (5, 2)), ((6, 1), (7, 0)), ((7, 1), (6, 2))] # mid bands
pairsg = [((1, 4), (2, 3)), ((3, 2), (4, 1)), ((5, 0), (6, 0)), ((5, 1), (4, 2)), ((3, 3), (2, 4)), ((1, 5), (0, 6)), ((0, 7), (1, 6)), ((2, 5), (3, 4)), 
                                ((4, 3), (5, 2)), ((6, 1), (7, 0)), ((7, 1), (6, 2))]
#,((4,1),(4,2)),((4,3),(4,4))]
def binarizeLogo(path):
    l = np.array(openImage(path,'default'))
    ret,th = cv2.threshold(l,170,255,cv2.THRESH_BINARY)
    return th

def arnold(img):
    r, c  = img.shape
    p = np.zeros((r, c), np.uint8)
    a = 1
    b = 1
    for i in range(r):
        for j in range(c):
            x = (i + b * j) % r
            y = (a * i + (a * b + 1) * j) % c
            p[x, y] = img[i, j]
    return p
    
def mergeCellsToImage(blocks,w,h,win_size):
        display = np.empty((win_size, win_size), dtype=np.uint8)
        N = int(win_size / 8)
        for i, j in it.product(range(N), range(N)):
            arr = blocks[i*N+j]
            x,y = i*8, j*8
            display[x : x + 8, y : y + 8] = arr
                
        return display

def openImage(im_path,mode):
    if(mode != None):
        im1 = Image.open(im_path)
        img = ImageOps.grayscale(im1)
    else:
        img = Image.open(im_path)
    return img

def applyIDCT(array):
    idc = idct(idct(array.T, norm='ortho').T, norm='ortho')
    return idc
    
def applyDCT(cell):
    #img1 = cell.astype('float')
    dc = dct(dct(cell.T, norm='ortho').T, norm='ortho')     
    return dc


def splitImagechannels(im):
    r,g,b = im.split()
    return g,b,r

def embed(path,win_size,logo1,logo2,rep_code):
    
    secret_pairs_g = []
    secret_pairs_b = []
    arr = np.zeros([8,8])

    secret_pg = []
    secret_pb = []
    green_blocks = []
    blue_blocks = []
    bin_l1 = binarizeLogo(logo1)
    bin_l2 = binarizeLogo(logo2)
    
    arn1 = arnold(bin_l1)
    arn2 = arnold(bin_l2)

    #plt.imshow(bin_l1,cmap = 'gray')
    #plt.show()

    im = openImage(path,None)
    g_channel, b_channel,r_channel = splitImagechannels(im)


    r_channel = np.array(r_channel)

    g_channel_array = np.array(g_channel)
    b_channel_array = np.array(b_channel)

    N,M = g_channel.size
    g_w = math.floor(N / 8)
    g_h = math.floor(M / 8)
    
    k = 0
    l = 0
    step = 0
    arn1_1_bit = []
    arn1_0_bit = []

    arn2_1_bit = []
    arn2_0_bit = []

    if(win_size == 8):
        step = win_size
    else:
        step = win_size * 2


    for r in range(0,N, win_size):
        for c in range(0,M, win_size):
            #print(r,c

            random_pairs_arn1 = []
            random_pairs_arn2 = []

            g_grid_cell = g_channel_array[r:r + win_size,c:c + win_size]
            b_grid_cell = b_channel_array[r:r + win_size,c:c + win_size]
            #print(g_grid_cell.shape)
            if(k < 64 and l < 64):
                g_dct_cell = applyDCT(g_grid_cell) 
                b_dct_cell = applyDCT(b_grid_cell) 
                
                reorderedg = zigzag(g_dct_cell)
                reorderedb = zigzag(b_dct_cell)

                reshapedg = np.reshape(reorderedg, (8, 8))

                reshapedb = np.reshape(reorderedb, (8, 8))
                if(arn1[k,l] == 255):
                    t1times = rep_code[0] * 1
                    binary = bin(t1times)[2:]
                    arn1_1_bit.append((str(binary)))
                    for i in range(rep_code[0]):
                        pair = pairsg[i]
                        
                        a = pair[0]
                        b = pair[1]

                        n = a[0]
                        m = a[1]

                        h = b[0]
                        u = b[1]
                        d = reshapedg[n,m] - reshapedg[h,u]
                        
                        if(reshapedg[n,m] <= reshapedg[h,u]):
                            reshapedg[n,m],reshapedg[h,u] = reshapedg[h,u],reshapedg[n,m]
                        else:
                            reshapedg[n,m],reshapedg[h,u] = reshapedg[n,m],reshapedg[h,u]

                    invzigzag = inverse_zigzag(reshapedg.flatten(),8,8)
                    idctg = applyIDCT(invzigzag) 
                    green_blocks.append(idctg)
                else:
                    t1times = rep_code[0] * str(0)
                    arn1_0_bit.append((t1times))
                    for i in range(rep_code[0]):
                        pair = pairsg[i]

                        a = pair[0]
                        b = pair[1]

                        n = a[0]
                        m = a[1]

                        h = b[0]
                        u = b[1]
                        d = reshapedg[n,m] - reshapedg[h,u]
                        if(reshapedg[n,m] > reshapedg[h,u]):
                            reshapedg[n,m],reshapedg[h,u] = reshapedg[h,u],reshapedg[n,m]
                        else:
                            reshapedg[n,m],reshapedg[h,u] = reshapedg[n,m],reshapedg[h,u]
                    invzigzag = inverse_zigzag(reshapedg.flatten(),8,8)
                    idctg = applyIDCT(invzigzag)
                    green_blocks.append(idctg)
                
                if(arn2[k,l] == 255):
                    t1times = rep_code[0] * 255
                    binary = bin(t1times)[2:]
                    arn2_1_bit.append((str(binary)))
                    for i in range(rep_code[0]):
                        pair = pairsg[i]
                        
                        a = pair[0]
                        b = pair[1]

                        n = a[0]
                        m = a[1]

                        h = b[0]
                        u = b[1]

                        if(reshapedb[n,m] <= reshapedb[h,u]):
                            reshapedb[n,m],reshapedb[h,u] = reshapedb[h,u],reshapedb[n,m]
                        else:
                            reshapedb[n,m],reshapedb[h,u] = reshapedb[n,m],reshapedb[h,u]

                    invzigzag = inverse_zigzag(reshapedb.flatten(),8,8)      
                    idctb = applyIDCT(invzigzag)
                    blue_blocks.append(idctb)
                else:
                    t1times = rep_code[0] * str(0)
                    arn2_0_bit.append((t1times))
                    for i in range(rep_code[0]):
                        pair = pairsg[i]
                       
                        a = pair[0]
                        b = pair[1]

                        n = a[0]
                        m = a[1]

                        h = b[0]
                        u = b[1]
                       
                        if(reshapedb[n,m] > reshapedb[h,u]):
                            reshapedb[n,m],reshapedb[h,u] = reshapedb[h,u],reshapedb[n,m]
                        else:
                            reshapedb[n,m],reshapedb[h,u] = reshapedb[n,m],reshapedb[h,u]

                    invzigzag = inverse_zigzag(reshapedb.flatten(),8,8)       
                    idctb = applyIDCT(invzigzag)
                    blue_blocks.append(idctb)
            else:
                green_blocks.append(g_grid_cell)
                blue_blocks.append(b_grid_cell)
            l += 1
        k += 1
        l = 0

    dis1 = mergeCellsToImage(blue_blocks,g_w,g_h,N)
    dis2 = mergeCellsToImage(green_blocks,g_w,g_h,N)
    
    red = Image.fromarray(r_channel)
    green = Image.fromarray(dis2)
    blue = Image.fromarray(dis1)
    path = "watermarked_logo_" + path
    rgb = Image.merge('RGB', (red,green,blue))
    rgb.save(path,quality= 100,subsampling=0)
    
    return path
    


    