import os , sys
from collections import Counter

def recsip(s1,sip,key):
	
	# ---- TO DO-----
	valid_nums = []
	pairs = []
	for i in range(len(s1)):
		pairs.append((i+1,s1[i]))

	for i in range(len(sip)):
		valid_nums.append(i+1)

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

	for i in range(len(s1)):
		if(s1[s1[i] - 1] != i + 1):
			s1[s1[i] - 1] = i + 1

	if(s1[0] != s + 1):
		s1[0] = s + 1
	if(s1[s] != 1):
		s1[s] = 1

	for i in range(len(s1)):
		if(valid_nums[i] in s1):
			continue
		else:
			s1[valid_nums[i] - 1] = valid_nums[i]
	"""
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

	print(new_sip)
	for i in range(len(new_sip)):
		if(new_sip[i] == 0):
			new_sip[i] = i + 1
			centralelem = (new_sip[i],i+1)

	print(new_sip)
	if(new_sip != sip):
		new_sip = correctErrors(new_sip,sip,error,centralelem)

	return new_sip

def findSimilar(t,l):
	p = None
	for i in range(len(l)):
		k = l[i][1]
		w = l[i][0]
		if(t[0] == k and t[1] != w):
			return l[i]
		else:
			continue

def correctErrors(new_sip,sip,error,ce):
	swap = []
	#print(sip)
	for i in range(len(new_sip)):
		pos = i + 1
		elem = new_sip[i]
		if(new_sip[elem - 1] != pos):
			continue
		elif(new_sip[i] == pos and (new_sip[i],pos) != ce):
			error[pos - 1] = 0
		else:
			error[pos - 1] = 1
	print(error)
	for i in range(len(error)):
		if(error[i] == 0):
			swap.append(i)
	swap = [(swap[i], swap[i + 1]) 
         for i in range(len(swap) - 1)]
	for i in range(len(swap)):
		x = swap[i][0]
		y = swap[i][1]
		new_sip[x] = y + 1
		new_sip[y] = x + 1

	return new_sip
"""
	return s1
if __name__ == '__main__':
	a = recsip([4, 6, 4, 5, 2, 7, 3],[4, 6, 7, 1, 5, 2, 3],5)
	print(a)