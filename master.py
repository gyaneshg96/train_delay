execfile('train_no.py')

x = 1
def timeconv(t):
	return int(t[:2])*60 + int(t[3:])
input1 = [600,800]
input2 = ["06:30","14:00"]
while (x==1):
	input1 = input('Enter range of prices e.g. [600,800]\n')
	input2 = input('Enter preferred range of time e.g. ["06:30","14:00"]\n')
	if (input2[0]>input2[1]):
		tot1 = [w for w in train_list if w[2]>=input1[0] and w[2]<=input1[1] and timeconv(w[3])+w[5] >= timeconv(input2[0]) and  timeconv(w[3])+w[5] <= 1440]
		tot2 = [w for w in train_list if w[2]>=input1[0] and w[2]<=input1[1] and timeconv(w[3])+w[5]-1440 >= 0 and timeconv(w[3])+w[5] - 1440 <= timeconv(input2[1]) ]
		tot = tot1+tot2
	else:
		tot = [w for w in train_list if w[2]>=input1[0] and w[2]<=input1[1] and timeconv(w[3])+w[5] >= timeconv(input2[0]) and  timeconv(w[3])+w[5] <= timeconv(input2[1])]
	print('The trains are ranked in the order as you required\n')
	for tt in sorted(tot, key=lambda train: train[6])[:5]:
		print (tt)
	x = input('Press 1. for another entry, 2. for quitting\n')

print ('Thank you!')

