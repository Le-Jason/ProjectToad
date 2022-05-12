#### HEADER ####
#PROJECT: CU BOULDER PROJECT TOAD
#AUTHOR: JASON LE(jason.le7131@gmail.com)
#LAST MODIFIED: 5/9/2022
#DESCRIPTION: STOP MOVEMENT FROM CLIENT STAND
################

#### LIBRARIES ####
from socket import *
from threading import Thread
###################

#### FUNCTIONS ####
def Motor1():
#FUNCTION: Stop Arduino 1
#INPUT: NULL
#OUTPUT: NULL
    #### CHANGE THESE VARIABLES FOR CURRENT SETUP ####
    ipNumber = '192.168.1.108' #<===CHANGE TO CURRENT ARDUINO 1 IP NUMBER
    portNumber = 2390 #<===CHANGE TO WANTED PORT NUMBER(MOST OF THE TIME YOU DONT NEED TO CHANGE)
    ##################################################
    #WIFI SETUP
    adress = (ipNumber,portNumber)
    client_socket = socket(AF_INET,SOCK_DGRAM)
    client_socket.settimeout(1)
    while(1):
        try:
            #UPLINK DATA
            commandData = 90 #<===CHANGE THIS TO STOP SPEED
            client_socket.sendto(str(commandData).encode('utf-8'),adress)
        except:
            pass
def Motor2():
#FUNCTION: Stop Arduino 2
#INPUT: NULL
#OUTPUT: NULL
    #### CHANGE THESE VARIABLES FOR CURRENT SETUP ####
    ipNumber = '192.168.1.127' #<===CHANGE TO CURRENT ARDUINO 1 IP NUMBER
    portNumber = 2390 #<===CHANGE TO WANTED PORT NUMBER(MOST OF THE TIME YOU DONT NEED TO CHANGE)
    ##################################################
    #WIFI SETUP
    address = (ipNumber,portNumber)
    client_socket = socket(AF_INET,SOCK_DGRAM)
    client_socket.settimeout(1)
    while(1):
        try:
            #UPLINK DATA
            commandData = 90 #<===CHANGE THIS TO STOP SPEED
            client_socket.sendto(str(commandData).encode('utf-8'),address)
        except:
            pass
    

def Motor3():
#FUNCTION: Stop Arduino 2
#INPUT: NULL
#OUTPUT: NULL
    #### CHANGE THESE VARIABLES FOR CURRENT SETUP ####
    ipNumber = '192.168.1.106' #<===CHANGE TO CURRENT ARDUINO 1 IP NUMBER
    portNumber = 2390 #<===CHANGE TO WANTED PORT NUMBER(MOST OF THE TIME YOU DONT NEED TO CHANGE)
    ##################################################
    address = (ipNumber,portNumber)
    client_socket = socket(AF_INET,SOCK_DGRAM)
    client_socket.settimeout(1)
    while(1):
        try:
            #UPLINK DATA
            commandData = 0 #<===CHANGE THIS TO STOP SPEED
            client_socket.sendto(str(commandData).encode('utf-8'),address)
        except:
            pass
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