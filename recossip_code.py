import os , sys
from collections import Counter


def passes(s,sip,key,mod):
	if(mod == "left"):
		pairs = []

		for i in range(len(s)):
			pairs.append((i+1,s[i]))

		new_sip = []

		k = int(len(pairs) / 2)
		for i in range(0,k):
			x = pairs[i][0]
			y = pairs[i][1]

			rev = (y,x)

			if(rev in pairs):
				pass
			else:
				pairs[y - 1] = (y,x)
		

		for i in range(len(pairs)):
			new_sip.append(pairs[i][1])

		return new_sip

	if(mod == "right"):
		pairs = []

		for i in range(len(s)):
			pairs.append((i+1,s[i]))

		new_sip = []

		k = int(len(pairs) / 2)
		for i in range(len(pairs)-1,k,-1):
			x = pairs[i][0]
			y = pairs[i][1]

			rev = (y,x)

			if(rev in pairs):
				print(pairs[i])
				pass
			else:
				print(pairs[i])
				pairs[y - 1] = (y,x)
		

		for i in range(len(pairs)):
			new_sip.append(pairs[i][1])

		return new_sip

	if(mod == "middle"):
		pairs = []
		new_sip = []

		for i in range(len(s)):
			pairs.append((i+1,s[i]))

		for i in range(len(pairs)):
			x = pairs[i][0]
			y = pairs[i][1]

			rev = (y,x)

			if(rev in pairs):
				pass
			else:
				pairs[x - 1] = (x,x)

		for i in range(len(pairs)):
			new_sip.append(pairs[i][1])

		return new_sip

	if(mod == "start"):
		B = list(bin(key)[2:])
		k = len(B)

		new_sip = []

		for i in range(len(s)):
			new_sip.append(s[i])

		
		new_sip[0] = k + 1
		new_sip[k] = 1


		return new_sip

def recsip(s1,sip,key):

	if(s1 != sip):
		new_sip = passes(s1,sip,key,"start")
		

	
	if(new_sip != sip):
		new_sip = passes(new_sip,sip,key,"left")

		if(new_sip != sip):
			new_sip = passes(new_sip,sip,key,"middle")
		

	# P5 property of SIP says:
	# if we have the binary represantation B = list(binary(key)) of some key = X
	# then sip[0] = length(B) + 1
	# and sip[length(B)] = 1
	# 	for examble key = 5 has B = [1,0,1]
	# 	so length(B) = 3
	# 	sip[0] = 4 and sip[3] = 1
	# 	so we know for sure 2 valid numbers of sip 
	# 	in this step sip looks like sip = [4,0,0,1,0,0,0]
	'''
	B = list(bin(key)[2:])
	s = len(B)

	new_sip[0] = s + 1
	new_sip[s] = 1


	
	for i in range(len(s1)):
		if(s1[s1[i] - 1] != i + 1):
			s1[s1[i] - 1] = i + 1
	

	if(s1[0] != s + 1):
		s1[0] = s + 1
	if(s1[s] != 1):
		s1[s] = 1

	s1[s + 1] = s + 2

	c = 0

	for i in range(len(s1)):
		k = s1[c] - 1
		if(s1[k]  == c + 1):
			pass
		else:
			s1[s1[c] - 1] = c + 1
		c = c + 1
	
	for i in range(len(s1)):
		if(s1[i] in valid_nums):
			continue
		else:
			#print(valid_nums[i])
			s1[valid_nums[i] - 1] = valid_nums[i]
	'''
	
	return new_sip


if __name__ == '__main__':
	a = recsip( [4, 6, 7, 1, 7, 2, 3],[4,6,7,1,5,2,3],5)
	print(a)