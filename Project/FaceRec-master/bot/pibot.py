import serial
import socket
import time

ard=serial.Serial('com5',9600)
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("connecting")
s.bind(('',9000)) 
s.listen(10)

con,ad= s.accept()
print("connected")
s=con.recv(10)
f=0
while (True):
	s=con.recv(1)
	print('s=',s)
	s=s.decode()
	if(s!=' ' and s!='\n' and s!=''):
		if (s=='-'):
			s=con.recv(1)
			f=1
		v=int(s)
		
		if(f==1):
			v=v*-1
		print('v=',v)
		sv=(str(v)).encode()
		ard.write(sv)
		ard.flush()
		av=ard.readline()
		print('av=',av)
		

con.close()		
		
	
	

