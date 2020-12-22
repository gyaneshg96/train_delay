
# coding: utf-8

# In[1]:

from __future__ import print_function
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests

from bs4 import BeautifulSoup

from scipy import stats
import statsmodels.api as sm


# In[2]:
#print (str(sys.argv[0]))'
url = 'http://www.irctclive.in/RunningTrainHistoryStatus/'+(str(sys.argv[0]))+'/lastyear'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')


# In[3]:

table = soup.find_all(class_='table datatable table-striped table-bordered')


# In[4]:

date = []
delay = []
for row in table[0]('tr')[1:]:
    col = row('td')
    date.append(col[0].string)
    delay.append(col[2].string)


# In[5]:

dtime = []
for time in delay:
    if time.find('Hr') != -1:
        dtime.append(60*int(time[0:time.find('Hr')]) + int(time[time.find('Hr')+3:time.find('Min')]))
    elif time.find('Min') != -1:
        dtime.append(int(time[0:time.find('Min')]))
    else:
        dtime.append(0)


# In[6]:

R = 0.25
smoothed_dtime = [0]*len(dtime)
smoothed_dtime[0] = dtime[0]
for t in range(1,len(dtime)):
    smoothed_dtime[t] = R*dtime[t] + (1-R)*smoothed_dtime[t-1]
rng = pd.date_range('1/1/2016', periods=len(smoothed_dtime), freq='D')


# In[10]:

df = pd.Series(smoothed_dtime, index=rng)



n,x,c = plt.hist(df, 100, normed=0)
plt.xlabel('Delay in minutes')
plt.ylabel('Days in year')

summ = 0 # finding cdf of the histogram
cumulative = []
for i in range(len(x)-1):
	summ = summ + n[i]*(x[i+1]-x[i])
	cumulative.append(summ)

confidence = cumulative[99]*0.95
# In[16]:

#plt.semilogy(x[0:100],n)
#plt.show()


# In[17]:

from scipy.optimize import curve_fit
def model(t, a, b,c):
   return a*np.exp(-b*t) + c
def model2(t, a, b,c): #for Gamma Function, used for fitting
   return a*np.exp(-b*t)*t**(c-1)
# In[18]:

#y = model(30, 2, 3)
#y


# In[19]:

from scipy.stats import gamma
bins = []
diff = 10 #the additional time beyond mean delay
conf = 50 
for i in range(100):  #for midpoints of bins
	bins.append((x[i]+x[i+1])/2) 
bins = np.array(bins)
for i in range(len(x)-2): #for finding the percentage chance for falling in mean + 10mins
	if cumulative[i] <= confidence and cumulative[i+1] >= confidence:
		pvalue = bins[i] + (bins[i+1]-bins[i])*(confidence - cumulative[i])/(cumulative[i+1] - cumulative[i])
	if np.mean(smoothed_dtime) + diff >= bins[i] and np.mean(smoothed_dtime) + diff <= bins[i+1]:
		conf = cumulative[i] + (np.mean(smoothed_dtime) + diff - bins[i])*(cumulative[i+1] - cumulative[i])/(bins[i+1] - bins[i])

percent = conf/summ
popt, pcov = curve_fit(model2, bins, n, bounds=(0,[100,0.08,6.5])) #fit

# For calculating r adjusted
sst = 0
ssr = 0
for i in range(len(bins)):
	sst = sst + (n[i]-np.mean(np.array(n)))**2
	ssr = ssr + (n[i]-model2(bins[i], popt[0], popt[1], popt[2]))**2
	
rsquared = (1-ssr/sst)
rsquared_adjusted = rsquared -(1-rsquared)*3/(96)
plt.plot(bins[0:100], model2(bins[0:100], popt[0], popt[1], popt[2]))
n,x,c = plt.hist(df, 100, normed=0)
plt.bar(x[0:100],n)
plt.xlabel('Delay')
plt.ylabel('Days')
#plt.savefig('graphs/delay'+str(sys.argv[0])+'.png')
plt.close()
plt.show()
# In[ ]:



