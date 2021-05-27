import os,sys
import re
import ast
from collections import Counter
from recossip import recsip
import math

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
	if(mode == 'crop' or 'jpeg'):
		if(s1 != sip):
			new_sip = recsip(s1,sip,5)
			print("fixed sip: ",new_sip)
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
		args = ast.literal_eval(ARGS)
		if(ATTACK == 'crop'):
			# we dont want to embed when image is edited
			# just test if watermark can be extracted
			path = attack_model.attackImage("watermarked_"+IMAGE_NAME+".jpg",ATTACK,args,KEY,COPT,MODEL)
			s1,s2,s3 = extract_model.getSip(path,size)
			recostructSip(sip,s1,s2,s3,ATTACK)
		elif(ATTACK == 'rotate'):
			embed_model.getWatermarkedImage(IMAGE,sip,size,IMAGE_NAME,COPT)
			args = ast.literal_eval(ARGS)
			path = attack_model.attackImage("watermarked_"+IMAGE_NAME+".jpg",ATTACK,args,KEY,COPT,MODEL)
			s1,s2,s3 = extract_model.getSip(path,size)
			detectSipRotation(s1)
			detectSipRotation(s2)
			detectSipRotation(s3)
			if(args[0] == 0):
				print("sip : ",sip,"\n","s1 : ",s1,"\n","s2 : ",s2,"\n","s3 : ",s3)
		else:
			embed_model.getWatermarkedImage(IMAGE,sip,size,IMAGE_NAME,COPT)
			args = ast.literal_eval(ARGS)
			path = attack_model.attackImage("watermarked_"+IMAGE_NAME+".jpg",ATTACK,args,KEY,COPT,MODEL)
			s1,s2,s3 = extract_model.getSip(path,size)
			print("sss",s1)
			recostructSip(sip,s1,s2,s3,ATTACK)
	elif(MODEL == 'logo'):
		attack_model = initModel(MODEL)
		args = ast.literal_eval(ARGS)
		LOGO_1 = sys.argv[5]
		LOGO_2 = sys.argv[6]
		#rep = (3,1)
		#rep = (5,1)
		rep = (3,1)
		KEY = "no key"
		COPT = "no c"
		#SECRET_PAIRS = [((2,0),(3,0)),((2,1),(3,1)),((2,2),(3,2)),((2,5),(2,6)),((2,7),(3,0)),((3,1),(3,2)),((3,3),(3,4)),((3,5),(3,6)),((3,7),(4,0)),((4,1),(4,2)),((4,3),(4,4))]
		#SECRET_PAIRS = [((2,7),(3,0)),((3,1),(3,2)),((3,3),(3,4)),((3,5),(3,6)),((3,7),(4,0)),((4,1),(4,2)),((4,3),(4,4))]
		#SECRET_PAIRS = [((3,3),(3,4)),((3,5),(3,6)),((3,7),(4,0)),((4,1),(4,2)),((4,3),(4,4))]
		SECRET_PAIRS = [((3,7),(4,0)),((4,1),(4,2)),((4,3),(4,4))]
		im = embed(IMAGE,8,LOGO_1,LOGO_2,rep)
		path = attack_model.attackImage(im,ATTACK,args,KEY,COPT,MODEL)
		extractLogoFromImage(path,8,SECRET_PAIRS,rep)
		return
	else:
		return

if __name__ == '__main__':
	testAttack()