# -*- coding: utf-8 -*-
"""
Created on Sun May  9 03:01:26 2021

@author: Kryptic Nessi
"""

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


f = open('Co60.txt','r') # open f i l e
header = f.readline () # re ad and i g n o r e he ade r
channel = np.zeros(1024)# creates an array of zeros with 60 spaces
Ecount = np.zeros(1024)
i = 0

acqtime=3152.79
for line in f : # l o o p o ve r l i n e s
    line = line.replace(',',' ')
    line = line.strip()
    columns = line.split()
    channel[i] = float(columns[0]) # e x t r a c t data
    Ecount[i] = float(columns[1])/acqtime
    i = i + 1
#eventsum=0
#Total number of events (make sure to remove acquisition time)
#for i in range(1024):
#    eventsum += Ecount[i]
#print("total number of events: ",eventsum)


#_________________________________model
H=channel    
#experimental data plot----------------------------------
plt.plot(H,Ecount,'bo',label='pulse height spectrum ')


#Cobalt 60 modification
E0=Ecount
for i in range(len(Ecount)):
    if H[i]<800:
        E0[i]=0
initialGuess = [1,0.5,900]
def Gaus(H,A,sigma,centroid):
    return (A/(sigma*np.sqrt(2*np.pi)))*np.e**(-((H-centroid)**2)/2*sigma**2)

#perform curve fit
popt, pcov = curve_fit(Gaus,H,E0,initialGuess)
print(popt)

# xdata to be supplied to Gaus function
x = np.zeros(1024)
ygauss = np.zeros(1024)
for i in range(1024):
        x[i] = i
ygauss = Gaus(x,*popt)         
#xfit = np.arange(0,600,0.01)--------------------------------


#plt.plot(xfit,Gaus(xfit,*popt),'r')
plt.plot(x,ygauss,'r',label='Gaussian fitting')

plt.legend(loc = 1, numpoints = 2)

plt.grid()
plt.xlabel("Pulse height,\n measured as channel number, channels (prorportional to voltange).")
plt.ylabel("Differential number of pulse heights, per unit time.")
plt.title("Fitted gaussian over the\n pulse height spectrum photo-peak of 137Cs.")
#plt.savefig()

plt.show()
dymin = (Ecount - Gaus(H,*popt))/0.9613
min_chisq = sum(dymin*dymin)
dof = len(H)-len(popt)
#print("Chi square: ", min_chisq)
#print("Number of degrees of freedom: ", dof)
#print("chi square per degree of freedom: ",min_chisq/dof)
#print()
