#!/usr/bin/python

import sys
from bs4 import BeautifulSoup
import urllib
import numpy as np

r = urllib.urlopen('file:///home/gyanesh/Downloads/HCC/National%20Train%20Enquiry%20System%20-Indian%20Railways.html').read()
soup = BeautifulSoup(r)
train_num =[]
temp = []
tmp = soup.find_all(class_="trainNo")
for k in range(len(tmp)/2):
	train_num.append(tmp[k].string)
	sys.argv=[tmp[k].string]
	if k not in [10,11]:
		execfile('trains_analysis.py')
		temparr = np.array(dtime)
		temp.append((np.mean(temparr), np.std(temparr),percent,rsquared_adjusted))
		
r = urllib.urlopen('file:///home/gyanesh/Downloads/HCC/National%20Train%20Enquiry%20System%20-Indian%20Railways.html').read()
soup = BeautifulSoup(r)
tmp = soup.findChildren(['td'])
train_list = []
for i in range(72):
	if i not in [10,11]:
		train_list.append([tmp[58+16*i].string, tmp[60+16*i].string, tmp[71+16*i].string, tmp[72+16*i].string])

for w in train_list:	
	w[0] = int(w[0])
	w[1] = str(w[1])
	w[2] = str(w[2])
	w[3] = str(w[3])
	w[3] = int(w[3][:2])*60 + int(w[3][3:])
	if w[1] == 'SUPERFAST':		
		w.append(745)    
	if w[1] == 'RAJDHANI':
                w.append(940)
        if w[1] == 'GARIB RATH':
                w.append(515)
        if w[1] == 'SHATABDI':
                w.append(870)
        if w[1] == 'MAIL EXP':
                w.append(685)
        if w[1] == 'DURONTO':
                w.append(850)
	t = w[4]
	w[4] = w[3]
	w[3] = w[2]
	w[2] = t

for i in range(len(temp)):
	train_list[i].append(round(temp[i][0],2))
	train_list[i].append(round(temp[i][0]+train_list[i][4],2))
	train_list[i].append(round(temp[i][2]*100))
	train_list[i].append(round(temp[i][3],3))




