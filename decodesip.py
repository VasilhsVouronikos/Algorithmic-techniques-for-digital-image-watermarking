# THIS FUNCTION DECODES A SELF INVERTING PERMUTATION
# BACK TO THE INPUT INTEGER

def findSubsequences(p):
	X_seq = []
	Y_seq = []
	for i in range(len(p) - 1):             # to find the X and Y sequence we just compare p[i] and p[i + 1]
		if(p[i] < p[i + 1]):                # for example p = (5, 6, 9, 8, 1, 2, 7, 4, 3) , p[i] = 5 and p[i + 1] = 6
			X_seq.append(p[i])              # so 5 will go in the X and we continue with 6 and 9 and so on
		else:						        # we do this fo all the elements except for the last one so we dont have problems with the bounds of the list
			Y_seq.append(p[i])
	if(p[len(p) - 1] < p[len(p) - 2]):      # Here we handle the last element compare it with the previous element in our list the number 4
		Y_seq.append(p[len(p) - 1])
	else:
		X_seq.append(p[len(p) - 1])
	

	return X_seq,Y_seq

def initList(N):
	l = []
	for i in range(N):                     # initList just initialize a list with a gine length N with zeros
		l.append(0)                        # we use this function to initialize some of our lists in decodeSip function
	return l

def flip(B):
	B_inverse = []
	for i in range(len(B)):                # flip function just flips the elements of a given list of 0s and 1s
		if(B[i] == 0):
			B_inverse.append(1)
		if(B[i] == 1):
			B_inverse.append(0)
	return B_inverse

def decodeSip(sip):

	cycle_list = []

	N = len(sip)			              # length of initial bitonic permutation

	if(N % 2 == 0):             
		M = int(N / 2)				
	else:                       
		M = int(N / 2) + 1    
	# FORM CYCLES FROM SIP

	for i in range(M - 1):
		t = (sip[i] , i + 1)              # to form cycles we go from the start of the sip list to the middle
		cycle_list.append(t)              # and we form tupples containg (sip[i],i + 1) , i + 1 because list first index starts from 0
										  # also the loop goes to M - 1 so we dont have problems with list bounds because of the element i + 1
	for k in range(len(sip)):
		if(k + 1 == sip[k]):              # Here we handle the 1-cycle element.In the sip list the only element that has same value in index and element
			cycle_list.append(sip[k])     # is the middle element of the bitonic permutation and this element forms 1-cycle
										  # so we go through the sip list and we find the element that has same index and value

	# REVERSE THE CYCLE LIST
	cycle_list.reverse()

	# INITIALIZE BITONIC PERMUTATION
	P_b = initList(N)

	# FORM BITONIC PERMUTATION
	i = 0
	j = N
	for k in range(M):
		if(type(cycle_list[len(cycle_list) - k - 1]) is tuple):
			t = cycle_list[len(cycle_list) - k - 1]
			P_b[i] = t[0]
			P_b[j - 1] = t[1]
			i += 1
			j -= 1
			k += 1
		else:
			t = cycle_list[len(cycle_list) - k - 1]
			P_b[i] = t
			i += 1
			k += 1


	# FORM X AND Y SEQUENCES

	X,Y = findSubsequences(P_b)

	# FORM B*
	B_inverse = initList(N)

	for i in range(len(X)):
		B_inverse[X[i] - 1] = 0
	for j in range(len(Y)):
		B_inverse[Y[j] - 1] = 1


	# FORM B

	B = flip(B_inverse)


	# FORM DECIMAL FROM BINARY
	B = [str(B[i]) for i in range(len(B))]   # we turn the int B list to string so the int(B,2) will work
	B = ''.join(B)                           # we turn the list to string
	key = int((int(B,2)) / 2)                # then the string representation of the binary to decimal
                                             # we divide by 2 because by adding an extra 0 in the end of B we shift left the number
	return key

if __name__ == '__main__':
	# inorder traversal to the sequence
	l = [8,4,12,2,6,10,13,1,3,5,7,9,11]
	s = decodeSip(l)
	print(s)