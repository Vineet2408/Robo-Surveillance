import cv2
import io
import socket
import struct
import time
import pickle
import zlib
import time
global connected
connected = True
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#socket creation
client_socket.connect(('192.168.1.5', 9000))
connection = client_socket.makefile('wb')
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

cam = cv2.VideoCapture(0)

cam.set(3, 640);
cam.set(4, 480);

img_counter = 0
def Reconnect():
	global connected
	while not connected:
		try :
			print("trying to connect")
			client_socket.connect(('192.168.1.5', 9000))
			connected=True
			print( "re-connection successful" ) 
		except socket.error:
			time.sleep( 2 )

			
	

while True:
	ret, frame = cam.read()
	
	data = pickle.dumps(frame, 0)
	size = len(data)


	print("{}: {}".format(img_counter, size))
	try :
		client_socket.sendall(struct.pack(">L", size) + data)
		print("sent")
	except Exception as e:
		connected=False
		print("disconnected")
		Reconnect()
		
	img_counter += 1
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
	time.sleep(0.01)
        

cam.release()

