import serial 
import time 
arduino = serial.Serial(port='COM14', baudrate=115200, timeout=.1) 

while True: 
    value = data = arduino.readline().decode('utf-8')  
    print(value) # printing the value 
