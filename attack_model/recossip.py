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
	
	return s1

	
if __name__ == '__main__':
	a = recsip([7, 6, 7, 1, 5, 2, 3],[4, 6, 7, 1, 5, 2, 3],5)
	print(a)