import serial
import time
class readGps:
    def __init__(self):
        
        try:
            self.ser = serial.Serial('/dev/ttyACM0', 9600, timeout=10)  # Open Serial port
        except :
            self.isopen=False
        else:
            self.isopen=True
        if(not(self.isopen)):
            try:
                self.ser = serial.Serial('/dev/ttyACM1', 9600, timeout=10)  # Open Serial port
            except :
                self.isopen=False
            else:
                self.isopen=True
        
        self.line=[]
        self.lat=''
        self.lng=''
        self.timestamp=''
        self.time=''
        self.status=''
        

 
    def setLatLng(self,latString, lngString):
        self.lat = latString[:2].lstrip('0') + "." + "%.7s" % str(float(latString[2:]) * 1.0 / 60.0).lstrip("0.")
        self.lng = lngString[:3].lstrip('0') + "." + "%.7s" % str(float(lngString[3:]) * 1.0 / 60.0).lstrip("0.")
        
    def checksum(self):
        checkString = self.line.partition("*")
        checksum = 0
        for c in checkString[0]:
            checksum ^= ord(c)

        try:  # Just to make sure
            inputChecksum = int(checkString[2].rstrip(), 16);
        except:
            print("Error in string")
            return False

        if checksum == inputChecksum:
            return True
        else:
            print("===================================Checksum error!===================================")
            print(hex(checksum), "!=", hex(inputChecksum))
            return False
        

    def read(self):
        if self.isopen:
            try:
                k=0
                while True:
                    k=k+1
                    while self.ser.read().decode("utf-8") != '$':  # Wait for the begging of the string
                        pass  # Do nothing
                    self.line = self.ser.readline().decode("utf-8")  # Read the entire string
                    lines = self.line.split(",")
                    
                    if self.checksum():
                   
                        if lines[0] == "GPGLL":
                            
                            self.setLatLng(lines[1], lines[3])
                            self.time= time.strftime("%H:%M:%S",
                                 time.strptime(lines[5], "%H%M%S.%f"))  
                            self.timestamp=lines[5]
                            self.status=lines[6]
                            break
                            
            except:
                print('Error de lectura')
