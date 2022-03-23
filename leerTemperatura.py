# -*- coding: utf-8 -*-
import time
import board
import busio
import adafruit_mcp9808
import datetime as dt
from subprocess import Popen,PIPE
import os
import RPi.GPIO as GPIO
from os.path import exists


import Adafruit_BMP.BMP085 as BMP085  #IMPORT LIBRARY

try: 
    bmp = BMP085.BMP085()
    bmpF=True
except :
    print("Error: bmp")  
    bmpF=False
i2c_bus=busio.I2C(board.SCL, board.SDA)

#this to get the tempertura from a mcp9808 board

try:    
    mcp = adafruit_mcp9808.MCP9808(i2c_bus)
    mcpF=True
    
except :
    print("Error: MCP")  
    mcpF=False
tempC_estageo=-99
tempC_magneto=-99

GPIO.setmode(GPIO.BCM)
GPIO.setup(4,GPIO.OUT)
GPIO.setup(17,GPIO.OUT)
try:
    GPIO.output(4,False)
    GPIO.output(17,False)
except OSError as err:
    print("OS error: {0}".format(err)) 
    
while True:
    dt_now = dt.datetime.now()
    header =[]            
    header.extend(["Timestamp","Temp_Magnetometro", "Temp_Estageo"])   # Define a CSV  header "Temp_Estageo", 
    diaInicio=dt.datetime.now()

    filename = "../datos/Temperatura_"+ str(dt_now.date()) + ".csv"
    if(not(exists(filename))):
        with open(filename,"w") as file:
            file.write(",".join(str(value) for value in header)+ "\n")   # Write each value from the header 
            file.flush()
    k=0
    with open(filename,"a") as file:           # Open the file into Append mode (enter data without erase previous data)
        while True:
            if(mcpF):
                tempC_estageo = mcp.temperature
            if(bmpF):
                tempC_magneto = bmp.read_temperature()+1.0
            if(tempC_estageo>37):
                try:
                    GPIO.output(4,True)
                    GPIO.output(17,True)
                except :
                    print("Error: GPIO") 
            else:
                try:
                    GPIO.output(4,False)
                    GPIO.output(17,False)
                except :
                    print("Error: GPIO") 
            dt_now = dt.datetime.now()
            file.write(str(dt_now.timestamp()) + "," + str(tempC_magneto) + "," + str(tempC_estageo)+"\n")
            k=k+1
            time.sleep(120)
            if(k%2==0):
                print('Temp_Estageo: {} C'.format(tempC_estageo))
                print('Temp_Magnetometro: {} C'.format(tempC_magneto))
                file.flush()
                today=dt.datetime.now()
                if ((diaInicio.strftime("%m/%d/%Y"))!=today.strftime("%m/%d/%Y")):
                    exit()
            