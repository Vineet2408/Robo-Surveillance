import serial
import socket
import time
from botMov import *

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("connecting")
s.bind(('',9000)) 
s.listen(10)

con,ad= s.accept()
print("connected =",ad)

s=con.recv(10)
print(s)
f=0
while(f<5):

	q=ard.readline()
	print(q)
	f=f+1
print('start')
while (True):
	try:
		
		data=con.recv(5)
		ar=data.split()
		joy=ar[0]
		dir=ar[1]
		offset=ar[2]
		joy=joy.decode()
		dir=dir.decode()
		s=offset.decode()	
		offset=offset.decode()

		print('joy = ',joy,'dir = ',dir,'offset = ',offset)
		if 'l' in joy:
			if (dir=='0'):
				print("center left")
			elif dir=='1':
				print('thottle up =',offset)
				tu(offset)
				
			elif dir=='2':
				print('yaw right =',offset)	
				yr(offset)		
			elif dir=='3':
				print('thottle down =',offset)
				td(offset)			
			elif dir=='4':
				print('yaw left =',offset)
				yl(offset)
				
		elif 'r' in joy:
			if (dir=='0'):
				print("center right")
			elif dir=='1':
				print('pitch forward =',offset)
				mf(offset)
			elif dir=='2':
				print('roll right')
				rr(offset)
			elif dir=='3':
				print('pitch backward =',offset)
				mb(offset)
			elif dir=='4':
				print('roll left =',offset)
				rl(offset)	
			
		data=""	
	except Exception as e:
		print("error")
