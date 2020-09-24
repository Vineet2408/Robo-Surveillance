import serial
import socket
import time
from botMov import *
from threading import *
import cv2
import io
import pickle

global client_socket
global address		
cam=cv2.VideoCapture(0)
#stream = io.BytesIO()
client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect(('192.168.43.22', 9000))

cam.set(3, 640);
cam.set(4, 480);

img_counter = 0
print('sending')


s=client_socket.recv(10)
print(s)
f=0

while(f<15):

	q=ard.readline()
	print(q)
	f=f+1
print('start')

def control():

	while (True):
		try:
			
			data=client_socket.recv(5)
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
		time.sleep(0.001)
		
def camera():
		
	while True:
		ret, frame = cam.read()
		data = pickle.dumps(frame, 0)
		size = len(data)
		print("frames:","{}: {}".format(img_counter, size))
		len1=str(size)
		#sending frame size
		client_socket.send(len1.encode())
		#receiving acknowledgement
		ack=client_socket.recv(2)
		#sending frame 
		client_socket.send(data)
		buy=client_socket.recv(2)
		print("ack for vinnu: ",buy)
		img_counter += 1
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		time.sleep(0.03)
	cam.release()
	
if __name__ == '__main__':
	cam=Thread(target=camera)
	drone=Thread(target=control)
	
	cam.start()
	drone.start()
	
	cam.join()
	drone.join()