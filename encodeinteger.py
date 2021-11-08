# THIS FUNCTION ENCODES AN INTEGER INTO 
# A SELF INVERTING PERMUTATION



def bitonic(X,Y):
	X.sort()               # sort X list in an ascending order
	Y.sort(reverse=True)   # sort Y list in an descending order
	p = X + Y
	return p

def getCycles():
	return C_list

def getBinary(num):
	B = list(bin(num)[2:])
	return B

def flip(B_star):
	B = []
	for i in range(len(B_star)):
		if(B_star[i] == 0):
			B.append(1)
		if(B_star[i] == 1):
			B.append(0)
	return B

def encodeInteger(key):

		sip = []
		P_b = []
		B = []
		C_list = []
		B_inverse = []
		# FORM BINARY REPRESANTATION O INPUT INTEGER
		B = getBinary(key)						  			  # bin function returns the binaty representation as string so we form a list of characters
		B = [int(i) for i in B]								  # this characters are just 0 and 1 so we reform the list to contain ints
		B_inverse = []
		X_seq = []
		Y_seq = []

		# FORM 000...0||B||0 WHERE ZEROS AT THE START ARE n*
		for i in range(len(B)):
			B.insert(0,0)                                      # insert n (lenght of B) 0s in front of the binary representation of key
		B.insert(len(B),0)                                     # insert one extra 0 in the end

		# FORM FLIP(B) = B'
		B_inverse = flip(B)


		#FORM X AND Y SEQUENCES
		for i in range(len(B_inverse)):
			if(B_inverse[i] == 0):
				X_seq.append(i + 1)
			if(B_inverse[i] == 1):
				Y_seq.append(i + 1)


		# FORM THE BITONIC SEQUENCE
		P_b = bitonic(X_seq,Y_seq)

		# FORM CYCLES 
		N = len(P_b)
		M = 0
		if(N % 2 == 0):             # check if permutation has odd or even length
			M = N / 2				# M represents the how many cycles we have
		else:                       # for example if πb(5,6,9,8,7,4,3,2,1) is the bitonic permutation has odd length
			M = int(N / 2) + 1      # so we will have M = 5 cycles, 4 2-cycle and 1 1-cycle

		for i in range(M):
			if(P_b[i] == P_b[len(P_b) - i - 1]):    # case1: the number from the left is the same with the number from right (we are in the middle of πb)
				t = (P_b[i])
				C_list.append(t)
			else:
				t = (P_b[i],P_b[len(P_b) - i - 1])  # case2: we are not in the middle of πb so we form a 2-cycle t = (pi,pj)
				C_list.append(t)                    # where pi is the i-th number from the left and pj is the j-th number from right of πb
								                    # in the end C_list looks like that [(p1,p2),(p3,p4),...]

		# FORM PERMUTATION FOLLOWING THE GIVEN ALGORITHM
		sip = P_b
		#P_b = sip
		for i in range(len(C_list)):
			t = C_list[i]
			if(type(t) is tuple):                  # checking if we have tupple or not because when we put one single digit as tupple in python
				a = t[0]						   # by default python add's it as single number not as tupple
				b = t[1]
				sip[a - 1] = b
			else:
				a = t
				sip[a - 1] = a
		#del P_b[:]
		return sip


if __name__ == '__main__':
	sip = encodeInteger(128)
	print(sip)