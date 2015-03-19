import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
dataReg=[40, 38, 37, 36, 35, 33, 32, 31]

start = 7
reset = 11
addressStrobe = 12
dataStrobe = 13
interrupt = 15
reset = 16
wait = 18
write = 22

GPIO.setup(start,GPIO.OUT)
GPIO.setup(reset,GPIO.OUT)
GPIO.setup(dataStrobe,GPIO.OUT)
GPIO.setup(addressStrobe,GPIO.OUT)
GPIO.setup(write,GPIO.OUT)
GPIO.setup(interrupt,GPIO.IN)
GPIO.setup(wait,GPIO.IN)

GPIO.output(write,GPIO.HIGH)

GPIO.output(dataStrobe,GPIO.HIGH)
GPIO.output(addressStrobe,GPIO.HIGH)
GPIO.output(start,GPIO.LOW)

#data write
def dataWrite(data): #data is a 8 bit binary array
    for x in range(8):
        GPIO.setup(dataReg[x],GPIO.OUT)
        print 'pin ' +str(dataReg[x]) + 'is set to be the ouput'
        

    GPIO.output(write,GPIO.LOW)
    print 'set WRITE to low'

    for x in range(0,8):
        GPIO.output(dataReg[x],data[x])
        print 'number'+ str(x) +' write '+ str(data[x]) + ' to pin '+ str(dataReg[x])

    GPIO.output(dataStrobe,GPIO.HIGH)
    print 'set data Strobe to high'
                    
    
    GPIO.output(start,GPIO.HIGH)
    print 'set START to high'
                    
    while True:
        if not GPIO.input(wait):
            break
    print 'received the wait signal'

    GPIO.output(dataStrobe,GPIO.LOW)
    print 'set data Strobe to low'
    
    GPIO.cleanup(dataReg)
    print 'cleared up pin ' + str(dataReg[0]) + 'to' +str(dataReg[7])
 
    GPIO.output(dataStrobe,GPIO.HIGH)
    print 'set data strobe to high'
    GPIO.output(write,GPIO.HIGH)
    print 'set Write to high'
    GPIO.output(start,GPIO.LOW)
    print 'set start to low'
    



#address write
def addressWrite(address):


    for x in range(0,8):
        GPIO.setup(dataReg[x],GPIO.OUT)
        print 'pin ' +str(dataReg[x]) + 'is set to be the ouput'
                    
    
    GPIO.output(write,GPIO.LOW)
    print 'set WRITE to low'

    for x in range(0,8):
        GPIO.output(dataReg[x],address[x])
        print 'number'+ str(x) +' write '+ str(address[x]) + ' to pin '+ str(dataReg[x])

        
    GPIO.output(addressStrobe,GPIO.LOW)
    print 'set address Strobe to high'

    GPIO.output(start,GPIO.HIGH)
    print 'set START to high'
    
    while True:
        if not GPIO.input(wait):
            break
    print 'received the wait signal'

    GPIO.cleanup(dataReg)
    print 'cleared up pin ' + str(dataReg[0]) + 'to' +str(dataReg[7])

    GPIO.output(addressStrobe,GPIO.HIGH)
    print 'set address strobe to high'

    GPIO.output(write,GPIO.HIGH)
    print 'set WRITE to high'

    GPIO.output(start,GPIO.LOW)
    print 'set start to low'
    
#data read
def dataRead(data):

    for x in range(0,8):
        GPIO.setup(dataReg[x],GPIO.IN)
        print 'pin ' +str(dataReg[x]) + 'is set to be the input'

    GPIO.output(start,GPIO.HIGH)
    print 'set START to LOW'

    GPIO.output(write,GPIO.HIGH)
    print 'set WRITE to HIGH'
    GPIO.output(dataStrobe,GPIO.LOW)
    print 'set data Strobe to LOW'

    while True:
        if not GPIO.input(wait):
            break
    print 'received the wait signal'            

    for x in range(0,8):
        data[x] = GPIO.input(dataReg[x])
        print 'number'+ str(x) +' read '+ str(address[x]) + ' from  pin '+ str(dataReg[x])

    GPIO.cleanup(dataReg)
    print 'cleared up pin ' + str(dataReg[0]) + 'to' +str(dataReg[7])

    GPIO.output(dataStrobe,GPIO.HIGH)
    print 'set data Strobe to HIGH'

    GPIO.output(start,GPIO.LOW)
    print 'set Start to LOW'

#address read
def addressRead(address):
    for x in range(0,8):
        GPIO.setup(dataReg[x],GPIO.IN)
        print 'pin ' +str(dataReg[x]) + 'is set to be the input'

    GPIO.output(start,GPIO.HIGH)
    print 'set START to high'
    GPIO.output(write,GPIO.HIGH)
    print 'set WRITE to high'
    GPIO.output(addressStrobe,GPIO.LOW)
    print 'set address Strobe to LOW'

    while True:
        if not GPIO.input(wait):
            break
    print 'received the wait signal' 

    for x in range(0,8):
        address[x] = GPIO.input(dataReg[x])
        print 'number'+ str(x) +' read '+ str(address[x]) + ' from  pin '+ str(dataReg[x])

    GPIO.cleanup(dataReg)
    print 'cleared up pin ' + str(dataReg[0]) + 'to' +str(dataReg[7])
    
    GPIO.output(addressStrobe,GPIO.HIGH)
    print 'set address Strobe to HIGH'

    GPIO.output(start,GPIO.LOW)
    print 'set Start to LOW'



data= [0,0,0,0,0,0,0,0]
data1= [1,1,1,1,1,1,1,1]
dataWrite(data1)
GPIO.cleanup()
