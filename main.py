from encodeinteger import encodeInteger
from decodesip import decodeSip
from embed_key import EmbedPermutation
from extract_sip import ExtractPermutation
import sys
import re



KEY = int(sys.argv[1])
IMAGE = sys.argv[2]
IMAGE_NAME = re.split(r'\.(?!\d)', IMAGE)[0]
COMMAND = sys.argv[3]
COPT = float(sys.argv[4])
global SIP 
global SIZE

def startEncoding():
	global SIP,SIZE
	SIP = encodeInteger(KEY)
	SIZE = len(SIP)

def startEmbeding():
	global SIP,SIZE
	w = EmbedPermutation()
	w.getWatermarkedImage(IMAGE,SIP,SIZE,IMAGE_NAME,COPT,2,2)

def startExtracting():
	ex = ExtractPermutation()
	sip1,sip2,sip3 = ex.getSip(IMAGE,SIZE,2,2)
	return sip1,sip2,sip3

if __name__ == '__main__':
	if(COMMAND == "embed"):
		print("Starting encoding of key: ",KEY)
		startEncoding()
		print("Encoding ended succesfully")
		print("Starting embeding of permutation")
		startEmbeding()
		print("Embeding ended succesfully")
	else:
		print("Starting encoding of key: ",KEY)
		startEncoding()
		print("Encoding ended succesfully")
		print("Starting extraction of permutation")
		s1,s2,s3 = startExtracting()
		print(s1,s2,s3)
		key1 = decodeSip(s1)
		key2 = decodeSip(s2)
		key3 = decodeSip(s3)

		if(key1 == KEY):
			print("Extraction ended succesfully")
			print("Permutation of key key1 = ",key1," ","matches with input ",KEY," with permutation ",SIP)
		elif(key2 == KEY):
			print("Extraction ended succesfully")
			print("Permutation of key key2 = ",key2," ","matches with input ",KEY," with permutation ",SIP)
		elif(key3 == KEY):
			print("Extraction ended succesfully")
			print("Permutation of key key3 = ",key3," ","matches with input ",KEY," with permutation ",SIP)
		else:
			print("None of the extracted permutation matches.")