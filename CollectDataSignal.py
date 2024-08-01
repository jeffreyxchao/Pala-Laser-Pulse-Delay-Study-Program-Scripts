import pyvisa
import time # for sleep
from time import strftime
import csv


start_time = time.time()
CODE_DIV = 25

rm = pyvisa.ResourceManager()
print ('oscilloscope address:', rm.list_resources())
sds = rm.open_resource("USB0::0xF4ED::0xEE3A::SDS1EDEX4R3172::INSTR", write_termination = '\n',read_termination='\n')
print('oscilloscope:',sds.query('*IDN?'))

sds.timeout = 10000
sds.chunk_size = 20*1024*1024

sds.write('MEMORY_SIZE 7K')
mem_size=sds.query('MEMORY_SIZE?')
print('memory size:',mem_size)


sds.write("chdr off")


wf_size=2000
wf_start="3000"
waveform="WFSU SP,1,NP,"+str(wf_size)+",FP,"+wf_start
print (waveform)
sds.write(waveform)


tdiv = sds.query("tdiv?")
sara = sds.query("sara?")
vdiv = sds.query("c1:VDIV?")
ofst = sds.query("c1:ofst?")

time_value = []
for idx in range(0, wf_size):
    time_data = 1000000*idx*(1/float(sara))

    time_value.append(time_data)


#--------------------------------------------------------------------------------------------------------------
start_time = time.time()
for j in range(1,1001):
    print("j=",j)
    
    sds.write('STOP')

    a="0"
    i=0
    while True:
        i=i+1
        sds.write('INR?')
        a=sds.read()
        if a == "0":
            #print("i1=",i,a)
            break
        else:
            pass

    sds.write('ARM')

    
    a="0"
    i=0
    while True:
        i=i+1
        sds.write('INR?')
        a=sds.read()
        if a == "1":
            break
        if a == "8193":
            break
        else:
            pass
    sds.write('STOP')

    sds.write("C1:WF? DAT2")
    recv1 = list(sds.read_raw())[16:]
    recv1.pop()
    volt_value = []

    for data in recv1:
        if data > 127:
            data = data - 256
        else:
            pass
        data=data/CODE_DIV*float(vdiv)-float(ofst)
        volt_value.append(data)    
        
    l_time=time.time()
    short_time = strftime("%Y%m%d%H%M%S", time.localtime(l_time))+str(l_time)[11:][:3]    
    timestamp = strftime("%m/%d/%Y %H:%M:%S", time.localtime(l_time)) + "." + str(l_time)[11:][:3] 
    filename = 'insert location path name here' + short_time + '.csv'
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([filename, timestamp])
        
        for times, volt in zip(time_value, volt_value):
            csvwriter.writerow([times, volt])
#----------------------------------------------------------------------------------------------------------
    
print("total time:",time.time()-start_time)
sds.close()