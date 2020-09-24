import socket
import sys
import cv2
import pickle
import numpy as np
import struct ## new
import zlib
import tensorflow as tf
from align_custom import AlignCustom
from face_feature import FaceFeature
from mtcnn_detect import MTCNNDetect
from tf_graph import FaceRecGraph
import argparse
import sys
import json
import time
from threading import *
import multiprocessing
from multiprocessing import Pipe
import mss
import time
from FaceRecog import *
global server_socket
global FrameCounter
global frameList
global devices
global noc


def add(a,b):
	c=a+b
	print(c)
	return c

def createSocket():
	global server_socket
	global FrameCounter
	global aligner
	global extract_feature
	global face_detect
	global devices
	global noc
	devices=[]
	FrameCounter,aligner,extract_feature,face_detect=startRec()
	FrameCounter=0
	noc=1000
	server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	#server_socket.settimeout(0.1)
	print('Socket created')

	server_socket.bind(('',9000))
	print('Socket bind complete')
	server_socket.listen(noc)
	print('Socket now listening')
	return server_socket
	
def start(socket):
		rpf=Thread(target=recPiFrame(socket))
		rpf.start()
def connectDevice(server_socket):
	global devices
	conCount=0
	try:
		
		print("accepting")
		conn,add=server_socket.accept()
		time.sleep(0.1)
		print("new device connected | address : ",add[0]," ",add[1])
		if conn is not None:
			devices.append(conn)
			
			time.sleep(0.5)
	except Exception as e:
		print(e,"error")
		time.sleep(0.1)
	time.sleep(0.5)

def recPiFrame(server_socket):
	global frameList
	global aligner
	global extract_feature
	global face_detect
	global FrameCounter
	global devices
	frameList=[]	
	d=0
	connectDevice(server_socket)
	
	conn1=devices[0]
	print("|--- Conection has been established with pi ---|")
	p_output, p_input = Pipe()
	svf=Thread(target=sendVideoFrame(server_socket))
	svf.start()
	time.sleep(0.01)
	data = b""
	payload_size = struct.calcsize(">L")
	time.sleep(1)
	print("payload_size: {}".format(payload_size))
	while True:
		print("recv:")
		time.sleep(0.01)
		while len(data) < payload_size:
			data += conn1.recv(4096)
		packed_msg_size = data[:payload_size]
		data = data[payload_size:]
		msg_size = struct.unpack(">L", packed_msg_size)[0]
		while len(data) < msg_size:
			data += conn1.recv(4096)
		frame_data = data[:msg_size]
		data = data[msg_size:]
		frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
		frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
		frameList,FrameCounter,frame=camera_recog(frame,frameList,FrameCounter,aligner,extract_feature,face_detect)
		time.sleep(0.01)
		
		cv2.waitKey(1)


def sendVideoFrame(server_socket):
	global FrameCounter
	global frameList
	global devices
	print("waiting for devices to connect")
	time.sleep(1.0)
	img_counter = 0
	connectDevice(server_socket)
	encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
	print('sending')
	cmdRecThread=Thread(target=RecCommand)
	cmdRecThread.start()
	cmdRecThread.join()
	fail=0

	while True:
		try:
			countDevices=1
			while (countDevices <len(devices)):
				if FrameCounter > 3:
					frame =frameList[FrameCounter-2]
					cv2.imshow('fcontroller'+str(len(frame)),frame)
					result, frame = cv2.imencode('.jpg', frame, encode_param)
					#data = zlib.compress(pickle.dumps(frame, 0))
					data = pickle.dumps(frame, 0)
					size = len(data)

					#print("frames:","{}: {}".format(img_counter, size))
					
					conn2=devices[countDevices]
					ds=conn2.send(frame)
					if(ds==0):
						connectDevice(server_socket)
					
					time.sleep(0.05)
					countDevices+=1
					
					img_counter += 1
					if cv2.waitKey(1) & 0xFF == ord('q'):
						break	
		except Exception as e:
			pass
		
		
def RecCommand():
	time.sleep(1)
	while True:	
		global devices
		cd=1
		while cd<len(devices):
			try:
				
				conn2=devices[cd]
				pr=conn2.recv(10)
				time.sleep(0.050)
				print(pr)
			except Exception as e:
				pass