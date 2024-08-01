from __future__ import print_function 
import numpy as np 
import matplotlib.pyplot as plt 
from scipy.optimize import curve_fit
import pandas as pd
import glob, os, csv
from scipy.signal import find_peaks
 
    
f_dir_i = 'put name of location of data files here' + os.sep
 
fns = glob.glob(f_dir_i + '*.csv')

file_path = 'create name for data file here'
  
with open(file_path, mode='a', newline='') as file:
    writer = csv.writer(file)
    writer.writerows([['file name', 'time', 'fl1', 'full_width1', 'time1', 'offset', 'fl2', 'full_width2', 'delay']])

for fileName in fns: 
    print(fileName)
    df = pd.read_csv(fileName) 
    
    first_column_name = df.columns[0]
    second_column_name = df.columns[1]  
    
    ydata = df[second_column_name][1:]
    ydata = ydata.astype(np.float64)
    ydata = np.asarray(ydata)
    
    xdata = df[first_column_name][1:]
    xdata = xdata.astype(np.float64)
    xdata = np.asarray(xdata)

    ydata_peak1 = ydata[300:800]
    ydata_peak2 = ydata[1000:1750]

    
    a, properties = find_peaks(ydata_peak1, prominence=0.1, width=50)
    try:
        peak_loc1 = 300 + a[0]
    except:
        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([fileName])
        continue
    
    b, properties = find_peaks(ydata_peak2, prominence=0.1, width=50)
    try:
        delay = 1000 + b[0] - peak_loc1
    except:
        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([fileName])
        continue
    

     
    # Define the Gaussian function 
    def Gauss(x, A, B, C, D, E, F, G): 
    	y = A*np.exp(-1*((x-C)*2/B)**2) + D + E*np.exp(-1*((x-G-C)*2/F)**2)
    	return y 
    try:
        parameters, covariance = curve_fit(Gauss, xdata, ydata, p0=[0.4, 20, xdata[peak_loc1], 0, 0.4, 20, xdata[delay]], maxfev=100000)
        if parameters[0] < 0:
            raise Exception("noise")
    except:
        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([fileName])
        continue
    
    fit_A = parameters[0] 
    fit_B = parameters[1] 
    fit_C = parameters[2]
    fit_D = parameters[3]
    fit_E = parameters[4]
    fit_F = parameters[5]
    fit_G = parameters[6]
    
    with open(fileName, mode='r') as file:
        reader = csv.reader(file)
        rows = list(reader)
        time = rows[0][1]

        
    data = [
            [fileName, time, fit_A, fit_B, fit_C, fit_D, fit_E, fit_F, fit_G] 
    ]  
    
    # Append data to CSV file
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)
    
    fit_y = Gauss(xdata, fit_A, fit_B, fit_C, fit_D, fit_E, fit_F, fit_G) 
    plt.plot(xdata, ydata) 
    plt.plot(xdata, fit_y) 
