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
ARG1 = sys.argv[3]
ARG2 = sys.argv[4]
ARG3 = sys.argv[5]
MODEL = sys.argv[6]


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
from NC import calculate_C,similarity,similaritysip

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

			print("SIMILARITY PER CHANNEL BEFORE RECOSTRUCTION:\n")

			c1 = similaritysip(s1,sip)
			c2 = similaritysip(s2,sip)
			c3 = similaritysip(s3,sip)

			print(c1," ",c2," ",c3,'\n')

			new_sip1 = recsip(s1,sip,5)
			new_sip2 = recsip(s2,sip,5)
			new_sip3 = recsip(s3,sip,5)

			print("SIMILARITY PER CHANNEL AFTER RECOSTRUCTION:\n")

			print(new_sip1,new_sip2,new_sip3)


			c1 = similaritysip(new_sip1,sip)
			c2 = similaritysip(new_sip2,sip)
			c3 = similaritysip(new_sip3,sip)

			print(c1," ",c2," ",c3,'\n')


			if(new_sip1 == sip):
				print("fixed sip: ",new_sip1)
				print("Similarity reached: ",c1)
			elif(new_sip2 == sip):
				print("fixed sip: ",new_sip2)
				print("Similarity reached: ",c2)
			elif(new_sip3 == sip):
				print("fixed sip: ",new_sip3)
				print("Similarity reached: ",c3)
			else:
				print("Sip is not found yet!")
				print("Similarity per channel: \n",c1,"\n",c2,"\n",c3)
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
		KEY = int(sys.argv[7])
		COPT = float(sys.argv[8])
		attack_model,embed_model,extract_model = initModel(MODEL)
		sip = encodeInteger(KEY)
		size = len(sip)
		#args = ast.literal_eval(ARGS)
		if(ATTACK == 'crop'):
			# we dont want to embed when image is edited
			# just test if watermark can be extracted
			embed_model.getWatermarkedImage(IMAGE,sip,size,IMAGE_NAME,COPT,2,2)
			path = attack_model.attackImage("watermarked_"+IMAGE_NAME+".jpg",ATTACK,[ARG1,ARG2,ARG3],KEY,COPT,MODEL)
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
			path = attack_model.attackImage("watermarked_"+IMAGE_NAME+".jpg",ATTACK,[ARG1,(ARG2,ARG3)],KEY,COPT,MODEL)
			s1,s2,s3 = extract_model.getSip(path,size,2,2)
			print(s1,s2,s3)
			#similaritysip(s1,sip)
			recostructSip(sip,s1,s2,s3,ATTACK)
	elif(MODEL == 'logo'):
		if(ATTACK == 'crop'):
			attack_model = initModel(MODEL)
			LOGO_1 = sys.argv[7]
			LOGO_2 = sys.argv[8]
			rep = (7,1)
			KEY = "no key"
			COPT = "no c"
			SECRET_PAIRS = [((4, 3),
				(5, 2)),((6, 1),(7, 0)),((7, 1), (6, 2)),((5, 0), (6, 0)), ((5, 1), (4, 2)),((3,3),(3,4)),((3, 2),(4, 1))]
			# STUPID SYNTAX CAN EASILY BE FORGOTTEN
			# DONT BE LIKE THAT WRITE CLEAN CODE
			im = embed(IMAGE,8,LOGO_1,LOGO_2,rep)
			path = attack_model.attackImage(im,ATTACK,[ARG1,ARG2,ARG3],KEY,COPT,MODEL)
			lg1,lg2 = extractLogoFromImage(path,8,SECRET_PAIRS,rep)

			im1 = Image.fromarray(lg1)
			im2 = Image.fromarray(lg2)

			print(ARG1)

			path1 = "M:\\BSc-Watermarking\\code\\attack_model\\logo11.png"
			path2 = "M:\\BSc-Watermarking\\code\\attack_model\\logo12.png"

			if(ARG3 == "cols" or ARG3 == "rows"):
				path3 = "M:\\BSc-Watermarking\\code\\attack_model\\charts\\geometric_charts\\" + IMAGE_NAME + "\\(7,1)\\intresting_cases\\" + ARG1 + "_" + ARG3 +  "\\logo1" + str("") + ".png"
				path4 = "M:\\BSc-Watermarking\\code\\attack_model\\charts\\geometric_charts\\" + IMAGE_NAME + "\\(7,1)\\intresting_cases\\" + ARG1 + "_" + ARG3 +"\\logo2" + str("") + ".png"
			if(ARG3 == "white" or ARG3 == "black"):
				path3 = "M:\\BSc-Watermarking\\code\\attack_model\\charts\\geometric_charts\\" + IMAGE_NAME + "\\(7,1)\\intresting_cases\\" + ARG1 + "x" + ARG2 + "_" + ARG3 +  "\\logo1" + str("") + ".png"
				path4 = "M:\\BSc-Watermarking\\code\\attack_model\\charts\\geometric_charts\\" + IMAGE_NAME + "\\(7,1)\\intresting_cases\\" + ARG1 + "x" + ARG2 + "_" + ARG3 +"\\logo2" + str("") + ".png"
			

			im1.save(path3,quality=100,subsampling=0)
			im2.save(path4,quality=100,subsampling=0)


			similarity(path1,lg1)
			similarity(path2,lg2)

			#M:\BSc-Watermarking\code\attack_model\charts\filter_charts\sharpening\logos
			
		else:

			attack_model = initModel(MODEL)
			#args = ast.literal_eval(ARGS)
			LOGO_1 = sys.argv[7]
			LOGO_2 = sys.argv[8]
			#rep = (3,1)
			#rep = (5,1)
			rep = (11,1)
			KEY = "no key"
			COPT = "no c"
			SECRET_PAIRS = [((1, 4), (2, 3)), ((3, 2), (4, 1)), ((5, 0), (6, 0)), ((5, 1), (4, 2)), ((3, 3), (2, 4)), ((1, 5), (0, 6)), ((0, 7), (1, 6)), ((2, 5), (3, 4)), 
								((4, 3), (5, 2)), ((6, 1), (7, 0)), ((7, 1), (6, 2))]
			
			
			im = embed(IMAGE,8,LOGO_1,LOGO_2,rep)
			path = attack_model.attackImage(im,ATTACK,[ARG1,(ARG2,ARG3)],KEY,COPT,MODEL)
			lg1,lg2 = extractLogoFromImage(path,8,SECRET_PAIRS,rep)

			
			im1 = Image.fromarray(lg1)
			im2 = Image.fromarray(lg2)

			path1 = "M:\\BSc-Watermarking\\code\\attack_model\\logo11.png"
			path2 = "M:\\BSc-Watermarking\\code\\attack_model\\logo12.png"
		
			if(ARG1 == "gamma"):
				path3 = "M:\\BSc-Watermarking\\code\\attack_model\\charts\\filter_charts\\" + ARG1 + "\\logos\\" + ARG1 + "(" + ARG2 +")\\" + "\\512x512\\" + IMAGE_NAME +"\\logo1" + str("") + ".png"
				path4 = "M:\\BSc-Watermarking\\code\\attack_model\\charts\\filter_charts\\" + ARG1 + "\\logos\\" + ARG1 + "(" + ARG2 +")\\" + "\\512x512\\" + IMAGE_NAME +"\\logo2" + str("") + ".png"
			elif(ARG1 == "gaussian_noise"):
				path3 = "M:\\BSc-Watermarking\\code\\attack_model\\charts\\filter_charts\\" + ARG1 + "\\logos\\" + ARG1 + "(" + ARG3 +")\\" + IMAGE_NAME +"\\logo1" + str("") + ".png"
				path4 = "M:\\BSc-Watermarking\\code\\attack_model\\charts\\filter_charts\\" + ARG1 + "\\logos\\" + ARG1 + "(" + ARG3 +")\\" + IMAGE_NAME +"\\logo2" + str("") + ".png"
			else:
				path3 = "M:\\BSc-Watermarking\\code\\attack_model\\charts\\filter_charts\\" + ARG1  + "\\logos\\" + IMAGE_NAME +"\\logo1" + str("") + ".png"
				path4 = "M:\\BSc-Watermarking\\code\\attack_model\\charts\\filter_charts\\" + ARG1  + "\\logos\\" + IMAGE_NAME + "\\logo2" + str("") + ".png"

			im1.save(path3,quality=100,subsampling=0)
			im2.save(path4,quality=100,subsampling=0)


			similarity(path1,lg1)
			similarity(path2,lg2)
			
			#M:\BSc-Watermarking\code\attack_model\charts\filter_charts\gamma\logos\gamma(0.25)



	else:
		return 

if __name__ == '__main__':
	testAttack()