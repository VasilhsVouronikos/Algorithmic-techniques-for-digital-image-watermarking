import os , sys
from collections import Counter

def recsip(s1,sip,key):
	
	# ---- TO DO-----

	pairs = []
	for i in range(len(s1)):
		pairs.append((i+1,s1[i]))


	new_sip = []
	for i in range(len(sip)):
		new_sip.append(0)

	# P5 property of SIP says:
	# if we have the binary represantation B = list(binary(key)) of some key = X
	# then sip[0] = length(B) + 1
	# and sip[length(B)] = 1
	# 	for examble key = 5 has B = [1,0,1]
	# 	so length(B) = 3
	# 	sip[0] = 4 and sip[3] = 1
	# 	so we know for sure 2 valid numbers of sip 
	# 	in this step sip looks like sip = [4,0,0,1,0,0,0]

	B = list(bin(key)[2:])
	s = len(B)
	new_sip[0] = s + 1
	new_sip[s] = 1

	pairs.remove(pairs[0])
	pairs.remove(pairs[s-1])

	# ---- TO DO ------
	pair_copy = []
	for i in range(len(pairs)):
		pair_copy.append(pairs[i])
	for i in range(len(pairs)):
		x = pairs[i][0]
		y = pairs[i][1]
		pair_copy.remove((x,y))
		z = findSimilar((x,y),pair_copy)
		if(z is not None and z[0] != new_sip[0] and z[1] != new_sip[0] and z[0] != new_sip[s] and z[1] != new_sip[s]):
			new_sip[z[0] - 1] = z[1]
			new_sip[z[1] - 1] = z[0]
	return new_sip

def findSimilar(t,l):
	p = None
	for i in range(len(l)):
		k = l[i][1]
		w = l[i][0]
		#print((w,k),(t[0],t[1]))
		if(w == t[1] and k != t[0]):
			return l[i]
		elif(w != t[1] and k != t[0]):
			return l[i]
		else:
			continue

	

if __name__ == '__main__':
	sip = [4, 6, 7, 1, 5, 2, 3]
	s = recsip([1, 3, 5, 7, 5, 2, 3],sip,5)
	print(s)
	