#### HEADER ####
#PROJECT: CU BOULDER PROJECT TOAD
#AUTHOR: JASON LE(jason.le7131@gmail.com)
#LAST MODIFIED: 5/9/2022
#DESCRIPTION: UPLINK COMMANDS TO CLIENT STAND AND DOWNLINK ENCODER DATA INTO CSV FILE
################

#### LIBRARIES ####
from socket import *
from time import *
from threading import Thread
import ctypes
import os
###################

#### GLOBAL VARIABLES ####
global motor1EncoderData
global motor1TimeData
global motor2EncoderData
global motor2TimeData
global motor3EncoderData
global motor3TimeData
#INITIALIZE ARRAYS
motor1EncoderData = []
motor2EncoderData = []
motor3EncoderData = []
motor1TimeData = []
motor2TimeData = []
motor3TimeData = []
##########################

#### FUNCTIONS ####
def millis():
#FUNCTION: Get milliseconds since the start of the script
#INPUT: NULL
#OUTPUT: t_ms = milliseconds
    tics = ctypes.c_int64()
    freq = ctypes.c_int64()
    #get ticks on the internal ~2MHz QPC clock
    ctypes.windll.Kernel32.QueryPerformanceCounter(ctypes.byref(tics)) 
    #get the actual freq. of the internal ~2MHz QPC clock 
    ctypes.windll.Kernel32.QueryPerformanceFrequency(ctypes.byref(freq)) 
    t_ms = tics.value*1e3/freq.value
    return t_ms

def Motor1():
#FUNCTION: Command and collect from Arduino 1
#INPUT: NULL
#OUTPUT: CSV File (DEGREES vs SECONDS)
    #### CHANGE THESE VARIABLES FOR CURRENT SETUP ####
    ipNumber = '192.168.1.108' #<===CHANGE TO CURRENT ARDUINO 1 IP NUMBER
    pathName = 'C:/Users/spong/Documents/Coding/Python' #<===CHANGE TO CSV LOCATION
    portNumber = 2390 #<===CHANGE TO WANTED PORT NUMBER(MOST OF THE TIME YOU DONT NEED TO CHANGE)
    ##################################################
    #WIFI AND CSV SETUP
    address = (ipNumber,portNumber) 
    client_socket = socket(AF_INET,SOCK_DGRAM)
    client_socket.settimeout(1)
    fileName = 'Motor1.csv'
    completeName = os.path.join(pathName,fileName)
    newFile = open(completeName,"w")
    newFile.write("Time,EncoderAngle,Speed")
    newFile.write("\n")
    #VARIABLE SETUP
    timeInitial = millis()
    counter = 1
    while(1):
        #UPLINK DATA
        commandData = 86 #<===CHANGE THIS TO DESIRED SPEED
        client_socket.sendto(str(commandData).encode('utf-8'),address)
        try:
            #DOWNLINK DATA
            [rec_data,addr] = client_socket.recvfrom(2048)
            motor1EncoderData.append(float(rec_data.decode('utf-8')))
            currentTime = millis() - timeInitial
            motor1TimeData.append(currentTime/1000)
            motor1VelocityData = velocityFunc(motor1EncoderData,motor1TimeData)
            print("Motor1 ON")
            if(counter == -1):
                newFile.write(str(motor1TimeData[-1]))
                newFile.write(",")
                newFile.write(str(motor1EncoderData[-1]))
                newFile.write(",")
                newFile.write(str(motor1VelocityData[-1]))
                newFile.write("\n")
                newFile.flush()
            if(counter != -1):
                counter = counter + 1
                if(counter == 4):
                    counter = -1
        except:
            print("Motor 1 Error")

def Motor2():
#FUNCTION: Command and collect from Arduino 2
#INPUT: NULL
#OUTPUT: CSV File (DEGREES vs SECONDS)
    #### CHANGE THESE VARIABLES FOR CURRENT SETUP ####
    ipNumber = '192.168.1.127' #<===CHANGE TO CURRENT ARDUINO 1 IP NUMBER
    pathName = 'C:/Users/spong/Documents/Coding/Python' #<===CHANGE TO CSV LOCATION
    portNumber = 2390 #<===CHANGE TO WANTED PORT NUMBER(MOST OF THE TIME YOU DONT NEED TO CHANGE)
    ##################################################
    #WIFI AND CSV SETUP
    address = (ipNumber,portNumber)
    client_socket = socket(AF_INET,SOCK_DGRAM)
    client_socket.settimeout(1)
    fileName = 'Motor2.csv'
    completeName = os.path.join(pathName,fileName)
    newFile = open(completeName,"w")
    newFile.write("Time,EncoderAngle,Speed")
    newFile.write("\n")
    #VARIABLE SETUP
    motor2timeInitial = millis()
    counter = 1
    while(1):
        #UPLINK DATA
        commandData = 86 #<===CHANGE THIS TO DESIRED SPEED
        client_socket.sendto(str(commandData).encode('utf-8'),address)
        try:
            #DOWNLINK DATA
            [rec_data,addr] = client_socket.recvfrom(2048)
            motor2EncoderData.append(float(rec_data.decode('utf-8')))
            currentTime = millis() - motor2timeInitial
            motor2TimeData.append(currentTime/1000)
            motor2VelocityData = velocityFunc(motor2EncoderData,motor2TimeData)
            print("Motor2 ON")
            if(counter == -1):
                newFile.write(str(motor2TimeData[-1]))
                newFile.write(",")
                newFile.write(str(motor2EncoderData[-1]))
                newFile.write(",")
                newFile.write(str(motor2VelocityData[-1]))
                newFile.write("\n")
                newFile.flush()
            if(counter != -1):
                counter = counter + 1
                if(counter == 4):
                    counter = -1
        except:
            print("Motor 2 Error")

def Motor3():
#FUNCTION: Command and collect from Arduino 3
#INPUT: NULL
#OUTPUT: CSV File (DEGREES vs SECONDS)
    #### CHANGE THESE VARIABLES FOR CURRENT SETUP ####
    ipNumber = '192.168.1.106' #<===CHANGE TO CURRENT ARDUINO 1 IP NUMBER
    pathName = 'C:/Users/spong/Documents/Coding/Python' #<===CHANGE TO CSV LOCATION
    portNumber = 2390 #<===CHANGE TO WANTED PORT NUMBER(MOST OF THE TIME YOU DONT NEED TO CHANGE)
    ##################################################
    #WIFI AND CSV SETUP
    address = (ipNumber,portNumber)
    client_socket = socket(AF_INET,SOCK_DGRAM)
    client_socket.settimeout(1)
    pathName = 'C:/Users/spong/Documents/Coding/Python'
    fileName = 'Motor3.csv'
    completeName = os.path.join(pathName,fileName)
    newFile = open(completeName,'w')
    newFile.write("Time,EncoderAngle,Speed")
    newFile.write("\n")
    #VARIABLE SETUP
    commandData = 0
    motor3TimeInitial = millis()
    counter = 1
    while(1):
        #UPLINK DATA
        commandData = 800 #<===CHANGE THIS TO DESIRED SPEED
        client_socket.sendto(str(commandData).encode('utf-8'),address)
        try:
            #DOWNLINK DATA
            [rec_data,addr] = client_socket.recvfrom(2048)
            motor3EncoderData.append(float(rec_data.decode('utf-8')))
            currentTime = millis() - motor3TimeInitial 
            motor3TimeData.append(currentTime/1000)
            motor3VelocityData = velocityFunc(motor3EncoderData,motor3TimeData)
            print("Motor3 ON")
            if(counter == -1):
                newFile.write(str(motor3TimeData[-1]))
                newFile.write(",")
                newFile.write(str(motor3EncoderData[-1]))
                newFile.write(",")
                newFile.write(str(motor3VelocityData[-1]))
                newFile.write("\n")
                newFile.flush()
            if(counter != -1):
                counter = counter + 1
                if(counter == 4):
                    counter = -1
        except:
            print("Motor 3 Error")

def velocityFunc(val,t):
#FUNCTION: Determine Velocity from Position Data
#INPUT: val = position data
#       t = time data
#OUTPUT: vel = velocity data
    vel = []
    for i in range(1,len(t)-1):
        vtemp = (val[i+1]-val[i-1])/(t[i+1]-t[i-1])
        vel.append(vtemp)
    return vel
###################

#### THREADING SETUP ####
motor1Thread = Thread(target=Motor1)
motor2Thread = Thread(target=Motor2)
motor3Thread = Thread(target=Motor3)

motor1Thread.daemon=True
motor2Thread.daemon=True
motor3Thread.daemon=True

motor1Thread.start()
motor2Thread.start()
motor3Thread.start()

motor1Thread.join()
motor2Thread.join()
motor3Thread.join()
##########################