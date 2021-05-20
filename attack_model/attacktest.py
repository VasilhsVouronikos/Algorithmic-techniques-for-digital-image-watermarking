import os,sys
import re
import ast

ATTACK = sys.argv[1]
IMAGE = sys.argv[2]
IMAGE_NAME = re.split(r'\.(?!\d)', IMAGE)[0]
ARGS = sys.argv[3]
KEY = int(sys.argv[4])
COPT = float(sys.argv[5])

def get_current_path():
	path = os.getcwd().split("\\")
	path.pop(0)
	path.pop(len(path)-1)
	new_path = "\\"+"\\".join(path)
	
	return new_path

path_to_extract = get_current_path()

sys.path.insert(0,path_to_extract)

from extract import ExtractPermutation
from embed import EmbedPermutation
from encodeinteger import encodeInteger
from decodesip import decodeSip
from attackimage import attackModel

def initModel():
	model = attackModel()
	w = EmbedPermutation()
	ex = ExtractPermutation()
	return model,w,ex

def recostructSip(sip,s1,s2,s3,mode):
	if(mode == 'crop'):
		pairs = []
		pairs1 = []
		black = []
		for i in range(len(sip)):
			pairs.append((i+1,sip[i]))
		for i in range(len(s1)):
			pairs1.append((i+1,s1[i]))
		for i in range(len(pairs1)):
			p = (pairs1[i][1],pairs1[i][0])
			p1 = (pairs1[i])
			if(p not in pairs1 and p not in pairs):
				black.append(p)
		for i in range(len(black)):
			k = black[i][0]
			l = black[i][1]
			items = list(filter(lambda x: x[1] == l, pairs1))
			s1[items[0][1] - 1] = items[0][0]
		print("fixed sip: ",s1)
	elif(mode == 'rotate'):
		print("sip : ",sip,"\n","s1 : ",s1[::-1],"\n","s2 : ",s2[::-1],"\n","s3 : ",s3[::-1])
	else:
		print("sip : ",sip,"\n","s1 : ",s1,"\n","s2 : ",s2,"\n","s3 : ",s3)

def testAttack():
	attack_model,embed_model,extract_model = initModel()
	sip = encodeInteger(KEY)
	size = len(sip)
	args = ast.literal_eval(ARGS)
	# we dont want to embed when image is edited
	# just test if watermark can be extracted
	if(ATTACK == 'crop'):
		path = attack_model.attackImage("watermarked_"+IMAGE_NAME+".jpg",ATTACK,args,KEY,COPT)
		s1,s2,s3 = extract_model.getSip(path,size)
		recostructSip(sip,s1,s2,s3,ATTACK)
	else:
		embed_model.getWatermarkedImage(IMAGE,sip,size,IMAGE_NAME,COPT)
		args = ast.literal_eval(ARGS)
		path = attack_model.attackImage("watermarked_"+IMAGE_NAME+".jpg",ATTACK,args,KEY,COPT)
		s1,s2,s3 = extract_model.getSip(path,size)
		recostructSip(sip,s1,s2,s3,ATTACK)

if __name__ == '__main__':
	testAttack()