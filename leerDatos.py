
import sys
import numpy as np
import datetime as dt
import ADS1256
from subprocess import Popen,PIPE
import os
import RPi.GPIO as GPIO
from os.path import exists
from readGps import readGps
import time


def leerDatos():
    ADC = ADS1256.ADS1256()
    try:
        ADC.ADS1256_init()
    except :
        print("Error: ADC")  
  
    header =[]            
    header.extend(["Timestamp","x","y","z","v1","v2"])   # Define a CSV header 
    diaInicio=dt.datetime.now()
    
    filename = "../datos/Datos_"+ str(diaInicio.date()) + ".csv"
    GPS = readGps()
    time.sleep(5)
   # try:
    #    GPS.readGps_init()
    #except :
    #    print("Error: GPS")
    GPS.read()
    time.sleep(5)
    print(GPS.lat)
    print(GPS.lng)
    print(GPS.timestamp)
    print(GPS.status)
    print(GPS.time)                   
    k=0
    if(not(exists(filename))):
        with open(filename,"w") as file:
           file.write("#"+str(GPS.lat)+","+str(GPS.lng)+","+str(GPS.time)+","+str(GPS.timestamp)+","+str(GPS.status)+",\n")                             # With the opened file...
           file.write(",".join(str(value) for value in header)+ "\n")   # Write each value from the header
           file.flush()
    with open(filename,"a") as file:           # Open the file into Append mode (enter data without erase previous data)
        while True:
            try:
                xd=ADC.ADS1256_GetChannalValue(0) *5.0/0x7fffff
                yd=ADC.ADS1256_GetChannalValue(1) *5.0/0x7fffff
                zd=ADC.ADS1256_GetChannalValue(2) *5.0/0x7fffff
                v1d=ADC.ADS1256_GetChannalValue(4) *5.0/0x7fffff
                v2d=ADC.ADS1256_GetChannalValue(5) *5.0/0x7fffff
            except :
                print("Error: Lectura") 
            datetime=dt.datetime.now()
            lectura=str(datetime.timestamp()) + "," + str(xd)+ "," + str(yd)+ ","+ str(zd) + "," + str(v1d) + "," + str(v2d)+"\n"
            file.write(lectura)
            k=k+1
            if(k%20==0):
               file.flush()
               today=dt.datetime.now()
               if ((diaInicio.strftime("%m/%d/%Y"))!=today.strftime("%m/%d/%Y")):
                   exit()
                   
            #if k%5==0 and k<1000:
            #    print(lectura)
           # if k%20==0 and k>1000:
            #    print(lectura)
            
try:          
    leerDatos()

except (KeyboardInterrupt):
    exit()
