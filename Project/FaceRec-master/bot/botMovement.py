import serial
import time
import numpy
ard = serial.Serial('com6',9600) 















	
def moveBackward(speed): 
	psp=((speed).encode())
	sp=(-1*(int(speed))
	sp=(str(sp))

	
	ard.write(psp)	
	str=ard.read(2)
	ard.write(psp)
	str=ard.read(2)
	ard.write(sp)
	str=ard.read(2)
	ard.write(sp)

	
def rollLeft(speed):
	sp=(-1*(int(speed))
	psp=((speed).encode())
	sp=(str(sp)).encode()
	ard.write(sp)
	str=ard.read(2)
	ard.write(psp)
	str=ard.read(2)
	ard.write(sp)
	str=ard.read(2)
	ard.write(psp)
	str=ard.read(2)

def rollRight(speed):
	sp=(-1*(int(speed))
	psp=((speed).encode())
	sp=(str(sp)).encode()
	ard.write(psp)
	str=ard.read(2)
	ard.write(sp)
	str=ard.read(2)
	ard.write(psp)
	str=ard.read(2)
	ard.write(sp)
	str=ard.read(2)
	
def yawLeft(speed):
	sp=speed*-1
	psp=((speed).encode())
	sp=(str(sp)).encode()
	ard.write(psp)
	str=ard.read(2)
	ard.write(sp)
	str=ard.read(2)
	ard.write(sp)
	str=ard.read(2)
	ard.write(psp)
	str=ard.read(2)	
	
def yawLeft(speed):
	sp=(-1*(int(speed))
	psp=((speed).encode())
	sp=(str(sp)).encode()
	ard.write(sp)
	str=ard.read(2)
	ard.write(psp)
	str=ard.read(2)
	ard.write(psp)
	str=ard.read(2)
	ard.write(sp)
	str=ard.read(2)	

def  throttleUp(speed):
	sp=(-1*(int(speed))
	psp=((speed).encode())
	sp=(str(sp)).encode()
	ard.write(psp)
	str=ard.read(2)
	ard.write(psp)
	str=ard.read(2)
	ard.write(psp)
	str=ard.read(2)
	ard.write(psp)
	str=ard.read(2)	
	
	
def throttleDown(speed): 
	sp=(-1*(int(speed))
	psp=((speed).encode())
	sp=(str(sp)).encode()
	ard.write(sp)
	str=ard.read(2)
	ard.write(sp)
	str=ard.read(2)
	ard.write(sp)
	str=ard.read(2)
	ard.write(sp)
	str=ard.read(2)	
