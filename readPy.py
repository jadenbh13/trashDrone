import serial
from time import sleep
import threading
import multiprocessing
from bags import runs
import os
from time import sleep
from testProc import callFunc2
h = False

numbList = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

def onlyNumbs(arg):
    retStr = ""
    for i in arg:
        if i in numbList:
            retStr += i
    return retStr
x = threading.Thread(target=runs)
se1 = False
se2 = False
se3 = False
while True:
    try:
        s = serial.Serial('/dev/ttyUSB0', 115200, timeout=3)
        reds = s.readline().decode()
        red = onlyNumbs(reds)
        print(reds)
        if red == '1':
            x.start()
        if red == '0':
            print("Option 2")
            with open('run.txt', 'w') as filetowrite:
                filetowrite.write('Land')
            print("runLand")
            #callFunc2()
    except Exception as e:
        print(e)
