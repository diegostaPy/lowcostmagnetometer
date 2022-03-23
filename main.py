from guizero import App,Text
from subprocess import Popen,PIPE
import os,signal

from readGps import readGps
import time

import sh
import datetime as dt
import subprocess
from os.path import exists
os.chdir('/home/pi/Desktop/EstGeoMag_FIUNA/Codigo')
def update():
    global diaInicio, processoMag, processoTemp
    today=dt.datetime.now()
    if ((diaInicio.strftime("%m/%d/%Y"))!=today.strftime("%m/%d/%Y")):
        os.killpg(os.getpgid(processoMag.pid), signal.SIGTERM)
        os.killpg(os.getpgid(processoTemp.pid), signal.SIGTERM)
        time.sleep(20)
        os.system("python3 leerDatos.py &")
        time.sleep(2)
        os.system("python3 leerTemperatura.py &")
        diaInicio=dt.datetime.now()
        welcome_message2.value=diaInicio.strftime("%m/%d/%Y, %H:%M:%S")
        
    filenameMag = "../datos/Datos_"+ str(today.date()) + ".csv"
    filenameTemp = "../datos/Temperatura_"+ str(today.date()) + ".csv"
    line_count(textMagN,filenameMag)
    line_count(textTempN,filenameTemp)

    lastline(textMag,filenameMag)
    lastline(textTemp,filenameTemp)
   
def line_count(var,filename):
    if(exists(filename)):
        var.value=str(int(subprocess.check_output(['wc', '-l', filename]).split()[0]))+" registros"
    else:
        var.value="Aun no se creo el archivo del dia"
def lastline(var,filename):
    if(exists(filename)):
        var.value=subprocess.check_output(['tail', '-1', filename])

    else:
        var.value="Aun no hay datos del dia"
def mostrarVentana():
    global GPS,diaInicio, processoMag, processoTemp,textTempN,textMagN,textTemp,textMag,welcome_message2
    
    app = App(title="Magnetometro en funcionamiento", width=1000, 
        height=300, 
        layout="auto", 
        bg=None, 
        visible=True)
    time.sleep(5)
    GPS = readGps()
   # try:
    #    GPS.readGps_init()
    #except :
    #    print("Error: GPS")
    time.sleep(5)
    GPS.read()
    time.sleep(5)
    print(GPS.lat)
    print(GPS.lng)
    print(GPS.timestamp)
    print(GPS.status)
    print(GPS.time)
    diaInicio=dt.datetime.now()
    filename = "../datos/Datos_"+ str(diaInicio.date()) + ".csv"
    welcome_message0 = Text(app, text="Latitud " + GPS.lat+ " Longitud "+ GPS.lng,size=16, font="Times New Roman", color="black")

    welcome_message1 = Text(app, text="Toma datos iniciada el ",size=16, font="Times New Roman", color="black")
    welcome_message2 = Text(app, text=  diaInicio.strftime("%m/%d/%Y, %H:%M:%S"),size=16, font="Times New Roman", color="black")
    welcome_message21= Text(app, text=  "Los ultimos registros de temperatura son:",size=16,font="Times New Roman", color="black")
    textTemp = Text(app, text= "",size=12, font="Times New Roman", color="black")
    textTempN= Text(app, text= "",size=12, font="Times New Roman", color="black")
 
    welcome_message22= Text(app, text=  "Los ultimos registros de voltaje son:",size=16, font="Times New Roman", color="black")
   
 
   
    textMag = Text(app, text= "",size=12, font="Times New Roman", color="black")
    textMagN = Text(app, text= "",size=12, font="Times New Roman", color="black")
   
    app.repeat(20000,update)
    app.display()

    #filename = "../datos/Temperatura_"+ str(dt.datetime.now().date()) + ".csv"
    #line=tail = sh.tail("-f", filename, _iter=True)
    #welcome_message2 = Text(app, text=line, size=12, font="Times New Roman", color="lightblue")

try:
    global processoMag,processoTemp
    time.sleep(5)

    processoMag =Popen("python3 leerDatos.py",stdout=PIPE, stderr=PIPE, shell=True,preexec_fn=os.setsid)
    processoTemp =Popen("python3 leerTemperatura.py",stdout=PIPE, stderr=PIPE, shell=True,preexec_fn=os.setsid)
    mostrarVentana()

    os.killpg(os.getpgid(processoMag.pid), signal.SIGTERM)

    os.killpg(os.getpgid(processoTemp.pid), signal.SIGTERM)


except :
    os.killpg(os.getpgid(processoMag.pid), signal.SIGTERM)

    os.killpg(os.getpgid(processoTemp.pid), signal.SIGTERM)

    exit()
