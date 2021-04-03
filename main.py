from encodeinteger import encodeInteger
from decodesip import decodeSip
from embed import EmbedPermutation
from extract import ExtractPermutation
import sys
import re



KEY = int(sys.argv[1])
IMAGE = sys.argv[2]
IMAGE_NAME = re.split(r'\.(?!\d)', IMAGE)[0]
COMMAND = sys.argv[3]
global SIP 
global SIZE

def startEncoding():
	global SIP,SIZE
	SIP = encodeInteger(KEY)
	SIZE = len(SIP)

def startEmbeding():
	global SIP,SIZE
	w = EmbedPermutation()
	w.getWatermarkedImage(IMAGE,SIP,SIZE,IMAGE_NAME)

def startExtracting():
	ex = ExtractPermutation()
	sip = ex.getSip(IMAGE,SIZE)
	return sip

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
		s = startExtracting()
		print("Extraction ended succesfully")
		decodeSip(s)
