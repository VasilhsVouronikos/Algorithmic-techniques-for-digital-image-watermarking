import os,sys
import re
import ast
from collections import Counter
from recossip import recsip
import math
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt



ATTACK = sys.argv[1]
IMAGE = sys.argv[2]
IMAGE_NAME = re.split(r'\.(?!\d)', IMAGE)[0]
ARGS = sys.argv[3]
MODEL = sys.argv[4]


def get_current_path():
	path = os.getcwd().split("\\")
	path.pop(0)
	path.pop(len(path)-1)
	new_path = "\\"+"\\".join(path)
	
	return new_path

path_to_extract = get_current_path()

sys.path.insert(0,path_to_extract)

from extract_sip import ExtractPermutation
from embed_key import EmbedPermutation
from encodeinteger import encodeInteger
from decodesip import decodeSip
from attackimage import attackModel
from embed_logo import embed
from extract_logo import extractLogoFromImage

def initModel(m):
	if(m == 'key'):
		model = attackModel()
		w = EmbedPermutation()
		ex = ExtractPermutation()
		return model,w,ex
	else:
		model = attackModel()
		return model

# Recostruct SIP when an image is cropped
# or compressed
# based on SIP properties

def recostructSip(sip,s1,s2,s3,mode):
	if(mode == 'crop' or 'jpeg' or 'scale' or 'filter'):
		if(s1 != sip or s2 != sip or s3 != sip):
			new_sip1 = recsip(s1,sip,5)
			new_sip2 = recsip(s2,sip,5)
			new_sip3 = recsip(s3,sip,5)
			if(new_sip1 == sip):
				print("fixed sip: ",new_sip1)
			elif(new_sip2 == sip):
				print("fixed sip: ",new_sip2)
			elif(new_sip3 == sip):
				print("fixed sip: ",new_sip3)
		else:
			print("sip : ",sip,"\n","s1 : ",s1,"\n","s2 : ",s2,"\n","s3 : ",s3)
	else:
		print("sip : ",sip,"\n","s1 : ",s1,"\n","s2 : ",s2,"\n","s3 : ",s3)

# Detect rotation based on the diagonal
# properties of SIP
# Succesfuly detects 180 degrees rotation 
# Succesfuly detects 90 degrees rotation 

def detectSipRotation(sip_estimation):
	c = 0
	valid = math.ceil(len(sip_estimation)) / 2
	for i in range(len(sip_estimation)):
		if(sip_estimation[i] == i + 1):
			if(i + 1 < valid):
				print("180 degrees rotation detected")
				break
		else:
			c += 1
	if(c == len(sip_estimation)):
		print("90 degrees rotation detected")

def testAttack():
	if(MODEL == 'key'):
		KEY = int(sys.argv[5])
		COPT = float(sys.argv[6])
		attack_model,embed_model,extract_model = initModel(MODEL)
		sip = encodeInteger(KEY)
		size = len(sip)
		#args = ast.literal_eval(ARGS)
		if(ATTACK == 'crop'):
			# we dont want to embed when image is edited
			# just test if watermark can be extracted
			embed_model.getWatermarkedImage(IMAGE,sip,size,IMAGE_NAME,COPT,2,2)
			path = attack_model.attackImage("watermarked_"+IMAGE_NAME+".jpg",ATTACK,args,KEY,COPT,MODEL)
			s1,s2,s3 = extract_model.getSip(path,size,2,2)
			recostructSip(sip,s1,s2,s3,ATTACK)
		elif(ATTACK == 'rotate'):
			embed_model.getWatermarkedImage(IMAGE,sip,size,IMAGE_NAME,COPT,2,2)
			path = attack_model.attackImage("watermarked_"+IMAGE_NAME+".jpg",ATTACK,args,KEY,COPT,MODEL)
			s1,s2,s3 = extract_model.getSip(path,size,2,2)
			detectSipRotation(s1)
			detectSipRotation(s2)
			detectSipRotation(s3)
			if(args[0] == 0):
				print("sip : ",sip,"\n","s1 : ",s1,"\n","s2 : ",s2,"\n","s3 : ",s3)
		elif(ATTACK == 'scale'):
			PR = 2
			PB = 2
			embed_model.getWatermarkedImage(IMAGE,sip,size,IMAGE_NAME,COPT,PR,PB)
			path = attack_model.attackImage("watermarked_"+IMAGE_NAME+".jpg",ATTACK,args,KEY,COPT,MODEL)
			s1,s2,s3 = extract_model.getSip(path,size,1,1)
			print("sip : ",sip,"\n","s1 : ",s1,"\n","s2 : ",s2,"\n","s3 : ",s3)
			recostructSip(sip,s1,s2,s3,ATTACK)
		else:
			embed_model.getWatermarkedImage(IMAGE,sip,size,IMAGE_NAME,COPT,2,2)
			path = attack_model.attackImage("watermarked_"+IMAGE_NAME+".jpg",ATTACK,["noise",(0,0.01)],KEY,COPT,MODEL)
			s1,s2,s3 = extract_model.getSip(path,size,2,2)
			print(s1,s2,s3)
			recostructSip(sip,s1,s2,s3,ATTACK)
	elif(MODEL == 'logo'):
		if(ATTACK == 'crop'):
			attack_model = initModel(MODEL)
			LOGO_1 = sys.argv[5]
			LOGO_2 = sys.argv[6]
			rep = (7,1)
			KEY = "no key"
			COPT = "no c"
			SECRET_PAIRS = [((4, 3),
				(5, 2)),((6, 1),(7, 0)),((7, 1), (6, 2)),((5, 0), (6, 0)), ((5, 1), (4, 2)),((3,3),(3,4)),((3, 2),(4, 1))]
			# STUPID SYNTAX CAN EASILY BE FORGOTTEN
			# DONT BE LIKE THAT WRITE CLEAN CODE
			im = embed(IMAGE,8,LOGO_1,LOGO_2,rep)
			path = attack_model.attackImage(im,ATTACK,args,KEY,COPT,MODEL)
			extractLogoFromImage(path,8,SECRET_PAIRS,rep)
		else:

			attack_model = initModel(MODEL)
			#args = ast.literal_eval(ARGS)
			LOGO_1 = sys.argv[5]
			LOGO_2 = sys.argv[6]
			#rep = (3,1)
			#rep = (5,1)
			rep = (11,1)
			KEY = "no key"
			COPT = "no c"
			SECRET_PAIRS = [((1, 4), (2, 3)), ((3, 2), (4, 1)), ((5, 0), (6, 0)), ((5, 1), (4, 2)), ((3, 3), (2, 4)), ((1, 5), (0, 6)), ((0, 7), (1, 6)), ((2, 5), (3, 4)), 
								((4, 3), (5, 2)), ((6, 1), (7, 0)), ((7, 1), (6, 2))]
			#SECRET_PAIRS = [((4, 3),
				#(5, 2)),((6, 1),(7, 0)),((7, 1), (6, 2)),((5, 0), (6, 0)), ((5, 1), (4, 2)),((3,3),(3,4)),((3, 2),(4, 1))]
			
			im = embed(IMAGE,8,LOGO_1,LOGO_2,rep)
			path = attack_model.attackImage(im,ATTACK,["noise",(0,0.01)],KEY,COPT,MODEL)
			extractLogoFromImage(path,8,SECRET_PAIRS,rep)
	else:
		return

if __name__ == '__main__':
	testAttack()