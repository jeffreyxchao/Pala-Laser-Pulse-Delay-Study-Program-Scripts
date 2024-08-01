from __future__ import print_function 
import numpy as np 
import matplotlib.pyplot as plt 
from scipy.optimize import curve_fit
import pandas as pd
from scipy.signal import find_peaks 
 
fns = 'insert data file to be analyzed'

df = pd.read_csv(fns)
first_column_name = df.columns[1]  
ydata = df[first_column_name][1:]
ydata = ydata.astype(np.float64)
ydata = np.asarray(ydata)


first_column_name = df.columns[0]
xdata = df[first_column_name][1:]
xdata = xdata.astype(np.float64)
xdata = np.asarray(xdata)

ydata_peak1 = ydata[300:800]
ydata_peak2 = ydata[1000:1750]


plt.plot(xdata, ydata)


a, properties = find_peaks(ydata_peak1, prominence=0.1, width=50)
peak_loc1 = 300 + a[0]

#plt.plot(ydata)
#plt.plot(peak_loc1, ydata[peak_loc1], "X")

b, properties = find_peaks(ydata_peak2, prominence=0.1, width=50)
delay = 1000 + b[0] - peak_loc1

#plt.plot(delay, ydata[delay], "X")


# Define the Gaussian function 
def Gauss(x, A, B, C, D, E, F, G): 
	y = A*np.exp(-1*((x-C)*2/B)**2) + D + E*np.exp(-1*((x-G-C)*2/F)**2)
	return y 
parameters, covariance = curve_fit(Gauss, xdata, ydata, p0=[0.4, 20, xdata[peak_loc1], 0, 0.4, 20, xdata[delay]], maxfev=10000)
 
fit_A = parameters[0] 
fit_B = parameters[1] 
fit_C = parameters[2]
fit_D = parameters[3]
fit_E = parameters[4]
fit_F = parameters[5]
fit_G = parameters[6]
fit_y = Gauss(xdata, fit_A, fit_B, fit_C, fit_D, fit_E, fit_F, fit_G) 
plt.plot(xdata, ydata) 
plt.plot(xdata, fit_y, '-')     
